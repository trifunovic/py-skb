import spacy

# Load the English language model
nlp = spacy.load("en_core_web_sm")

# Process a text
doc = nlp("Hello, world! This is a test sentence.")

# Print tokenized text with part-of-speech tags and dependencies
for token in doc:
    print(f"{token.text:10} {token.pos_:10} {token.dep_}")