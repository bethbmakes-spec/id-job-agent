import time
import requests

RED_FLAG_PHRASES = [
    "toxic culture", "toxic management", "high turnover", "understaffed",
    "micromanagement", "micromanaged", "layoffs", "poor leadership",
    "no work life balance", "burnout", "favoritism", "disorganized",
    "lack of direction", "constant reorg", "bait and switch", "overworked",
    "unrealistic deadlines", "creative team is ignored", "marketing team is understaffed",
    "revolving door", "quit within months", "avoid this company", "run don't walk",
    "no growth opportunities", "unclear expectations", "low morale",
]
DEPARTMENT_TERMS = ["marketing team", "design team", "creative team", "designer", "marketing"]


def search_glassdoor_snippets(company_name, api_key, cse_id, num=5):
    base = "https://www.googleapis.com/customsearch/v1"
    query = f'"{company_name}" glassdoor reviews marketing design team'
    params = {"key": api_key, "cx": cse_id, "q": query, "num": num}
    try:
        r = requests.get(base, params=params, timeout=15)
        return r.json().get("items", [])
    except Exception as e:
        print(f"[warn] reputation search failed for {company_name}: {e}")
        return []


def check_company_reputation(company_name, api_key=None, cse_id=None):
    if not api_key or not cse_id:
        return False, "reputation check skipped (no search API configured)"
    items = search_glassdoor_snippets(company_name, api_key, cse_id)
    time.sleep(1)
    if not items:
        return False, "no Glassdoor/review snippets found (may need manual check)"
    hits = []
    for item in items:
        text = f"{item.get('title','')} {item.get('snippet','')}".lower()
        dept_mentioned = any(d in text for d in DEPARTMENT_TERMS)
        for phrase in RED_FLAG_PHRASES:
            if phrase in text:
                hits.append(f"'{phrase}'" + (" (dept-specific)" if dept_mentioned else ""))
    if hits:
        return True, "possible red flag -- review snippets mention: " + ", ".join(sorted(set(hits)))
    return False, "no red-flag language detected in available review snippets"
