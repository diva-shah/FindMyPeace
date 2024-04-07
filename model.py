import nltk
import random
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from textblob import TextBlob

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

def generate_statements():
    # Templates for generating statements
    sad_templates = ["I feel sad because {}.",
                    "{} makes me feel sad.",
                    "When {}, I feel sad.",
                    "I'm feeling sad because of {}."]

    anxious_templates = ["I feel anxious because {}.",
                        "{} makes me feel anxious.",
                        "When {}, I feel anxious.",
                        "I'm feeling anxious because of {}."]

    stressed_templates = ["I feel stressed because {}.",
                        "{} makes me feel stressed.",
                        "When {}, I feel stressed.",
                        "I'm feeling stressed because of {}."]

    angry_templates = ["I feel angry because {}.",
                    "{} makes me feel angry.",
                    "When {}, I feel angry.",
                    "I'm feeling angry because of {}."]

    # Words related to each emotion
    sad_words = ["loss", "loneliness", "grief", "heartbreak", "tears", "unhappy", "depressed"]
    anxious_words = ["worry", "fear", "nervousness", "tension", "apprehension", "panic", "uneasy"]
    stressed_words = ["pressure", "overwhelmed", "burnout", "tense", "strain", "stressful", "anxious"]
    angry_words = ["rage", "irritation", "frustration", "outrage", "anger", "resentment", "annoyance"]

    # Initialize sets to store generated statements
    sad_set = set()
    anxious_set = set()
    stressed_set = set()
    angry_set = set()

    # Generate statements for each emotion, ensuring no repetitions
    while len(sad_set) < 10:
        statement = random.choice(sad_templates).format(random.choice(sad_words))
        if "harm" not in statement and "suicide" not in statement:
            sad_set.add(statement)
    
    while len(anxious_set) < 10:
        statement = random.choice(anxious_templates).format(random.choice(anxious_words))
        if "harm" not in statement and "suicide" not in statement:
            anxious_set.add(statement)
    while len(stressed_set) < 10:
        statement = random.choice(stressed_templates).format(random.choice(stressed_words))
        if "harm" not in statement and "suicide" not in statement:
            stressed_set.add(statement)
    while len(angry_set) < 10:
        statement = random.choice(angry_templates).format(random.choice(angry_words))
        if "harm" not in statement and "suicide" not in statement:
            angry_set.add(statement)

    # Combine statements with labels for classification
    data_with_statements = [(statement, "sad") for statement in sad_set] + \
                           [(statement, "anxious") for statement in anxious_set] + \
                           [(statement, "stressed") for statement in stressed_set] + \
                           [(statement, "angry") for statement in angry_set]

    # Prompt the user if they want to add their own query
    add_query = input("Do you want to add your own query? (yes/no): ")

    # If the user wants to add their own query, prompt for it and add it to the dataset
    if add_query.lower() == "yes":
        user_query = input("Enter your query: ")
        data_with_statements.append((user_query, "query"))

    return data_with_statements


def train_classifier(data):
    # Preprocessing
    stop_words = set(stopwords.words('english'))
    preprocessed_data = []
    for text, emotion in data:
        words = nltk.word_tokenize(text.lower())
        filtered_words = [word for word in words if word.isalpha() and word not in stop_words]
        preprocessed_data.append((" ".join(filtered_words), emotion))

    # Feature extraction
    X, y = zip(*preprocessed_data)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(X)

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Random Forest classifier
    classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    classifier.fit(X_train, y_train)

    # Predictions
    y_pred = classifier.predict(X_test)

    # Evaluation
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)

    # Print confusion matrix and classification report
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))


def main():
    # Generate statements and prompt user for query
    data_with_statements = generate_statements()

    # Train classifier and evaluate
    train_classifier(data_with_statements)


if __name__ == "__main__":
    main()


