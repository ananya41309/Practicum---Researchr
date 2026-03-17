""" 
    This application will search for potential grants based on the title and description of a document. 
    It will use the keywords extracted from the document and the description to search for grants that match those keywords. 
    The search will be done using a variety of sources and search engines. The results will be returned as a list of grants that match the keywords. 
"""
import json
from xml.etree.ElementPath import find
import requests
from bs4 import BeautifulSoup
import re
from openai import OpenAI
from api_key import api_key
from datetime import datetime

search_url = "https://api.grants.gov/v1/api/search2"
fetchOpp_url = "https://api.grants.gov/v1/api/fetchOpportunity"
nufr_url = "https://www.northwestern.edu/foundationrelations/find-funding/funding-opportunities/"

#client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
def try_parse_int(x):
    try:
        return int(x)
    except Exception:
        try:
            return int(float(x))
        except Exception:
            return None

def parse_date_safe(d):
    """
    Try common formats and return ISO 'YYYY-MM-DD' or None.
    Accepts 'MM/DD/YYYY', 'YYYY-MM-DD', or date-like strings, or 'Rolling'.
    """
    if not d:
        return None
    s = str(d).strip()
    if s.lower() == "rolling":
        return "rolling"
    # try common formats
    fmts = ["%m/%d/%Y", "%Y-%m-%d", "%m-%d-%Y"]
    for f in fmts:
        try:
            dt = datetime.strptime(s, f)
            return dt.date().isoformat()
        except Exception:
            continue
    # try to extract using regex mm/dd/yyyy
    m = re.search(r"(\d{1,2}/\d{1,2}/\d{4})", s)
    if m:
        try:
            dt = datetime.strptime(m.group(1), "%m/%d/%Y")
            return dt.date().isoformat()
        except Exception:
            pass
    return None

def extract_best_award(r):
    if r.get("average_award"):
        v = try_parse_int(r["average_award"])
        if v is not None:
            return v
    # try floor/ceiling
    floor = try_parse_int(r.get("award_floor"))
    ceil = try_parse_int(r.get("award_ceiling"))
    if floor is not None and ceil is not None:
        return (floor + ceil) // 2
    if floor is not None:
        return floor
    if ceil is not None:
        return ceil
    # try 'amount' free text (NU site)
    amt_field = r.get("amount")
    if amt_field:
        # find first integer in string
        m = re.search(r"[\$]?([\d,]+)", str(amt_field))
        if m:
            v = try_parse_int(m.group(1).replace(",", ""))
            if v is not None:
                return v
    return None

def apply_filters(results, status_open, status_forecast, sources, award_min, award_max):
    """
    Filter results list in place and return filtered list.
    sources is a list (e.g. ['federal','foundation']) or empty/None to mean all.
    award_min/award_max are strings (or None); convert to ints if present.
    """
    out = []
    amin = try_parse_int(award_min) if award_min is not None and award_min != "" else None
    amax = try_parse_int(award_max) if award_max is not None and award_max != "" else None
    want_sources = set([s.lower().strip() for s in sources]) if sources else None

    for r in results:
        src = (r.get("source") or "").lower().strip()
        if want_sources and src not in want_sources:
            continue

        # status filter
        status = str(r.get("status", "")).lower()
        if (status_open or status_forecast):
            ok_status = False
            if status_open:
                if any(k in status for k in ("open", "posted", "open opportunity", "open_date", "open-now")) or status == "":
                    ok_status = True
            if status_forecast:
                if any(k in status for k in ("forecast", "anticipated", "forecasted", "archived")):
                    ok_status = True
            if not ok_status:
                continue

        # award filter
        award = extract_best_award(r)
        if amin is not None and award is not None and award < amin:
            continue
        if amax is not None and award is not None and award > amax:
            continue
        print(r['title'])
        out.append(r)
    return out

