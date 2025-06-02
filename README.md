# AI-Resume-Tracking
AI-Based Resume Screening App
This Streamlit app automatically analyzes and scores resumes (PDFs) across multiple skill domains (e.g., Data Science, Programming, Statistics) using keyword-based NLP techniques. It visualizes domain relevance and suggests suitable roles like Junior Data Scientist or Data Analyst based on predefined criteria.

🔍 Key Features
📥 Upload and analyze resumes in PDF format
🧠 Keyword-based content classification across 20+ skill domains
📊 Score breakdown and interactive pie chart visualization
🧾 Pre-trained model for intelligent domain analysis
📝 Role suitability recommendations based on scoring thresholds
🧼 Built-in preprocessing (case normalization, punctuation/number removal)
📉 Fallback mechanism for low-quality or incompatible PDFs

🛠 Technologies Used
Python
Streamlit (for interactive UI)
PyPDF2 (for PDF text extraction)
Pandas (for data processing)
Matplotlib (for pie chart visualization)
Joblib (for loading the pre-trained ML model)
Regex & String Processing (for resume content preprocessing)

📚 Skill Domains Covered
The resume is scanned for keywords in domains including but not limited to:
Data Science
Programming
Data Analytics
Statistics
Machine Learning
Software & Web Skills
Personal & Management Skills
Finance, Sales & Marketing
Graphic Design & Content Creation
Healthcare & Languages

✅ Recommendation Logic
Based on keyword match scores in key domains and total scores, the app suggests:
Junior Data Scientist
Data Analyst
Or flags the resume as not meeting requirements
Criteria are based on combinations of scores in statistics, language, personal skills, and technical keywords.


