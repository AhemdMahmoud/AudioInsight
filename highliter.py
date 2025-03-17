from gliner import GLiNER
import spacy
from spacy.tokens import Doc, Span
from spacy import displacy

# Load the GLiNER model
model = GLiNER.from_pretrained("urchade/gliner_multi-v2.1")

# Input text
text = input("Input text: ")
# nlp=spacy.load("en_core_web_sm")

# Labels for entity extraction
labels = ["person", "organization", "location", "date", "event", "award", "teams", "competitions","percent","Time","currency","Fac","quantity","UNIT","law","DATE"]
#nlp.pipe_labels['ner']

# Predict entities
entities = model.predict_entities(text, labels)
for entity in entities:
    print(entity["text"], "=>", entity["label"])

# Load the spaCy model
nlp = spacy.blank("ar")

# Tokenize the text using spaCy
doc = nlp(text)

# Create a list to hold the Span objects
entities_2 = []

# Iterate over the predicted entities and create Span objects
for entity in entities:
    start = entity["start"]
    end = entity["end"]
    label = entity["label"]
    span = doc.char_span(start, end, label=label)
    if span is not None:
        entities_2.append(span)

# Assign the entities to the doc.ents attribute
doc.ents = entities_2

# Render the entities with displacy
# displacy.serve(doc, style="ent")

html = displacy.render(doc, style="ent", page=True)
with open("entities.html", "w", encoding="utf-8") as f:
    f.write(html)

