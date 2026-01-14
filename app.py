from flask import Flask, render_template, request, redirect, url_for, flash
from Bio.Blast import NCBIWWW, NCBIXML
from Bio import SeqIO
from io import StringIO
import os, ssl, certifi

# Ensure HTTPS requests to NCBI use proper certificates (macOS can have issues)
ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
app = Flask(__name__)

# Load "SECRET_KEY" if provided, else use "dev" for local use
app.secret_key = os.environ.get("SECRET_KEY", "dev")

# Step 1: validate FASTA format using Biopython
def validate_fasta(text):
    try:
        handle = StringIO(text)
        record = list(SeqIO.parse(handle, "fasta"))
        return len(record) > 0

    except Exception:
        return False

# Main Route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # Text input from the form
        seq = request.form.get("sequence", "").strip()

        # Uploaded FASTA file
        file = request.files.get("fasta_file")
        file_text = ""
        if file and file.filename:
            file_text = file.read().decode("utf-8").strip()

        # Choose the input based on what the user provided
        final_seq = seq if seq else file_text

        # Long sequence error
        if len(final_seq) > 1000000:
            flash("Your sequence is too long for NCBI BLAST. Please submit one that is < 1,000,000 bases.")
            return redirect(url_for("index"))

        # Empty submission errors
        if not final_seq:
            flash("Please enter a sequence or upload a FASTA file.")
            return redirect(url_for("index"))

        # Validate FASTA before sending to NCBI
        if not validate_fasta(final_seq):
            flash("This sequence is invalid. Please try again.")
            return redirect(url_for("index"))

        # Submit BLAST request to NCBI (blastn against nt db). hitlist_size limits the number or returned hits
        results = NCBIWWW.qblast("blastn", "nt", final_seq, hitlist_size=10)
        blast_xml = results.read()

        # Debugging statement
        print("BLAST XML length:", len(blast_xml))

        # Parse XML
        blast_record = NCBIXML.read(StringIO(blast_xml))

        hits = []
        for alignment in blast_record.alignments:
            for hsp in alignment.hsps:
                percent_identity = (hsp.identities / hsp.align_length)

                hits.append({
                    "title": alignment.title,
                    "accession": alignment.accession,
                    "percent_identity": round(percent_identity, 2),
                    "alignment_length": hsp.align_length,
                    "evalue": hsp.expect
                })

        # Render results with parsed BLAST hits
        return render_template("results.html", hits=hits)

    # Render input form
    return render_template("index.html")

# App entry point
if __name__ == "__main__":
    app.run(debug=True)