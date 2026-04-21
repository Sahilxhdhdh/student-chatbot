import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ChatbotEngine:
    def __init__(self, intents_path):
        # Load intents
        with open(intents_path, "r", encoding="utf-8") as f:
            self.intents = json.load(f)["intents"]

        self.patterns = []
        self.tags = []

        # Extract patterns and tags
        for intent in self.intents:
            for pattern in intent["patterns"]:
                self.patterns.append(pattern.lower())
                self.tags.append(intent["tag"])

        # Train TF-IDF model
        self.vectorizer = TfidfVectorizer()
        self.X = self.vectorizer.fit_transform(self.patterns)

    # 🔍 Predict intent
    def predict_intent(self, text):
        text = text.lower().strip()

        # 🔥 Rule-based fix for greetings (IMPORTANT)
        if text in ["hi", "hello", "hey", "hii", "good morning", "good evening"]:
            return "greeting"

        vec = self.vectorizer.transform([text])
        similarity = cosine_similarity(vec, self.X)

        max_score = similarity.max()
        idx = similarity.argmax()

        # 🔥 Confidence threshold (prevents wrong matches)
        if max_score < 0.3:
            return "unknown"

        return self.tags[idx]

    # 💬 Generate response
    def respond(self, text, data):
        tag = self.predict_intent(text)

        # 👋 Greeting
        if tag == "greeting":
            name = data["student"]["name"]
            return {
                "message": f"Hey {name}! 👋 Great to see you. I can help with results, attendance, and fees."
            }

        # 📊 Results
        if tag == "results":
            return {
                "message": "📊 Fetching your results...",
                "action": "show_results"
            }

        # 📅 Attendance
        if tag == "attendance":
            return {
                "message": "📅 Checking your attendance...",
                "action": "show_attendance"
            }

        # 💰 Fees
        if tag == "fees":
            return {
                "message": "💰 Fetching your fee details...",
                "action": "show_fees"
            }

        # ❓ Unknown
        return {
            "message": "🤖 Sorry, I didn’t understand that. Try asking about results, attendance, or fees."
        }