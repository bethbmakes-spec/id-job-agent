"""
Glassdoor-style reputation red-flag check, focused on Marketing and Design/
Creative team sentiment (the departments most relevant to an Instructional
Designer, since ID roles frequently sit within or work closely with those
teams).

IMPORTANT: Glassdoor aggressively blocks direct scraping (returns CAPTCHAs/
403s to automated requests), so this module does NOT scrape Glassdoor
directly. Instead it uses a search-engine query (Google Custom Search, same
API already used for career-page discovery) to surface Glassdoor review
snippets and other public commentary, then flags concerning language.
Treat this as a triage signal, not a guarantee -- always skim the actual
Glassdoor page for any company that scores as a "possible red flag" before
ruling it out.

Usage:
    from reputation_check import check_company_reputation
    flag, notes = check_company_reputation("Acme Corp", api_key, cse_id)
"""
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
    """Search for Glassdoor reviews mentioning the company + marketing/design teams."""
    base = "https://www.googleapis.com/customsearch/v1"
    query = f'"{company_name}" glassdoor reviews marketing design team'
    params = {"key": api_key, "cx": cse_id, "q": query, "num": num}
    try:
        r = requests.get(base, params=params, timeout=15)
        data = r.json()
        return data.get("items", [])
    except Exception as e:
        print(f"[warn] reputation search failed for {company_name}: {e}")
        return []


def check_company_reputation(company_name, api_key=None, cse_id=None):
    """
    Returns (flagged: bool, notes: str).
    flagged=True means red-flag language was found near marketing/design
    team mentions in public review snippets -- recommend manual Glassdoor
    check before applying.
    """
    if not api_key or not cse_id:
        return False, "reputation check skipped (no search API configured)"

    items = search_glassdoor_snippets(company_name, api_key, cse_id)
    time.sleep(1)  # rate-limit courtesy

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
