import json
import logging
import time
import traceback

from dotenv import load_dotenv
load_dotenv()


def format_reply(text):
    """تنسيق الرد بشكل بسيط"""
    if not text:
        return text
    # استبدال النقاط بأسطر جديدة
    text = text.replace('. ', '.\n')
    text = text.replace('، ', '،\n')
    # إضافة سطر فارغ قبل كل فرصة
    import re
    text = re.sub(r'(\d+\.)', r'\n\1', text)
    return text


from flask import Flask, render_template, request, jsonify
from config import Config
from services.data_service import search_opportunities, get_context
from services.llm_service import get_bot_response

logging.basicConfig(
    filename=Config.LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()
        
        if not user_message:
            return jsonify({"reply": "الرجاء كتابة سؤال."})
        
        opportunities = search_opportunities(user_message)
        context = get_context(opportunities)
        reply = get_bot_response(user_message, context)
        
        return jsonify({"reply": reply})
    
    except Exception as e:
        return jsonify({"reply": f"عذراً، حدث خطأ: {str(e)}"})


if __name__ == "__main__":
    app.run(debug=True)
