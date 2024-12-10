import spacy
from nltk.stem import PorterStemmer
from spacy.matcher import PhraseMatcher

def analyze_dass21_symptoms(input_text):
    # Initialize spaCy and NLTK components
    nlp = spacy.load("en_core_web_sm")
    ps = PorterStemmer()

    # Define the DASS-21 categories and associated keywords
    DASS21_KEYWORDS = {
        "Depression": ["downhearted", "blue", "positive feelings", "meaningless", "disheartened",
                       "not worth", "worth nothing", "worthless", "unable", "nothing", "couldn't",
                       "hopeless"],
        "Anxiety": ["trembling", "scared", "scary", "panic", "panicked", "panicking", "absence", "worried",
                    "dryness", "drying", "breathe", "breathing"],
        "Stress": ["hard", "agitated", "agitating", "agitatedly", "difficult", "nervous", "nervously", "nervousness",
                   "overreact", "overreacting", "overreacted", "frustrating", "frustrated"]
    }

    # Convert keywords to lemmatized and stemmed forms
    def preprocess_keywords(keywords):
        processed_keywords = set()
        for keyword in keywords:
            tokens = nlp(keyword)
            for token in tokens:
                lemmatized = token.lemma_
                stemmed = ps.stem(lemmatized)
                processed_keywords.add(lemmatized)
                processed_keywords.add(stemmed)
        return list(processed_keywords)

    # Preprocess all keywords
    PROCESSED_DASS21_KEYWORDS = {
        category: preprocess_keywords(keywords) for category, keywords in DASS21_KEYWORDS.items()
    }

    # Phrase matcher for multi-word phrases
    def build_phrase_matcher(keywords):
        matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        for phrase in keywords:
            matcher.add(phrase, [nlp(phrase)])
        return matcher

    PHRASE_MATCHERS = {category: build_phrase_matcher(keywords) for category, keywords in DASS21_KEYWORDS.items()}

    # Negation detection
    def has_negation(token):
        negations = {"not", "no", "never", "n't"}
        return any(tok.text.lower() in negations for tok in token.lefts)

    # Analyze input text
    doc = nlp(input_text.lower())
    matched_symptoms = {"Depression": [], "Anxiety": [], "Stress": []}

    for category, keywords in PROCESSED_DASS21_KEYWORDS.items():
        # Check for lemma or stem matches
        for token in doc:
            lemma = token.lemma_
            stem = ps.stem(lemma)
            if lemma in keywords or stem in keywords:
                if not has_negation(token):
                    matched_symptoms[category].append(token.text)

    # Phrase matching
    for category, matcher in PHRASE_MATCHERS.items():
        matches = matcher(doc)
        for _, start, end in matches:
            phrase = doc[start:end].text
            matched_symptoms[category].append(phrase)

    # Count symptoms
    symptom_counts = {category: len(set(symptoms)) for category, symptoms in matched_symptoms.items()}

    # Return the results
    return {
        "matched_symptoms": matched_symptoms,
        "symptom_counts": symptom_counts
    }

# Example Input
user_input = """
I feel so hopeless and worthless lately.
I also get nervous when thinking about the future and feel very frustrated at work.
I am not nervous about small things.
"""

# Analyze Symptoms
results = analyze_dass21_symptoms(user_input)

# Output Results
print("Matched Symptoms:", results["matched_symptoms"])
print("Symptom Counts:", results["symptom_counts"])