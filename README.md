# AI Resume Parser – Simple Guide

This project is a small web app that helps you **analyse resumes automatically**.

You upload resumes, the app reads the text, looks for important skills, gives each candidate a score, and shows the results in easy charts.

The app runs in your browser using **Streamlit**.

---

## 1. What you need before starting

- Python 3.11 or newer installed on your system.
- Basic idea of how to open a terminal / command prompt.
- Internet connection (for installing Python libraries the first time).

You do **not** need deep machine learning knowledge to run this project.

---

## 2. Main Python libraries used (in simple words)

These are the tools the project relies on:

- **Streamlit**  
  Used to build the web UI. It creates the page, tabs, file upload buttons, sliders, and so on.

- **pandas**  
  Used to work with tables of data (one row per resume, with columns for scores and skills).

- **numpy**  
  Helps with numeric calculations and arrays.

- **NLTK (Natural Language Toolkit)**  
  Used to clean raw text:
  - split text into words
  - remove punctuation
  - remove common English words like *the*, *and*, *of* (called stopwords).

- **sentence-transformers**  
  Converts short text (like skill phrases) into numeric vectors (embeddings) so similar skills are close together. This is prepared for clustering and future improvements.

- **scikit‑learn**  
  Machine‑learning toolkit. Here it provides KMeans clustering for skills and can support more advanced analysis later.

- **plotly**  
  Draws interactive charts such as:
  - a histogram of scores
  - a radar chart comparing top candidates.

- **pdfplumber**  
  Reads text from PDF files so you can upload normal PDF resumes, not just `.txt` files.

All these are installed through `pip` (Python’s package manager).

---

## 3. Project files (what each file does)

- **`app.py`**  
  Main file. Runs the Streamlit app and defines three tabs:
  1. Upload Resumes  
  2. Analysis Dashboard  
  3. Batch CSV Processing

- **`preprocess.py`**  
  Functions to clean resume text and extract skills:
  - `clean_resume(text)` – cleans and normalizes the text.
  - `extract_skills(text)` – counts how often skills appear in four groups:
    - Python
    - Leadership
    - Web development
    - Data / analytics

- **`clustering.py`**  
  Functions for:
  - creating sentence embeddings using Sentence Transformers
  - grouping similar skills using KMeans (from scikit‑learn).  
  This is useful for more advanced analysis and future upgrades.

- **`scoring.py`**  
  Contains `score_candidate(resume_skills, job_skills, weights)`, which:
  - reads the skill counts from `extract_skills`
  - applies weights based on job importance
  - returns a final score out of 10 for each resume.

- **`requirements.txt`**  
  A plain text file listing all Python libraries needed to run the project.

You may also have a `sample_data/` folder with some example resumes and a demo CSV.

---

## 4. Step‑by‑step setup (first‑time only)

Follow these steps in order.

### Step 1 – Open the project folder

Place all project files in a folder, for example:

```
C:\Users\YourName\Desktop\AIPARSER
```

Open a terminal / command prompt in this folder.

### Step 2 – Create a virtual environment

Virtual environments keep this project’s libraries separate from other Python projects.

```
python -m venv .venv
```

Activate it:

```
# On Windows
.venv\Scripts\activate

# On macOS / Linux
source .venv/bin/activate
```

If activation worked, your terminal line will start with `(.venv)`.

### Step 3 – Install all required libraries

Run:

```
pip install --upgrade pip

pip install streamlit nltk scikit-learn pandas numpy \
            sentence-transformers plotly pdfplumber
```

This may take a few minutes the first time.

### Step 4 – Download NLTK language data

NLTK needs extra data files for tokenization and stopwords:

```
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

You only need to do this once on your machine.

---

## 5. How to run the app

Every time you want to use the app:

1. **Activate the virtual environment** (if not already active):

   ```
   # from the project folder
   .venv\Scripts\activate    # Windows
   # or
   source .venv/bin/activate # macOS / Linux
   ```

2. **Run the Streamlit app**:

   ```
   python -m streamlit run app.py
   ```

3. A browser tab should open automatically.  
   If not, open your browser and go to:

   ```
   http://localhost:8501
   ```

Now you are ready to use the interface.

---

## 6. How to use each tab in the app

### Tab 1 – Upload Resumes

- Click **“Upload resumes (.txt or .pdf)”**.
- Select one or more files:
  - `.txt` → plain text resumes
  - `.pdf` → text‑based PDFs (not scanned images)
- For each file:
  - If `.txt`, the app decodes the text and cleans it.
  - If `.pdf`, `pdfplumber` extracts the text from all pages.
- The app:
  - cleans the text using `clean_resume`
  - extracts skill counts using `extract_skills`
  - stores the results in session state.
- You will see a preview of the first resume’s text so you can check if parsing looks correct.

### Tab 2 – Analysis Dashboard

- On the left sidebar, set how important each area is:
  - Python
  - Leadership
  - Web development
  - Data analysis
- The app:
  - uses `score_candidate` to give each resume a score out of 10
  - displays:
    - best candidate score
    - average score
    - number of unique skill tags
    - number of resumes processed
    - a histogram of scores
    - a radar chart of the top 3 candidates
    - a table with one row per resume

This helps you quickly see who fits your needs best.

### Tab 3 – Batch CSV Processing

- Prepare a CSV file that has at least one column called `resume_text`.
- Go to the Batch tab and upload this CSV.
- The app:
  - applies the same cleaning and scoring logic to every row
  - adds a recommendation:
    - **Hire** – score ≥ 7  
    - **Review** – score between 5 and 7  
    - **Reject** – score < 5
- You can download the output as `resume_scores.csv`.

This is useful for running the model on larger datasets.

---

## 7. Requirements file (optional but recommended)

Create a file called `requirements.txt` with this content:

```
streamlit
nltk
scikit-learn
pandas
numpy
sentence-transformers
plotly
pdfplumber
```

Then, instead of installing libraries one by one, someone can simply run:

```
pip install -r requirements.txt
```

inside the virtual environment to get everything at once.

---

This README is designed so that a person who has basic Python installed, but no deep AI background, can:

1. Understand what the project does.  
2. Install all the right tools.  
3. Run the app.  
4. Explore the code if they want to learn more.
                                           
                                           Credits: Raunak Soni