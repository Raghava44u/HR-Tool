from flask import Flask, render_template, request, send_file
import spacy
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import csv
import os

app = Flask(__name__)

nlp = spacy.load("en_core_web_sm")

global_results = []

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

def extract_entities(text):
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    name_matches = re.findall(r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b', text)

    names = name_matches if name_matches else ["N/A"]
    emails = emails if emails else ["N/A"]

    return emails, names


@app.route('/', methods=['GET', 'POST'])
def index():
    global global_results
    global_results = []

    if request.method == 'POST':
        job_description = request.form['job_description']
        resume_files = request.files.getlist('resume_files')

        if not os.path.exists("uploads"):
            os.makedirs("uploads")

        processed_resumes = []
        for resume_file in resume_files:
            resume_path = os.path.join("uploads", resume_file.filename)
            resume_file.save(resume_path)

            resume_text = extract_text_from_pdf(resume_path)
            emails, names = extract_entities(resume_text)
            processed_resumes.append((names, emails, resume_text))

        # TF-IDF vectorizer
        tfidf_vectorizer = TfidfVectorizer()
        job_desc_vector = tfidf_vectorizer.fit_transform([job_description])

        shortlisted_cand = []
        for (names, emails, resume_text) in processed_resumes:
            resume_vector = tfidf_vectorizer.transform([resume_text])
            similarity = cosine_similarity(job_desc_vector, resume_vector)[0][0] * 100 
            shortlisted_cand.append((names, emails, similarity))

        shortlisted_cand.sort(key=lambda x: x[2], reverse=True)

        global_results = shortlisted_cand
    return render_template('index.html', results=global_results)

@app.route('/download_csv')
def download_csv():
    if not global_results:
        return "No data to download", 400

    csv_filename = "shortlisted_cand.csv"
    csv_full_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), csv_filename)

    with open(csv_full_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Rank", "Name", "Email", "Similarity"])
        
        for rank, (names, emails, similarity) in enumerate(global_results, start=1):
            name = names[0] if names else "N/A"
            email = emails[0] if emails else "N/A"
            writer.writerow([rank, name, email, similarity])

    return send_file(csv_full_path, as_attachment=True, download_name="shortlisted_cand.csv")

if __name__ == '__main__':
    app.run(debug=True)
