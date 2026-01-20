
from app import validate_fasta

def test_validate_fasta_pass():
    assert validate_fasta(">seq1\nATCG") is True

def test_validate_fasta_empty():
    assert validate_fasta("") is False

def test_validate_fasta_fail_text():
    assert validate_fasta("hello") is False