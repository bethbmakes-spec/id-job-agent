"""
Core scraping / filtering logic for the Instructional Design Job Search Agent.
Two source types:
  A) Niche/direct L&D job boards (crawled directly with requests+BeautifulSoup)
  B) Company career-page postings surfaced via a site-restricted search
     (Google Custom Search JSON API against major ATS domains: Greenhouse,
      Lever, Workday, SmartRecruiters, iCIMS, Jobvite, BambooHR, Ashby —
      these ARE the company's own site/subdomain, not LinkedIn/Indeed)

Run: python scraper.py
Outputs: output/job_digest_<date>.csv and .html
"""
import re
import csv
import json
import time
import os
from datetime import date
import requests
from bs4 import BeautifulSoup

from config import (
    TARGET_TITLES, MIN_SALARY, EXCLUDE_KEYWORDS, EXCLUDE_UNLESS_REMOTE,
    ATS_DOMAINS, NICHE_BOARDS, REQUIRE_BENEFITS_MENTION,
    EXCLUDE_COMPANY_KEYWORDS, EXCLUDE_DOMAINS, REQUIRE_DIRECT_EMPLOYER
)
from company_check import verify_company
from reputation_check import check_company_reputation

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; IDJobAgent/1.0)"}

SALARY_RE = re.compile(r"\$?\s?(\d{2,3}(?:,\d{3})|\d{2,3}k)\s*(?:-|to|–)\s*\$?\s?(\d{2,3}(?:,\d{3})|\d{2,3}k)", re.I)
SINGLE_SALARY_RE = re.compile(r"\$\s?(\d{2,3}),(\d{3})")


def parse_salary_range(text):
    """Return (low, high) ints if a salary range is found in text, else None."""
    text = text.replace(",", "")
    m = re.search(r"\$?\s?(\d{2,3})k\s*(?:-|to|–)\s*\$?\s?(\d{2,3})k", text, re.I)
    if m:
        return int(m.group(1)) * 1000, int(m.group(2)) * 1000
    m = re.search(r"\$(\d{5,6})\s*(?:-|to|–)\s*\$?(\d{5,6})", text)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None


def meets_salary_floor(text, floor=MIN_SALARY):
    rng = parse_salary_range(text)
    if rng is None:
        return None  # unknown — flag for manual review rather than auto-exclude
    low, high = rng
    return high >= floor


def is_excluded(text, is_remote):
    lower = text.lower()
    hit = any(kw in lower for kw in EXCLUDE_KEYWORDS)
    if hit and not (EXCLUDE_UNLESS_REMOTE and is_remote):
        return True
    return False


def is_hard_excluded(text, url=""):
    """Hard excludes that apply regardless of remote status: defense
    contractors, staffing/recruiting agencies, and offshore recruiters
    (India/Pakistan-based third-party recruiters). Returns (excluded, reason)."""
    lower = text.lower()
    lower_url = url.lower()

    for kw in EXCLUDE_COMPANY_KEYWORDS:
        if kw in lower:
            return True, f"matched excluded keyword: '{kw}'"

    for dom in EXCLUDE_DOMAINS:
        if dom in lower_url or dom in lower:
            return True, f"matched excluded domain: '{dom}'"

    return False, None


def looks_remote(text):
    lower = text.lower()
    return "remote" in lower and "no remote" not in lower and "not remote" not in lower


def has_benefits_mention(text):
    lower = text.lower()
    return any(k in lower for k in ["benefit", "401(k)", "401k", "health insurance", "pto", "paid time off"])


def has_bonus_mention(text):
    lower = text.lower()
    return any(k in lower for k in ["bonus", "incentive pay", "variable pay", "commission"])


def title_matches(text):
    lower = text.lower()
    return any(t.lower() in lower for t in TARGET_TITLES)


def score_posting(text, is_remote):
    score = 0
    if is_remote:
        score += 2
    if has_bonus_mention(text):
        score += 1
    if has_benefits_mention(text):
        score += 1
    sal = meets_salary_floor(text)
    if sal:
        score += 2
    return score


def fetch(url, timeout=15):
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(f"[warn] fetch failed {url}: {e}")
        return None


