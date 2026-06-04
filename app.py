
from flask import Flask, render_template, request
import pymysql
import os
import pdfplumber
import google.generativeai as genai

app = Flask(__name__)
# ==========================
# GEMINI CONFIGURATION
# ==========================

GEMINI_API_KEY = "AQ.Ab8RN6LmKdLHqF4YYHVg4XPgb7MSef2jFQbmRiArBfkiAPUj2w"

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    "gemini-2.0-flash"
)

# ==========================
# UPLOAD FOLDER
# ==========================

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==========================
# MYSQL CONNECTION
# ==========================

db = pymysql.connect(
    host="mysql.railway.internal",
    user="root",
    password="eAVFFDorrmWfoUIflnaSphpJZxTYWfeN",
    database="railway",
    port=3306
)

cursor = db.cursor()

# ==========================
# COMPANY REQUIREMENTS
# ==========================

company_requirements = {

    "Amazon": [
        "python",
        "dsa",
        "oop",
        "problem solving"
    ],

    "Microsoft": [
        "python",
        "dsa",
        "system design",
        "oop"
    ],

    "Infosys": [
        "python",
        "sql",
        "communication"
    ],

    "TCS Digital": [
        "java",
        "python",
        "sql",
        "dbms"
    ],

    "Accenture": [
        "communication",
        "problem solving",
        "sql"
    ]
}
# ==========================
# RECOMMENDATION BANK
# ==========================
recommendation_bank = {

    "Amazon": [
        "Master Data Structures and Algorithms",
        "Solve 150+ LeetCode problems",
        "Strengthen OOP concepts",
        "Build Flask or Spring Boot projects"
    ],

    "Microsoft": [
        "Practice DSA extensively",
        "Learn System Design basics",
        "Improve problem solving speed",
        "Contribute to open source projects"
    ],

    "Infosys": [
        "Improve DBMS knowledge",
        "Practice SQL queries",
        "Strengthen communication skills",
        "Build one full-stack project"
    ],

    "TCS Digital": [
        "Practice Java programming",
        "Revise DBMS concepts",
        "Improve aptitude skills",
        "Build mini projects"
    ],

    "Accenture": [
        "Improve communication skills",
        "Practice aptitude questions",
        "Learn SQL fundamentals",
        "Develop teamwork skills"
    ]
}

# ==========================
# KNOWN SKILLS
# ==========================

known_skills = [

    "python",
    "java",
    "c",
    "c++",
    "javascript",

    "html",
    "css",
    "react",
    "nodejs",
    "express",

    "flask",
    "django",

    "mysql",
    "sql",
    "mongodb",
    "dbms",

    "oop",

    "data structures",
    "algorithms",
    "dsa",

    "machine learning",
    "deep learning",
    "artificial intelligence",

    "communication",
    "leadership",
    "teamwork",

    "problem solving",
    "system design",

    "git",
    "github"
]

# ==========================
# HOME
# ==========================

@app.route('/')
def home():
    return render_template('index.html')


# ==========================
# ANALYZE
# ==========================