def sort_results(results, sort_by="relevance"):
    if sort_by == "deadline":
        # rolling first (lowest key), then earliest date, then unknown
        def keyfn(r):
            close = r.get("closeDate") or r.get("deadline") or ""
            parsed = parse_date_safe(close)
            if parsed == "rolling":
                return (0, "")
            if parsed:
                try:
                    return (1, parsed)
                except Exception:
                    return (2, "")
            return (3, "")
        return sorted(results, key=keyfn)
    else:
        return sorted(results, key=lambda x: float(x.get("score", 0)), reverse=True)

def search_grants(title, description, keywords, client, status_open=True, status_forecast = False, sources=None, award_min = None, award_max = None, sort_by="relevance", limit=10):
    #given keyword string, we are going to search through various sources for grants that match the keywords. We will return a list of grants that match the keywords.
    results = []
    
    grants_gov_grants = grants_gov_search(title, keywords)
    results.extend(grants_gov_grants)
    
    nufr_grants = nufr_search(keywords)
    results.extend(nufr_grants)

    filtered = apply_filters(results, status_open, status_forecast, sources, award_min, award_max)
    ranked = sort_results(filtered, sort_by = sort_by)
    top_n = ranked[:limit]
    
    #ranked = sorted(results, key=lambda x: x["score"], reverse=True)
    
    # generate summaries for the best results
    for r in top_n:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for summarizing grant opportunities for applying researchers."},
                {"role": "user", "content": f"Given the following grant opportunity, title: {r['title']}, description: {r['description']}, please return a concise summary of the grant details. This summary should only written as a standard paragraph. Return only the body of the summary without any introductory phrases."}
            ]
        )
        
        summary = response.choices[0].message.content.strip()
        r["summary"] = summary
        #r["summary"] = ""
    
    print ("Ranked Grants:")
    for r in top_n:
        print(r["title"], r["score"], r["summary"])
        
    return top_n

