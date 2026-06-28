# 🌱 فرص خضراء - المساعد الذكي

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1.3-green)](https://flask.palletsprojects.com)
[![Gemini](https://img.shields.io/badge/Gemini-API-orange)](https://ai.google.dev)

---

## 📖 عن المشروع

**المساعد الذكي** هو شات بوت تفاعلي يهدف إلى تسهيل وصول الشباب إلى الفرص المتاحة (منح، وظائف، تدريب) على منصة **"فرص خضراء"**.

يستخدم المشروع نموذج **Google Gemini API** لفهم الأسئلة باللغة العربية، ويعرض الفرص المخزنة في قاعدة بيانات محلية (JSON) بطريقة منظمة وسلسة.

---

## 🛠️ التقنيات المستخدمة

| التقنية | الغرض |
|---------|-------|
| **Python 3.11+** | لغة البرمجة الأساسية |
| **Flask** | إطار العمل الخلفي (Backend) |
| **Google Gemini API** | النموذج اللغوي لفهم الأسئلة |
| **HTML + CSS + JavaScript** | واجهة المستخدم الأمامية (Frontend) |
| **JSON** | تخزين البيانات التجريبية |

---

## 🛡️ الميزات الأمنية

تم تنفيذ عدد من الممارسات الأمنية لحماية التطبيق والمستخدمين:

### 1. Rate Limiter (تحديد عدد الطلبات)
- يسمح بـ **10 طلبات في الدقيقة** لكل عنوان IP.
- يمنع الاستخدام المفرط للـ API ويحمي من هجمات **DoS**.

```python
# utils/rate_limiter.py
def is_rate_limited(ip: str, limit: int = 10, window: int = 60) -> bool:
    now = time.time()
    requests[ip] = [t for t in requests[ip] if now - t < window]
    if len(requests[ip]) >= limit:
        return True
    requests[ip].append(now)
    return False

---

## 📂 هيكل المشروع
faras-khadra-chatbot/
│
├── app.py # نقطة الدخول الرئيسية
├── config.py # إعدادات التطبيق
├── requirements.txt # المكتبات المطلوبة
├── .env # المتغيرات البيئية (API Key)
├── .gitignore # الملفات المستثناة من Git
│
├── data/
│ └── opportunities.json # قاعدة البيانات (18 فرصة)
│
├── services/
│ ├── data_service.py # البحث وتصفية البيانات
│ └── llm_service.py # الاتصال بـ Gemini API
│
├── utils/
│ ├── rate_limiter.py # تحديد عدد الطلبات
│ └── validators.py # التحقق من صحة المدخلات
│
├── templates/
│ └── index.html # واجهة المستخدم الرئيسية
│
├── static/
│ ├── style.css # تنسيق الصفحة
│ └── logo.png # شعار المنصة
│
└── logs/
└── app.log # سجل الطلبات



---

## 🚀 كيفية التشغيل

### 1️⃣ استنساخ المشروع

```bash
git clone https://github.com/abdulrahmanalsalfy/faras-khadra-chatbot.git
cd faras-khadra-chatbot
2️⃣ إنشاء بيئة افتراضية
bash
python -m venv venv
لتفعيل البيئة:

Windows:

bash
venv\Scripts\activate
macOS / Linux:

bash
source venv/bin/activate
3️⃣ تثبيت المكتبات المطلوبة
bash
pip install -r requirements.txt
4️⃣ إعداد مفتاح Gemini API
احصل على مفتاح مجاني من: Google AI Studio

أنشئ ملف .env في المجلد الرئيسي وأضف:

env
GEMINI_API_KEY=AIzaSyD-xxxxxxxxxxxxxxxxx
GEMINI_MODEL=gemini-2.0-flash
5️⃣ تشغيل التطبيق
bash
python app.py
ثم افتح المتصفح على الرابط:

text
http://127.0.0.1:5000
🤖 كيفية استخدام المساعد
أسئلة مقترحة
السؤال	النتيجة
أعطني المنح المتاحة	عرض المنح الدراسية
ما هي الوظائف المتاحة	عرض الوظائف الشاغرة
هل هناك تدريب	عرض البرامج التدريبية
أعطني كل الفرص	عرض جميع الفرص

I
📊 مقتطف من البيانات
json
{
  "id": 1,
  "type": "منحة",
  "title": "منحة الملك سلمان للابتعاث",
  "organization": "وزارة التعليم السعودية",
  "description": "منحة دراسية كاملة لدراسة البكالوريوس والماجستير...",
  "deadline": "2026-09-30",
  "eligibility": "معدل لا يقل عن 85% في الثانوية العامة"
}
📸 لقطة من الواجهة
(يمكنك إضافة صورة هنا لاحقاً)

https://screenshot.png

👨‍💻 المطور
عبدالرحمن السلفي

GitHub: @abdulrahmanalsalfy

البريد الإلكتروني: abdulrahman.alsalfy70@gmail.com

📄 الرخصة
جميع الحقوق محفوظة © 2026 — فرص خضراء

🙏 شكر وتقدير
شكر خاص لفريق فرص خضراء على إتاحة هذه الفرصة، ولمنصة Google لتوفير Gemini API المجاني.
