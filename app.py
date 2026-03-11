import time

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from file_parser import parse_file
from keyword_extractor import extract_keywords
from openai import OpenAI
from api_key import api_key
#from google import genai

from search import search_grants

#DELETE
#from demodata import grants

app = Flask(__name__)
search_url = "https://api.grants.gov/v1/api/search2"
fetchOpp_url = "https://api.grants.gov/v1/api/fetchOpportunity"

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "csv", "txt"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

#client = genai.Client(api_key=api_key)
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

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

@app.route("/edit-search", methods=["POST"])
def edit_search():
    title = request.form["title"]
    description = request.form["description"]

    # edit the keywords based on user input
    new_keywords = request.form["keywords"].strip().split(", ")
    
    results = search_grants(title, description, new_keywords, client)
    #results = search_grants(title, description, merged_keywords, client)
    
    if len(description) > 500:
        description = description[:500] + "..."
    
    return render_template("results.html", results=results, title=title, description=description, keywords=new_keywords)

@app.route("/search", methods=["POST"])
def search():
    title = request.form["title"]
    description = request.form["description"]

    file_text = app.config.get("PARSED_TEXT", "")

    # keywords from uploaded documents
    doc_keywords = app.config.get("KEYWORDS", [])

    # keywords from project description
    #desc_keywords = extract_keywords(description)

    # merge + remove duplicates
    #merged_keywords = list(set(doc_keywords + desc_keywords))

    #print("Document Keywords:", doc_keywords)
    #print("Description Keywords:", desc_keywords)
    #print("Merged Keywords:", merged_keywords)
    #print("----------------------\n")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for ranking grant opportunities based on relevance to a researcher's interests."},
            {"role": "user", "content": f"Given these details about the research project: {title} {description} {file_text}, please generate a list of the top 10 keywords that best represent the researcher's interests and the project focus. These keywords will be used to search for relevant grant opportunities. Please return only the keywords in a list format without any additional text or explanation, separated only by spaces."}
        ]
    )
    ds_keywords = response.choices[0].message.content.strip().split()
    
    print("\n--- KEYWORD DEBUG ---")
    print(ds_keywords)
    print("--------------------------------\n")
    
    results = search_grants(title, description, ds_keywords, client)
    #results = search_grants(title, description, merged_keywords, client)
    
    if len(description) > 500:
        description = description[:500] + "..."
    
    return render_template("results.html", results=results, title=title, description=description, keywords=ds_keywords)

if __name__ == "__main__":
    app.run(debug=True)
