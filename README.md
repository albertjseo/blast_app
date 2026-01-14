# BLAST Web App
A Flask application for validating FASTA sequences and directly running NCBI BLAST searches within a browser.

 <img src="https://img.shields.io/badge/Language-Python-blue.svg" style="zoom:100%;" /> <img src="https://img.shields.io/badge/Language-HTML-orange.svg" style="zoom:100%;" /> <img src="https://img.shields.io/badge/Skill-Jinja-red.svg" style="zoom:100%;" /> <img src="https://img.shields.io/badge/Skill-Flask-purple.svg" style="zoom:100%;" />

---
## Context
This project was developed with the goal of:

- Accepting a DNA sequence via a text field or uploaded FASTA file
- Validating the inputs as a valid FASTA format
- Use **NCBI BLAST** to identify the species of origin for the provided DNA sequence
- Displaying the BLAST results as a simple and readable table

---
## Project Overview

This project provides a simple web interface for submitting DNA sequences to NCBI BLAST. 
Users can either paste a FASTA sequence or upload a `.fasta`/`.fa` file. 
The app validates the input, sends the sequence to NCBI’s BLAST API, parses the XML response, and displays the results in a clean, 
Bootstrap‑styled table.

The goal of this project is to offer a simple and easy‑to‑run BLAST client. To accomplish this, the application uses a modular structure 
that can be extended with additional BLAST parameters, tool sets, and other routes without requiring major refactoring. 

---
## Directory Structure  
```
blast-app/
│
├── app.py                   # Main Flask application
├── README.md                # Project documentation
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (optional)
├── .gitignore               # Git ignore rules
│
├── templates/
│   ├── base.html            # Shared layout
│   ├── index.html           # Input form
│   └── results.html         # BLAST results table
│
├── test_seq/                # Example FASTA files
│   ├── NC_003909.8.fasta
│   └── NC_009085.1.fasta
│
├── test_validate.py         # Pytest for FASTA validation
│
└── venv/                    # Virtual environment (not included in repo)

```
---
## Running the App Locally

### 1. Clone the Repository
```bash
git clone https://github.com/albertjseo/blast_app.git
cd blast_app
```
### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Flask App
```bash
python app.py
```

### 5. Open the App in your Browser
> http://127.0.0.1:5000

### 6. Input your Sequence Text / FASTA file and "Run BLAST"

---

## Unit Testing
### Run the Pytest from Project Root
**Assuming that the virtual environment is active and all requirements have been installed**
```bash
pytest
```

---
## Assumptions Made:
- I assumed submitted sequences would be relatively small
- While Biopython handles validation, I assumed users would submit valid or near-valid FASTA rather than random text
- I assumed that users did not need advanced BLAST configurations
- I assumed users would not require more BLAST hits than the configured hitlist_size to help keep BLAST responses small and results rendering fast