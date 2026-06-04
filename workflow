┌─────────────────────┐
│      User Opens     │
│      Website        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Fill Student Details│
│ Name                │
│ CGPA                │
│ Branch              │
│ Target Company      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Upload Resume (PDF) │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Flask Receives Form │
│ Data + Resume       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Save Resume in      │
│ Uploads Folder      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Extract Resume Text │
│ using pdfplumber    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Skill Detection     │
│ Python, Java, SQL,  │
│ ML, AI, etc.        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Store Student Data  │
│ in MySQL Database   │
│ (students table)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Create AI Prompt    │
│ Resume + Skills +   │
│ Company + CGPA      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Gemini API          │
│ Analysis            │
└──────────┬──────────┘
           │
           ▼
┌────────────────────────────────┐
│ Generate Recruiter Feedback    │
│ Strengths                      │
│ Weaknesses                     │
│ Hiring Opinion                 │
└──────────┬─────────────────────┘
           │
           ▼
┌────────────────────────────────┐
│ Generate Personalized Roadmap  │
│ Skills to Learn                │
│ Projects to Build              │
│ Improvement Plan               │
└──────────┬─────────────────────┘
           │
           ▼
┌─────────────────────┐
│ Calculate Company   │
│ Fit Score           │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Display Results     │
│ Fit Score           │
│ Skills Found        │
│ Recruiter Feedback  │
│ AI Roadmap          │
└─────────────────────┘
