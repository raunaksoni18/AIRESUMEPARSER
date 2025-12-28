import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

stop_words = set(stopwords.words('english'))

def clean_resume(text):
    """Clean and preprocess resume text."""
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    text = re.sub(r'\s+', ' ', text)
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if len(t) > 2 and t not in stop_words]
    return ' '.join(tokens)

def extract_skills(resume_text):
    """Extract key skills from cleaned text."""
    skills_keywords = {
        'python': ['python', 'pandas', 'numpy', 'sklearn', 'tensorflow'],
        'leadership': ['managed', 'team', 'supervised', 'led', 'coordinated'],
        'web': ['html', 'css', 'javascript', 'react', 'angular', 'node'],
        'data': ['sql', 'excel', 'tableau', 'powerbi', 'analytics']
    }
    
    cleaned = clean_resume(resume_text)
    skills = {}
    for category, keywords in skills_keywords.items():
        count = sum(1 for kw in keywords if kw in cleaned)
        if count > 0:
            skills[category] = count
    return skills
