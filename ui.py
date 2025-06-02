import streamlit as st
import PyPDF2
import re
import string
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import joblib
# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = reader.numPages
    content = ""
    for page_number in range(number_of_pages):
        page = reader.getPage(page_number)
        content += page.extractText()
    return content
try:
    #load the model
    model = joblib.load('resume_screening_model.pkl')
    # Function to preprocess text
    def preprocess_text(content):
        content = content.lower()
        content = re.sub(r'[0-9]+', '', content)
        content = content.translate(str.maketrans('', '', string.punctuation))
        return content

    # Function to calculate scores
    def calculate_scores(content):
        Area_with_key_term = {
            'Data science': ['algorithm', 'analytics', 'hadoop', 'machine learning', 'data mining', 'python',
                            'statistics', 'data', 'statistical analysis', 'data wrangling', 'algebra', 'Probability',
                            'visualization'],
            'Programming': ['python', 'r programming', 'sql', 'c++', 'scala', 'julia', 'tableau', 'javascript',
                            'powerbi', 'code', 'coding'],
            'Experience': ['project', 'years', 'company', 'excellency', 'promotion', 'award', 'outsourcing', 'work in progress'],
            'Management skill': ['administration', 'budget', 'cost', 'direction', 'feasibility analysis', 'finance', 
                                'leader', 'leadership', 'management', 'milestones', 'planning', 'problem', 'project', 
                                'risk', 'schedule', 'stakeholders', 'English'],
            'Data analytics': ['api', 'big data', 'clustering', 'code', 'coding', 'data', 'database', 'data mining', 
                            'data science', 'deep learning', 'hadoop', 'hypothesis test', 'machine learning', 'dbms', 
                            'modeling', 'nlp', 'predictive', 'text mining', 'visualization'],
            'Statistics': ['parameter', 'variable', 'ordinal', 'ratio', 'nominal', 'interval', 'descriptive', 
                            'inferential', 'linear', 'correlations', 'probability', 'regression', 'mean', 'variance', 
                            'standard deviation'],
            'Machine learning': ['supervised learning', 'unsupervised learning', 'ann', 'artificial neural network', 
                                'overfitting', 'computer vision', 'natural language processing', 'database'],
            'Data analyst': ['data collection', 'data cleaning', 'data processing', 'interpreting data', 
                            'streamlining data', 'visualizing data', 'statistics', 'tableau', 'tables', 'analytical'],
            'Software': ['django', 'cloud', 'gcp', 'aws', 'javascript', 'react', 'redux', 'es6', 'node.js', 
                        'typescript', 'html', 'css', 'ui', 'ci/cd', 'cashflow'],
            'Web skill': ['web design', 'branding', 'graphic design', 'seo', 'marketing', 'logo design', 'video editing', 
                        'es6', 'node.js', 'typescript', 'html/css', 'ci/cd'],
            'Personal Skill': ['leadership', 'team work', 'integrity', 'public speaking', 'team leadership', 
                                'problem solving', 'loyalty', 'quality', 'performance improvement', 'six sigma', 
                                'quality circles', 'quality tools', 'process improvement', 'capability analysis', 
                                'control'],
            'Accounting': ['communication', 'sales', 'sales process', 'solution selling', 'crm', 'sales management', 
                        'sales operations', 'marketing', 'direct sales', 'trends', 'b2b', 'marketing strategy', 
                        'saas', 'business development'],
            'Sales & marketing': ['retail', 'manufacture', 'corporate', 'goods sale', 'consumer', 'package', 'fmcg', 
                                'account', 'management', 'lead generation', 'cold calling', 'customer service', 
                                'inside sales', 'sales', 'promotion'],
            'Graphic': ['brand identity', 'editorial design', 'design', 'branding', 'logo design', 'letterhead design', 
                        'business card design', 'brand strategy', 'stationery design', 'graphic design', 'exhibition graphic design'],
            'Content skill': ['editing', 'creativity', 'content idea', 'problem solving', 'writer', 'content thinker', 
                            'copy editor', 'researchers', 'technology geek', 'public speaking', 'online marketing'],
            'Graphical content': ['photographer', 'videographer', 'graphic artist', 'copywriter', 'search engine optimization', 
                                'seo', 'social media', 'page insight', 'gain audience'],
            'Finanace': ['financial reporting', 'budgeting', 'forecasting', 'strong analytical thinking', 'financial planning', 
                        'payroll tax', 'accounting', 'productivity', 'reporting costs', 'balance sheet', 'financial statements'],
            'Health/Medical': ['abdominal surgery', 'laparoscopy', 'trauma surgery', 'adult intensive care', 'pain management', 
                            'cardiology', 'patient', 'surgery', 'hospital', 'healthcare', 'doctor', 'medicine'],
            'Language': ['english', 'malay', 'mandarin', 'bangla', 'hindi', 'tamil']
        }

        scores = {domain: sum(1 for word in terms if word in content) for domain, terms in Area_with_key_term.items()}
        return pd.DataFrame(list(scores.items()), columns=['Domain/Area', 'Score']).sort_values(by='Score', ascending=False)

    # Streamlit UI
    st.title('AI-Based Resume Screening')

    # Upload PDF
    uploaded_file = st.file_uploader("Upload a Resume (PDF)", type="pdf")

    if uploaded_file:
        # Extract text
        content = extract_text_from_pdf(uploaded_file)
        content = preprocess_text(content)

        # Calculate scores
        scored_df = calculate_scores(content)

        # Display scores
        st.subheader('Resume Score Breakdown by Domain')
        st.write(scored_df)

        # Visualization
        st.subheader('Resume Decomposition by Domain')
        fig, ax = plt.subplots()
        ax.pie(scored_df['Score'], labels=scored_df['Domain/Area'], autopct='%1.0f%%', shadow=True, startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

        # Analyze and recommend
        total_score = scored_df['Score'].sum()
        st.subheader('Recommendation')

        if total_score >= 50 and scored_df.loc[scored_df['Domain/Area'] == 'Personal Skill', 'Score'].values[0] >= 2 \
                and scored_df.loc[scored_df['Domain/Area'] == 'Language', 'Score'].values[0] >= 1 \
                and scored_df.loc[scored_df['Domain/Area'] == 'Statistics', 'Score'].values[0] >= 9:
            st.write("Status: Resume Meets The Requirement. Suggest To Recruit as Junior Data Scientist.")
        elif total_score >= 40 and scored_df.loc[scored_df['Domain/Area'] == 'Personal Skill', 'Score'].values[0] >= 2 \
                and scored_df.loc[scored_df['Domain/Area'] == 'Language', 'Score'].values[0] >= 1 \
                and scored_df.loc[scored_df['Domain/Area'] == 'Data science', 'Score'].values[0] >= 10:
            st.write("Status: Resume Meets The Requirement. Suggest To Recruit as Junior Data Scientist.")
        elif total_score >= 60 and scored_df.loc[scored_df['Domain/Area'] == 'Language', 'Score'].values[0] >= 1 \
                and scored_df.loc[scored_df['Domain/Area'] == 'Data analytics', 'Score'].values[0] >= 8:
            st.write("Status: Resume Meets The Requirement. Suggest To Recruit as Junior Data Scientist.")
        elif total_score >= 30 and scored_df.loc[scored_df['Domain/Area'] == 'Statistics', 'Score'].values[0] >= 2 \
                and scored_df.loc[scored_df['Domain/Area'] == 'Programming', 'Score'].values[0] >= 3 \
                and scored_df.loc[scored_df['Domain/Area'] == 'Personal Skill', 'Score'].values[0] >= 2 \
                and scored_df.loc[scored_df['Domain/Area'] == 'Language', 'Score'].values[0] >= 1 \
                and scored_df.loc[scored_df['Domain/Area'] == 'Data analytics', 'Score'].values[0] >= 5 \
                and scored_df.loc[scored_df['Domain/Area'] == 'Data analyst', 'Score'].values[0] >= 5:
            st.write("Status: Resume Meets The Requirement. Suggest To Recruit as Data Analyst.")
        elif total_score >= 20 and scored_df.loc[scored_df['Domain/Area'] == 'Experience', 'Score'].values[0] >= 2 \
                and scored_df.loc[scored_df['Domain/Area'] == 'Personal Skill', 'Score'].values[0] >= 2 \
                and scored_df.loc[scored_df['Domain/Area'] == 'Language', 'Score'].values[0] >= 1 \
                and scored_df.loc[scored_df['Domain/Area'] == 'Programming', 'Score'].values[0] >= 3 \
                and scored_df.loc[scored_df['Domain/Area'] == 'Data analytics', 'Score'].values[0] >= 5:
            st.write("Status: Resume Meets The Requirement. Suggest To Recruit as Data Analyst.")
        else:
            st.write("Status: Resume Does Not Meet The Requirement.")
except:
    st.write("Please check the uploaded file once again.")