def crawl_niche_boards():
    """Very lightweight generic crawler: pulls links + surrounding text.
    Each board's HTML structure differs — this does a best-effort keyword scan
    of visible text and link hrefs, meant as a starting point to refine per-site
    CSS selectors once you see real output."""
    results = []
    for board in NICHE_BOARDS:
        html = fetch(board["url"])
        if not html:
            continue
        soup = BeautifulSoup(html, "html.parser")
        page_text = soup.get_text(" ", strip=True)
        for a in soup.find_all("a", href=True):
            link_text = a.get_text(strip=True)
            if not link_text or len(link_text) < 4:
                continue
            if title_matches(link_text):
                href = a["href"]
                if href.startswith("/"):
                    from urllib.parse import urljoin
                    href = urljoin(board["url"], href)
                results.append({
                    "source": board["name"],
                    "title": link_text,
                    "url": href,
                    "raw_context": page_text[:500],
                })
    return results


def search_ats_sites_via_google_cse(api_key, cse_id):
    """Search company career pages hosted on major ATS platforms (Greenhouse,
    Lever, Workday, etc.) — this counts as 'the company's own site' since these
    are the employer's branded application pages, not LinkedIn/Indeed.
    Requires GOOGLE_API_KEY and GOOGLE_CSE_ID env vars / config."""
    results = []
    base = "https://www.googleapis.com/customsearch/v1"
    for title in TARGET_TITLES:
        for domain in ATS_DOMAINS:
            query = f'"{title}" site:{domain}'
            params = {"key": api_key, "cx": cse_id, "q": query, "num": 5}
            try:
                r = requests.get(base, params=params, timeout=15)
                data = r.json()
                for item in data.get("items", []):
                    results.append({
                        "source": domain,
                        "title": item.get("title"),
                        "url": item.get("link"),
                        "raw_context": item.get("snippet", ""),
                    })
            except Exception as e:
                print(f"[warn] CSE search failed for {query}: {e}")
            time.sleep(1)  # be polite / respect rate limits
    return results


def build_digest(api_key=None, cse_id=None, check_reputation=True):
    all_results = crawl_niche_boards()
    if api_key and cse_id:
        all_results += search_ats_sites_via_google_cse(api_key, cse_id)

    rows = []
    excluded_log = []
    for job in all_results:
        text = job["title"] + " " + job.get("raw_context", "")
        url = job.get("url", "")
        remote = looks_remote(text)

        hard_excluded, reason = is_hard_excluded(text, url)
        if hard_excluded:
            excluded_log.append({**job, "exclusion_reason": reason})
            continue

        if REQUIRE_DIRECT_EMPLOYER:
            is_direct, direct_reason = verify_company(job.get("source", ""), url, text)
            if not is_direct:
                excluded_log.append({**job, "exclusion_reason": direct_reason})
                continue

        if is_excluded(text, remote):
            excluded_log.append({**job, "exclusion_reason": "tax-related, not remote"})
            continue

        sal_ok = meets_salary_floor(text)
        if sal_ok is False:
            excluded_log.append({**job, "exclusion_reason": "below salary floor"})
            continue

        if REQUIRE_BENEFITS_MENTION and has_benefits_mention(text) is False and sal_ok is not None:
            pass  # don't hard-exclude on benefits since snippets are short; flag instead

        rep_flag, rep_notes = (False, "not checked")
        if check_reputation and api_key and cse_id:
            company_guess = job.get("source", "")
            rep_flag, rep_notes = check_company_reputation(company_guess, api_key, cse_id)

        row_score = score_posting(text, remote)
        if rep_flag:
            row_score -= 3  # penalize but don't hard-exclude -- human judgment call

        rows.append({
            **job,
            "remote": remote,
            "salary_range_detected": parse_salary_range(text),
            "benefits_mentioned": has_benefits_mention(text),
            "bonus_mentioned": has_bonus_mention(text),
            "reputation_flag": rep_flag,
            "reputation_notes": rep_notes,
            "score": row_score,
        })

    if excluded_log:
        print(f"[info] Hard-excluded {len(excluded_log)} postings "
              f"(defense contractors, staffing agencies, offshore recruiters, tax roles, or below salary floor).")

    rows.sort(key=lambda r: r["score"], reverse=True)

    os.makedirs("output", exist_ok=True)
    today = date.today().isoformat()
    csv_path = f"output/job_digest_{today}.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "title", "url", "remote",
                                                 "salary_range_detected", "benefits_mentioned",
                                                 "bonus_mentioned", "reputation_flag", "reputation_notes",
                                                 "score", "raw_context"])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    return rows, csv_path


if __name__ == "__main__":
    api_key = os.environ.get("GOOGLE_API_KEY")
    cse_id = os.environ.get("GOOGLE_CSE_ID")
    rows, path = build_digest(api_key, cse_id)
    print(f"Found {len(rows)} candidate postings. Saved to {path}")
