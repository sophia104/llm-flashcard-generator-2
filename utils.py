import PyPDF2
import os
import json

def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def read_text(file):
    return file.read().decode('utf-8')

def export_to_csv(flashcards, filename):
    import csv
    keys = flashcards[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(flashcards)

def export_to_json(flashcards, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(flashcards, f, indent=4)
