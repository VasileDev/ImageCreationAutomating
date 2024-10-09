import pdfplumber
import os
import re

def extract_text(pdf_path: str) -> list:
    with pdfplumber.open(pdf_path) as pdf:
        pages = []
        for page in pdf.pages:
            text = page.extract_text()  # Extract all text from the page    
            pages.append(text)
    return pages

pdf_path = "100factspdf.pdf"
pages = extract_text(pdf_path)

# removing the last page (it doesn't contain facts)
del pages[-1]

refined_facts = []
for i in range(len(pages)):
    # Split sentences by number + point + space pattern, ex: "86. "
    sentences = re.split(r'\d+\. ', pages[i])
    for j in range(len(sentences)):
        # Replacing any kind of spaces with regular spaces
        sentences[j] = re.sub(r'\s+', ' ', sentences[j])
        # Removing numerotation of pages, ex: "Page 8 of 49"
        sentences[j] = re.sub(r'Page \d+ of \d+', '', sentences[j])
        refined_facts.append(str(sentences[j]))

# Getting rid of the chapter title
final_list = []
for elem in refined_facts:
    if "Untitled " in elem:
        continue
    else:
        final_list.append(elem)

# Writing the facts inside text files
facts_number = len(final_list)
if not os.path.exists("completed_facts"):
    os.makedirs("completed_facts")
os.chdir("completed_facts")
for i in range(facts_number):
    with open(f"fact{i}.txt", 'w', encoding="utf-8") as f_obj:
        f_obj.write(final_list[i])