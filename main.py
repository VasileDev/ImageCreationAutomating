from PIL import Image, ImageDraw, ImageFont
import requests
import os
import spacy

# Ensure the model is downloaded and load the SpaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Open the backgrund image
background = Image.open("background.png")

font = ImageFont.truetype("arial.ttf", 33)
text_color = (255, 255, 255)
fact_pos = (1020 // 7, 234)
fact_file_list = os.listdir("completed_facts")

def read_fact(file_name:str) -> str:
    file_object = open(file_name, 'r')
    text = file_object.read()
    file_object.close()
    return text

def arrange_text(text:str)->str:
    fact = ''
    i = 0
    # Max chars for a line: 50
    new_line = 50
    for char in text:
        i += 1
        fact = fact + char
        if i >= new_line and char == ' ':
            fact += "\n"
            new_line += 50
    return fact

def get_main_entity(doc):
    # Initialize variables to store subjects and named entities
    subjects = []
    named_entities = []
    
    # Iterate through the tokens in the sentence
    for token in doc:
        if token.dep_ in ('nsubj', 'nsubjpass'):
            subjects.append(token)
    
    # Collect all named entities
    for ent in doc.ents:
        if ent.label_ in ('PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LANGUAGE'):
            named_entities.append(ent)
    
    # Prioritize named entities that are subjects
    for subject in subjects:
        for ent in named_entities:
            if subject in ent:
                return ent.text
    
    # If no subjects are named entities, prioritize the most significant named entity
    if named_entities:
        return named_entities[0].text  # Return the first named entity
    
    # If no named entities, return the most significant noun chunk
    if subjects:
        return subjects[0].text
    
    noun_chunks = list(doc.noun_chunks)
    if noun_chunks:
        return noun_chunks[-1].text  # Return the last noun chunk as a fallback
    return None

def fetch_pexels_images(query, num_images=10, orientation='landscape'):
    # Read API key from the file
    root = os.getcwd()
    api_file_name = os.path.join(root, "pexels_api_key.txt")
    with open(api_file_name, 'r') as api_file_obj:
        api_key = api_file_obj.read().strip()

    base_url = "https://api.pexels.com/v1/"
    headers = {'Authorization': api_key}
    params = {
        'query': query,
        'per_page': num_images,
        'orientation': orientation
    }

    # Send API request to fetch images
    response = requests.get(base_url + 'search', headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        image_urls = [photo['src']['original'] for photo in data['photos']]
        return image_urls
    else:
        print("Failed to fetch the images: ", response.status_code)
        return []

for file in fact_file_list:
    # Make the background drawable
    drawOnBackground = ImageDraw.Draw(background)
    text = read_fact(f"completed_facts/{file}")
    fact = arrange_text(text)   
    # Draw wtermark
    drawOnBackground.text((73, 66), text="@smart.factz", fill=text_color, font=font)
    # Draw fact
    drawOnBackground.text(fact_pos, text=fact, fill=text_color, font=font)
    # Get the subject of the fact
    doc = nlp(text)
    main_entity = get_main_entity(doc)
    # Download an image matching the subject
    api_file_name = "pexels_api_key.txt"
    with open(api_file_name, 'r') as api_file_obj:
        api_key = api_file_obj.read().strip()  # Strip any extra whitespace/newlines

    pexels_api = PexelsAPI(api_key)
    # background.paste(save_button, (972, 66))




background.save(f"imgaaaaage_image.png")