def nufr_search(keywords):
    
    """
        given keywords, we are going to parse through the NU foundations relations website and 
        find grants that match the keywords. We will return a list of grants that match the keywords.
    """
    
    headers = { "User-Agent": "Mozilla/5.0" }

    r = requests.get(nufr_url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
        
    rows = soup.select("table tr")  # adjust selector if needed
    
    data = [] # this contains all of the rows from the table

    for row in rows[1:]:  # skip header
        
        # Find the hidden description container
        row_soup = BeautifulSoup(str(row), "html.parser")
        
        description_div = row_soup.select_one(".details-description")
        
        # Extract only real outbound links (exclude href="#")
        link_tag = description_div.find("a", href=True)

        if link_tag and link_tag["href"] != "#":
            grant_url = link_tag["href"]
        else:
            grant_url = None
        
        cells = [td.get_text(strip=True) for td in row.find_all("td")]
        if cells:
            
            pattern = r"(Rolling|\d{2}/\d{2}/\d{4})\s*$"
            
            match = re.search(pattern, cells[0])

            if match:
                terminal_value = match.group(1)
            else:
                terminal_value = None
                
            cleaned = re.sub(
                r"\n?Explore the.*(?:\n|$)",
                "",
                cells[0],
                flags=re.IGNORECASE
            ).strip()

            data.append({
                "description": cleaned,
                "openDate": "N/A",
                "closeDate": terminal_value or cells[0],
                "title": cells[1],
                "funder": cells[2],
                "status": cells[3],
                "award_floor": "none",
                "award_ceiling": "none",
                "amount": cells[4],
                "career_stage": cells[5],
                "discipline": cells[6],
                "deadline_month": cells[7],
                "url": grant_url,
                "source": "foundation"
            })
            
    def combined_text(entry):
        return " ".join([
            entry.get("title", ""),
            entry.get("description", ""),
            entry.get("discipline", "")
        ])
    
    def keyword_score(text, keywords):
        text = text.lower()
        return sum(text.count(k.lower()) for k in keywords)
    
    for r in data:
        r["score"] = keyword_score(combined_text(r), keywords)

    ranked = sorted(data, key=lambda x: x["score"], reverse=True)
    return ranked[:50]  # return top 10 results   

def grants_gov_search(title, keywords):
    """
        search grants.gov for grants that match the keywords. We will return a list of grants that match the keywords.
    """
    
    keyword_string = " ".join(keywords)
    combined_text = f"{title} {keyword_string}"
    
    #build json request
    payload = {
        "oppStatuses": "forecasted|posted",
        "keyword": combined_text,
    }

    headers = {  
        "Content-Type": "application/json",
    }
    
    grants = []
    
    response = requests.post(search_url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        res = response.json()
        #print("API Response:", res)
        data = res.get("data", {})
        hits = data.get("oppHits", [])
        #print(hits)    
        
        while not hits and keywords:
            #remove last 2 keywords and try again
            keywords = keywords[:-2]
            keyword_string = " ".join(keywords)
            combined_text = f"{title} {keyword_string}"
            
            payload = {
                "oppStatuses": "forecasted|posted",
                "keyword": combined_text,
            }
            
            response = requests.post(search_url, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                res = response.json()
                data = res.get("data", {})
                hits = data.get("oppHits", [])
            
        for hit in hits[:40]:
        
            hit_title = hit.get("title", "No Title")
            print(hit)
            hit_id = hit.get("id", 0)
            opp_payload = {
                "opportunityId": hit_id
            }
            print(hit_id)
            hit_opendate = hit.get("openDate", "N/A")
            if hit_opendate == "":
                hit_opendate = "N/A"
            hit_closedate = hit.get("closeDate", "N/A")
            if hit_closedate == "":
                hit_closedate = "N/A"
            hit_status = hit.get("oppStatus") or hit.get("status") or "posted"
            opp_response = requests.post(fetchOpp_url, data=json.dumps(opp_payload))
            if opp_response.status_code == 200:
                opp_data = opp_response.json().get("data", {})
                #print("Opportunity Data:", opp_data)
                if not opp_data.get("forecast", {}):
                    opp_desc = opp_data.get("synopsis", {}).get("synopsisDesc", "No Description")
                    award_ceiling = opp_data.get("synopsis", {}).get("awardCeiling")
                    award_floor = opp_data.get("synopsis", {}).get("awardFloor")
                else:
                    opp_desc = opp_data.get("forecast", {}).get("forecastDesc", "No Description")
                    award_ceiling = opp_data.get("forecast", {}).get("awardCeiling")
                    award_floor = opp_data.get("forecast", {}).get("awardFloor")

                """if opp_desc != "No Description":
                    try:
                        response = client.models.generate_content(
                            model="gemini-3-flash-preview", contents="Return only the relevant output. Given this description of a grant opportunity, summarize the description: " + opp_desc
                        )
                        opp_desc = response.text
                    except Exception as e:
                        print("Error generating summary:", e)
                        pass
                    time.sleep(1)"""
                average_award = None
                try:
                    if award_ceiling and award_floor:
                        average_award = (int(award_ceiling) + int(award_floor)) // 2
                except ValueError:
                    average_award = None
                    award_ceiling = None
                    award_floor = None
                
                print("Award Ceiling:", award_ceiling)
                print("Award Floor:", award_floor)
                grants.append({
                    "id": hit_id,
                    "title": hit_title,
                    "description": opp_desc,
                    "openDate": hit_opendate,
                    "closeDate": hit_closedate,
                    "award_ceiling": award_ceiling,
                    "award_floor": award_floor,
                    "average_award": average_award,
                    "url": f"https://www.grants.gov/search-results-detail/{hit_id}",
                    "source": "federal",
                    "status": hit_status
                })
                
    def combined_text(entry):
        return " ".join([
            entry.get("title", ""),
            entry.get("description", "")
        ])
    
    def keyword_score(text, keywords):
        text = text.lower()
        return sum(text.count(k.lower()) for k in keywords)
    
    for r in grants:
        r["score"] = keyword_score(combined_text(r), keywords)

    ranked = sorted(grants, key=lambda x: x["score"], reverse=True)
    return ranked[:50]  # return top 10 results