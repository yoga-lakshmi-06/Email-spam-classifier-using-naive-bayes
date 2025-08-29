# 📧 SpamVision Pro – Email Spam Classifier

SpamVision Pro is a **machine learning-powered web application** built using **Flask** and **Naive Bayes / Logistic Regression** for detecting spam emails.  
It provides a **modern dashboard UI** with features like spam score, auto-reply suggestions, voice input, translations, log management, and export options.

---

## 🚀 Features
- 🔑 User authentication (Register / Login)
- 📤 Upload `.txt` or `.docx` email files
- 📨 Real-time spam classification with probability score
- 📊 Dashboard with charts and spam statistics
- 🗂 User history and searchable logs
- 🌗 Dark mode toggle
- 🗣 Voice-to-text input for emails
- 🌍 Translation support
- 📝 Auto-reply suggestions
- 📑 Export results to PDF / Excel

---

## 📂 Project Structure

```bash
spamvision_pro/
│── __pycache__/         # Python cache files (auto-generated)
│── exports/             # Folder where exported reports/logs are saved
│── static/              # CSS, JS, images (frontend static files)
│── templates/           # HTML templates (dashboard, login, register, logs, etc.)
│── uploads/             # Uploaded email/text files for classification
│── venv/                # Virtual environment (dependencies installed here)
│
│── app.py               # Main Flask application (routes, dashboard, spam detection logic)
│── auth.py              # Handles user authentication (login/register/session)
│── database.db          # SQLite database (stores users, logs, history)
│── requirements.txt     # List of dependencies (Flask, scikit-learn, etc.)
│── spam_dataset.csv     # Dataset used for training spam classifier
│── spam_model.pkl       # Trained ML model (Naive Bayes/Logistic Regression)
│── train_spam_model.py  # Script to train and save the model
│── vectorizer.pkl       # Saved text vectorizer (TF-IDF/CountVectorizer)
│
└── README.md            # Project documentation
```

---

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/spamvision_pro.git
   cd spamvision_pro
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # (Linux/Mac)
   venv\Scripts\activate      # (Windows)
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Train the model (if not already trained)**
   ```bash
   python train_spam_model.py
   ```

5. **Run the app**
   ```bash
   python app.py
   ```

6. Open your browser and go to:
   ```
   http://127.0.0.1:5000
   ```

---

## 📊 Tech Stack
- **Backend:** Flask, Flask-Login, Flask-SQLAlchemy
- **Frontend:** HTML, CSS, Jinja2, JavaScript
- **ML Model:** Naive Bayes / Logistic Regression (scikit-learn)
- **Database:** SQLite
- **Other:** Pandas, Matplotlib, ReportLab, OpenPyXL, SpeechRecognition, Translate

---

## 🧪 Example Output
- Spam score: **85%** → Classified as Spam  
- Spam score: **12%** → Classified as Ham  

---

## 📜 License
This project is licensed under the **MIT License**.

---

