# train_spam_model.py
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import pickle

# Example dataset
data = {
    "text": [
        "Congratulations! You won a free ticket",
        "Please review the attached document",
        "Win money now!!!",
        "Meeting at 10 AM tomorrow",
        "Claim your prize by clicking this link",
        "Project deadline is next week"
    ],
    "label": [1, 0, 1, 0, 1, 0]  # 1 = spam, 0 = ham
}

df = pd.DataFrame(data)

# Convert text to numerical features
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df["text"])
y = df["label"]

# Train the model
model = MultinomialNB()
model.fit(X, y)

# Save the model
with open("spam_model.pkl", "wb") as f:
    pickle.dump(model, f)

# Save the vectorizer
with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("✅ Model and vectorizer saved successfully!")
