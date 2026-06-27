import json
from pathlib import Path
from typing import Any

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "opportunities.json"


def load_opportunities() -> list[dict[str, Any]]:
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


def search_opportunities(
    query: str,
    type_filter: str | None = None,
) -> list[dict[str, Any]]:
    opportunities = load_opportunities()
    
    if not opportunities:
        return []

    type_keywords = {
        'منحة': 'منحة', 'دراسة': 'منحة', 'ابتعاث': 'منحة',
        'وظيفة': 'وظيفة', 'عمل': 'وظيفة',
        'تدريب': 'تدريب', 'دورة': 'تدريب',
    }
    
    query_lower = query.lower()
    detected_type = None
    for word, opp_type in type_keywords.items():
        if word in query_lower:
            detected_type = opp_type
            break

    final_type_filter = detected_type or type_filter

    important_keywords =   type_keywords = {
        'منحة': 'منحة',
        'دراسة': 'منحة',
        'ابتعاث': 'منحة',
        'وظيفة': 'وظيفة',
        'عمل': 'وظيفة',
        'تدريب': 'تدريب',
        'دورة': 'تدريب',
    }
    
    has_important_keyword = any(word in query_lower for word in important_keywords)

    results = []
    for opp in opportunities:
        if final_type_filter and opp.get('type') != final_type_filter:
            continue

        if not has_important_keyword:
            results.append(opp)
            continue

        searchable = f"{opp.get('title', '')} {opp.get('description', '')} {opp.get('organization', '')}".lower()
        query_words = set(query_lower.split())
        if any(word in searchable for word in query_words):
            results.append(opp)

    if not results:
        if final_type_filter:
            results = [opp for opp in opportunities if opp.get('type') == final_type_filter]
        else:
            results = opportunities

    return results


def get_context(opportunities):
    """تحويل قائمة الفرص إلى سياق نصي لـ Gemini"""
    if not opportunities:
        return "لا توجد فرص متاحة حالياً."
    context = "الفرص المتاحة:\n"
    for opp in opportunities:
        context += f"\n- {opp.get('title')} | {opp.get('organization')} | {opp.get('type')}"
    return context