@app.route('/analyze', methods=['POST'])
def analyze():

    name = request.form['name']
    cgpa = request.form['cgpa']
    branch = request.form['branch']
    company = request.form['company']

    manual_skills = request.form.get('skills', '')

    resume = request.files.get('resume')

    detected_skills = []
    resume_text = ""
    resume_path = ""

    # ==========================
    # SAVE RESUME
    # ==========================

    if resume and resume.filename:

        resume_path = os.path.join(
            UPLOAD_FOLDER,
            resume.filename
        )

        resume.save(resume_path)

        try:

            with pdfplumber.open(resume_path) as pdf:

                for page in pdf.pages:

                    page_text = page.extract_text()

                    if page_text:
                        resume_text += page_text.lower()

        except Exception:
            resume_text = ""

    # ==========================
    # AUTO DETECT SKILLS
    # ==========================

    for skill in known_skills:

        if skill in resume_text:
            detected_skills.append(skill)

    # ==========================
    # MANUAL SKILLS
    # ==========================

    if manual_skills.strip():

        manual_skill_list = [
            skill.strip().lower()
            for skill in manual_skills.split(',')
        ]

        for skill in manual_skill_list:

            if skill not in detected_skills:
                detected_skills.append(skill)

    # ==========================
    # STORE IN MYSQL
    # ==========================

    insert_query = """
    INSERT INTO students
    (name, cgpa, branch, company_name, resume_path)
    VALUES (%s,%s,%s,%s,%s)
    """

    cursor.execute(
        insert_query,
        (
            name,
            cgpa,
            branch,
            company,
            resume_path
        )
    )

    db.commit()

    # ==========================
    # TARGET COMPANY ANALYSIS
    # ==========================

    required_skills = company_requirements.get(
        company,
        []
    )

    matched = []
    missing = []

    for skill in required_skills:

        if skill.lower() in detected_skills:
            matched.append(skill)
        else:
            missing.append(skill)

    # ==========================
    # IMPROVED FIT SCORE
    # ==========================

    skill_score = (
        len(matched) / len(required_skills)
    ) * 60

    cgpa_score = (
        float(cgpa) / 10
    ) * 30

    profile_score = 10 if len(detected_skills) >= 5 else 5

    fit_score = int(
        skill_score +
        cgpa_score +
        profile_score
    )

    if fit_score > 100:
        fit_score = 100

    # ==========================
    # COMPANY COMPARISON
    # ==========================

    all_scores = {}

    for company_name, req_skills in company_requirements.items():

        match_count = 0

        for skill in req_skills:

            if skill.lower() in detected_skills:
                match_count += 1

        score = int(
            (match_count / len(req_skills))
            * 100
        )

        all_scores[company_name] = score

    # ==========================
    # BEST COMPANY MATCH
    # ==========================

    best_company = max(
        all_scores,
        key=all_scores.get
    )

    best_score = all_scores[best_company]

    # ==========================
    # PLACEMENT VERDICT
    # ==========================

    if fit_score >= 80:
        placement_verdict = "Excellent Placement Readiness"

    elif fit_score >= 60:
        placement_verdict = "Good Placement Readiness"

    elif fit_score >= 40:
        placement_verdict = "Moderate Placement Readiness"

    else:
        placement_verdict = "Needs Improvement"

    # ==========================
    # RECRUITER FEEDBACK
    # ==========================

    if missing:

        recruiter_feedback = (
            f"{name} demonstrates strong academic potential "
            f"with a CGPA of {cgpa}. "
            f"The profile currently matches "
            f"{len(matched)} out of {len(required_skills)} "
            f"key requirements for {company}. "
            f"Focus on improving: "
            f"{', '.join(missing)}."
        )

    else:

        recruiter_feedback = (
            f"{name} is strongly aligned with "
            f"{company} requirements and demonstrates "
            f"excellent placement readiness."
        )

    # ==========================
    # RECOMMENDATIONS
    # ==========================

    recommendations = recommendation_bank.get(
        company,
        []
    )
    # ==========================
    # GEMINI FEEDBACK
    # ==========================

    try:

        prompt = f"""
        You are an HR recruiter.

        Student Name: {name}
        CGPA: {cgpa}
        Branch: {branch}

        Skills:
        {', '.join(detected_skills)}

        Target Company:
        {company}

        Missing Skills:
        {', '.join(missing)}

        Give recruiter feedback,
        strengths,
        weaknesses,
        and suggestions.

        Maximum 150 words.
        """

        response = model.generate_content(prompt)

        recruiter_feedback = response.text

    except Exception as e:

        recruiter_feedback = f"ERROR: {str(e)}"

    # ==========================
    # GEMINI ROADMAP
    # ==========================

    try:

        roadmap_prompt = f"""
        Create a 4 week roadmap.

        Target Company:
        {company}

        Current Skills:
        {', '.join(detected_skills)}

        Missing Skills:
        {', '.join(missing)}

        Format:

        Week 1:
        Week 2:
        Week 3:
        Week 4:
        """

        roadmap_response = model.generate_content(
            roadmap_prompt
        )

        ai_roadmap = roadmap_response.text

    except Exception as e:

        ai_roadmap = f"ERROR: {str(e)}"

    return render_template(
        'results.html',

        name=name,
        cgpa=cgpa,
        branch=branch,
        company=company,

        fit_score=fit_score,

        matched=matched,
        missing=missing,

        all_scores=all_scores,

        detected_skills=detected_skills,

        recommendations=recommendations,

        recruiter_feedback=recruiter_feedback,
        ai_roadmap=ai_roadmap,

        best_company=best_company,
        best_score=best_score,

        placement_verdict=placement_verdict
    )
# ==========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
