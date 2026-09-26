from flask import Flask, render_template, request, jsonify
from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL

app = Flask(__name__)
client = genai.Client(api_key=GEMINI_API_KEY)

FITNESS_PROMPT = """
You are Fitness Assistant, a fitness and wellness information chatbot.
Answer ONLY questions related to fitness and closely related topics:
workouts, exercise, strength training, cardio, stretching, mobility,
warm-ups, cool-downs, flexibility, endurance, muscle building, fat loss,
general fitness routines, gym training, home workouts, sports conditioning,
recovery, sleep for fitness, hydration, and general nutrition for fitness.
Do not provide diagnosis, medical treatment, or prescription advice. For
injuries, serious symptoms, or medical conditions, recommend consulting a
qualified healthcare professional.
If the user asks about software, programming, web development, electronics,
agriculture, sports news/results, politics, movies, or any unrelated topic,
reply exactly: "Sorry, I can answer only fitness and wellness-related questions."
Keep answers clear, practical, beginner-friendly, and safety-focused.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data received."}), 400
        user_message = data.get("message", "").strip()
        if not user_message:
            return jsonify({"success": False, "error": "Please enter a message."}), 400
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=f"{FITNESS_PROMPT}\n\nUser question:\n{user_message}"
        )
        return jsonify({"success": True, "reply": response.text})
    except Exception as e:
        print("ERROR:", repr(e))
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
