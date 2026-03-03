import time

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os, requests, json
from file_parser import parse_file
from keyword_extractor import extract_keywords
from google import genai
from api_key import api_key
from search import search_grants

#DELETE
#from demodata import grants

app = Flask(__name__)
search_url = "https://api.grants.gov/v1/api/search2"
fetchOpp_url = "https://api.grants.gov/v1/api/fetchOpportunity"

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "csv", "txt"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

client = genai.Client(api_key=api_key)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def compute_relevance(grant_text, keywords):
    grant_text = grant_text.lower()
    score = 0
    
    """for keyword in keywords:
        if keyword.lower() in grant_text:
            score += 1
    """
    
    for word in grant_text.split():
        if word in keywords:

            score += 1.0
            
    if len(keywords) == 0:
        return 0

    return round(score / len(set(grant_text.split())), 2)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        files = request.files.getlist("files")

        extracted_text = ""

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(file_path)

                extracted_text += " " + parse_file(file_path)
                keywords = extract_keywords(extracted_text)
                app.config["KEYWORDS"] = keywords


        # Store parsed text temporarily (simple approach)
        app.config["PARSED_TEXT"] = extracted_text

    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    title = request.form["title"]
    description = request.form["description"]

    file_text = app.config.get("PARSED_TEXT", "")

    # keywords from uploaded documents
    doc_keywords = app.config.get("KEYWORDS", [])

    # keywords from project description
    desc_keywords = extract_keywords(description)

    # merge + remove duplicates
    merged_keywords = list(set(doc_keywords + desc_keywords))

    print("\n--- KEYWORD DEBUG ---")
    print("Document Keywords:", doc_keywords)
    print("Description Keywords:", desc_keywords)
    print("Merged Keywords:", merged_keywords)
    print("----------------------\n")

    results = search_grants(title, description, merged_keywords)
    """

    #build json request
    payload = {
        "oppStatuses": "forecasted|posted",
        "keyword": combined_text,
    }

    headers = {  
        "Content-Type": "application/json",
    }
    
    response = requests.post(search_url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        res = response.json()
        #print("API Response:", res)
        data = res.get("data", {})
        hits = data.get("oppHits", [])
        #print(hits)    
        grants = []
        
        while not hits and merged_keywords:
            #remove last 2 keywords and try again
            merged_keywords = merged_keywords[:-2]
            keyword_string = " ".join(merged_keywords)
            combined_text = f"{title} {keyword_string}"
            
            payload = {
                "oppStatuses": "forecasted|posted",
                "keyword": combined_text,
            }
            
            print("\n--- KEYWORD DEBUG ---")
            print("Document Keywords:", doc_keywords)
            print("Description Keywords:", desc_keywords)
            print("Merged Keywords:", merged_keywords)
            print(payload)
            print("----------------------\n")
            
            response = requests.post(search_url, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                res = response.json()
                data = res.get("data", {})
                hits = data.get("oppHits", [])
            
        for hit in hits[:10]:  # Limit to top 10 results
        
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

                if opp_desc != "No Description":
                    try:
                        response = client.models.generate_content(
                            model="gemini-3-flash-preview", contents="Return only the relevant output. Given this description of a grant opportunity, summarize the description: " + opp_desc
                        )
                        opp_desc = response.text
                    except Exception as e:
                        print("Error generating summary:", e)
                        pass
                    time.sleep(1)
                
                average_award = None
                try:
                    if award_ceiling and award_floor:
                        average_award = (int(award_ceiling) + int(award_floor)) // 2
                except ValueError:
                    average_award = None
                
                grants.append({
                    "id": hit_id,
                    "title": hit_title,
                    "description": opp_desc,
                    "openDate": hit_opendate,
                    "closeDate": hit_closedate,
                    "award_ceiling": award_ceiling,
                    "award_floor": award_floor,
                    "average_award": average_award
                })
            
    #project_text = f"{title} {description}"

    for grant in grants:
        grant_text = grant.get("description", "")
        relevance = compute_relevance(grant_text, merged_keywords)
        grant["relevance"] = relevance

    # Sort grants by relevance score in descending order
    results = sorted(grants, key=lambda x: x["relevance"], reverse=True)
    
    best_relevance = results[0]["relevance"] if results else 0
    
    for grant in results:
        grant["relevance"] = round((grant["relevance"] / best_relevance), 2) if best_relevance > 0 else 0
        print(f"Title: {grant['title']}, Relevance: {grant['relevance']}")"""
    
    return render_template("results.html", results=results, title=title, description=description)

if __name__ == "__main__":
    app.run(debug=True)
