import re

def check_schema_markup(soup):
    scripts = soup.find_all("script", type="application/ld+json")
    found = len(scripts) > 0
    return {
        "found": found,
        "count": len(scripts),
        "details": "Schema.org markup detected" if found else "No schema markup found"
    }

def check_entity_coverage(text, entities):
    text_lower = text.lower()
    found = {}
    for entity in entities:
        found[entity] = entity.lower() in text_lower
    return found

def calculate_visibility_score(schema_result, entity_coverage, content_length):
    score = 0
    if schema_result["found"]:
        score += 30
    covered = sum(1 for v in entity_coverage.values() if v)
    score += min(covered * 10, 40)
    if content_length > 500:
        score += 15
    elif content_length > 200:
        score += 8
    return min(score, 100)

def generate_recommendations(schema_result, entity_coverage):
    recs = []
    if not schema_result["found"]:
        recs.append("Add LocalBusiness schema markup to help AI understand your services.")
    missing_entities = [e for e, found in entity_coverage.items() if not found]
    if missing_entities:
        recs.append(f"Clearly mention: {', '.join(missing_entities)} on your homepage.")
    if len(recs) == 0:
        recs.append("Your site has good foundational visibility. Consider adding more detailed service pages.")
    return recs
