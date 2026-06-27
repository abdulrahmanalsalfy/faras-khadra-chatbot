import re
import html


MALICIOUS_PATTERNS = [
    r"<script[^>]*>.*?</script>",
    r"<iframe[^>]*>.*?</iframe>",
    r"<object[^>]*>.*?</object>",
    r"<embed[^>]*>.*?</embed>",
    r"<svg[^>]*>.*?</svg>",
    r"on\w+\s*=",
    r"javascript\s*:",
    r"data\s*:\s*text/html",
    r"vbscript\s*:",
    r"expression\s*\(",
]

MALICIOUS_KEYWORDS = [
    r"(?i)\bDROP\s+TABLE\b",
    r"(?i)\bDROP\s+DATABASE\b",
    r"(?i)\bDELETE\s+FROM\b",
    r"(?i)\bTRUNCATE\b",
    r"(?i)\bALTER\s+TABLE\b",
    r"(?i)\bEXEC\b",
    r"(?i)\bEXECUTE\b",
    r"(?i)\bUNION\s+SELECT\b",
    r"(?i)\bLOAD_FILE\b",
    r"(?i)\bINTO\s+OUTFILE\b",
    r"(?i)\bINTO\s+DUMPFILE\b",
    r"(?i)\bINFORMATION_SCHEMA\b",
    r"(?i)\bPG_SLEEP\b",
    r"(?i)\bWAITFOR\s+DELAY\b",
    r"(?i)\bSLEEP\s*\(",
    r"(?i)\bBENCHMARK\s*\(",
    r"(?i)\bCHAR\s*\(",
    r"(?i)\bUNICODE\s*\(",
    r"(?i)\bNCHAR\s*\(",
    r"(?i)\bCONVERT\s*\(",
    r"(?i)\bCAST\s*\(",
]

COMMAND_INJECTION_PATTERNS = [
    r"[|;&`$]",
    r"(?i)\brm\s+-[rf]",
    r"(?i)\bwget\b",
    r"(?i)\bcurl\b",
    r"(?i)\bbase64\b",
    r"(?i)\beval\b",
    r"(?i)\bexec\b",
    r"(?i)\bsystem\b",
    r"(?i)\bpopen\b",
    r"(?i)\bsubprocess\b",
    r"(?i)\bos\.system\b",
    r"(?i)\bos\.popen\b",
    r"(?i)\b__import__\b",
    r"(?i)\b__builtins__\b",
    r"(?i)\bglobals\s*\(",
    r"(?i)\blocals\s*\(",
    r"(?i)\bcompile\s*\(",
    r"(?i)\bexecfile\b",
    r"(?i)\binput\s*\(",
]

PATH_TRAVERSAL_PATTERNS = [
    r"\.\.[\\/]",
    r"(?i)\b/etc/passwd\b",
    r"(?i)\bC:\\\\(Windows|Users|Program)",
]


def strip_html(text: str) -> str:
    return re.sub(r"<[^>]*>", "", text)


def escape_html(text: str) -> str:
    return html.escape(text, quote=True)


def sanitize_message(text: str, max_length: int = 500) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    text = strip_html(text)
    text = html.escape(text, quote=True)
    return text[:max_length]


def has_xss(text: str) -> bool:
    for pattern in MALICIOUS_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE | re.DOTALL):
            return True
    return False


def has_sql_injection(text: str) -> bool:
    for pattern in MALICIOUS_KEYWORDS:
        if re.search(pattern, text):
            return True
    return False


def has_command_injection(text: str) -> bool:
    for pattern in COMMAND_INJECTION_PATTERNS:
        if re.search(pattern, text):
            return True
    return False


def has_path_traversal(text: str) -> bool:
    for pattern in PATH_TRAVERSAL_PATTERNS:
        if re.search(pattern, text):
            return True
    return False


def is_malicious(text: str) -> bool:
    return (
        has_xss(text)
        or has_sql_injection(text)
        or has_command_injection(text)
        or has_path_traversal(text)
    )


def validate_message(text: str, max_length: int = 500) -> dict:
    result = {
        "valid": True,
        "sanitized": "",
        "error": None,
    }

    clean = (text or "").strip()
    if not clean:
        result["valid"] = False
        result["error"] = "الرسالة فارغة."
        return result

    if len(clean) > max_length:
        result["valid"] = False
        result["error"] = f"الرسالة طويلة جداً. الحد الأقصى {max_length} حرف."
        return result

    if has_xss(clean):
        result["valid"] = False
        result["error"] = "تم الكشف عن محتوى ضار (XSS)."
        return result

    if has_command_injection(clean):
        result["valid"] = False
        result["error"] = "تم الكشف عن محتوى ضار (حقن أوامر)."
        return result

    if has_path_traversal(clean):
        result["valid"] = False
        result["error"] = "تم الكشف عن محتوى ضار (عبور المسار)."
        return result

    result["sanitized"] = sanitize_message(clean, max_length)
    return result
