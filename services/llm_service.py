import google.genai as genai
from config import Config

SYSTEM_PROMPT = """أنت مساعد ذكي في منصة "فرص خضراء". قواعد الرد:
1. استخدم العربية الفصحى.
2. اذكر الفرص بشكل واضح مع التفاصيل المهمة.
3. إذا سأل المستخدم عن منح/وظائف/تدريب، ركز على ما يطلبه.
4. عند عرض الفرص، اكتب كل فرصة في سطر جديد مع تفاصيلها.

الفرص المتاحة:
{context}"""


def _get_client():
    return genai.Client(api_key=Config.GEMINI_API_KEY)


def get_bot_response(user_message: str, context: str) -> str:
    if not Config.GEMINI_API_KEY or Config.GEMINI_API_KEY == "your_api_key_here":
        return "⚠️ لم يتم تعيين مفتاح Gemini API. يرجى إضافته في ملف .env"

    try:
        client = _get_client()
        prompt = SYSTEM_PROMPT.format(context=context)
        full_prompt = f"{prompt}\n\nالمستخدم: {user_message}"
        response = client.models.generate_content(
            model=Config.GEMINI_MODEL,
            contents=full_prompt,
        )
        reply = response.text
        
        # تنسيق نهائي للرد
        reply = reply.replace('**الفرصة', '\n\n**الفرصة')
        reply = reply.replace('- الجهة:', '\n- الجهة:')
        reply = reply.replace('- الوصف:', '\n- الوصف:')
        reply = reply.replace('- الموعد:', '\n- الموعد:')
        reply = reply.replace('- الشروط:', '\n- الشروط:')
        reply = reply.replace('. ', '.\n')
        reply = reply.replace('، ', '،\n')
        
        return reply
    except Exception as e:
        return f"⚠️ عذراً، حدث خطأ أثناء معالجة طلبك: {str(e)}"