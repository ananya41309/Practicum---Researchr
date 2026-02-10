from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os, requests, json

#DELETE
#from demodata import grants

app = Flask(__name__)
search_url = "https://api.grants.gov/v1/api/search2"
fetchOpp_url = "https://api.grants.gov/v1/api/fetchOpportunity"

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "csv", "txt"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        files = request.files.getlist("files")

        print("Title:", title)
        print("Description:", description)

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        #return redirect(url_for("index"))

    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    title = request.form["title"]
    description = request.form["description"]

    keywords = description.split()
    print("Keywords:", keywords)
    statuses = "forecasted"
    #build json request
    payload = {
        "keywords": keywords,
        "oppStatuses": "forecasted|posted"
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
        for hit in hits[:10]:  # Limit to top 10 results
        
            hit_title = hit.get("title", "No Title")
            print(hit)
            hit_id = hit.get("id", 0)
            opp_payload = {
                "opportunityId": hit_id
            }
            print(hit_id)
            opp_response = requests.post(fetchOpp_url, data=json.dumps(opp_payload))
            if opp_response.status_code == 200:
                opp_data = opp_response.json().get("data", {})
                #print("Opportunity Data:", opp_data)
                if not opp_data.get("forecast", {}):
                    opp_desc = opp_data.get("synopsis", {}).get("synopsisDesc", "No Description")
                else:
                    opp_desc = opp_data.get("forecast", {}).get("forecastDesc", "No Description")
                grants.append({
                    "id": hit_id,
                    "title": hit_title,
                    "description": opp_desc
                })
            
    #project_text = f"{title} {description}"

    results = grants #match_grants(project_text, grants)
    
    return render_template("results.html", results=results, title=title, description=description)


if __name__ == "__main__":
    app.run(debug=True)
