"""
Lightweight company-verification helper.

Goal: confirm a job posting is from the DIRECT employer's own site/ATS
tenant (e.g. boards.greenhouse.io/acmecorp, acmecorp.wd5.myworkdayjobs.com),
not a staffing agency reposting a client's role, and not a defense
contractor. This is a heuristic layer -- for full certainty, a human should
glance at the "About [Company]" section of any posting scored highly.

Usage:
    from company_check import verify_company
    ok, reason = verify_company(company_name, posting_url, posting_text)
"""
import re
from config import EXCLUDE_COMPANY_KEYWORDS, EXCLUDE_DOMAINS

# ATS subdomain patterns that indicate a specific company's own careers page
# e.g. boards.greenhouse.io/<company-slug>, jobs.lever.co/<company-slug>
ATS_SLUG_PATTERN = re.compile(
    r"(?:greenhouse\.io|lever\.co|smartrecruiters\.com|jobvite\.com|icims\.com|ashbyhq\.com)/([a-zA-Z0-9\-]+)"
)
WORKDAY_PATTERN = re.compile(r"([a-zA-Z0-9\-]+)\.wd\d*\.myworkdayjobs\.com")


def extract_company_slug(url):
    """Pull the company slug out of a known ATS URL, if possible."""
    m = ATS_SLUG_PATTERN.search(url)
    if m:
        return m.group(1)
    m = WORKDAY_PATTERN.search(url)
    if m:
        return m.group(1)
    return None


def verify_company(company_name, url, posting_text):
    """
    Returns (is_direct_employer: bool, reason: str)
    """
    text = f"{company_name} {posting_text}".lower()
    url_lower = (url or "").lower()

    for kw in EXCLUDE_COMPANY_KEYWORDS:
        if kw in text:
            return False, f"excluded: matched keyword '{kw}'"

    for dom in EXCLUDE_DOMAINS:
        if dom in url_lower:
            return False, f"excluded: staffing agency domain '{dom}'"

    slug = extract_company_slug(url)
    if slug:
        return True, f"confirmed direct employer via ATS slug '{slug}'"

    # If posting explicitly names the hiring company and doesn't hit any
    # exclusion keyword, treat as provisionally direct (flag for human check
    # only if uncertain language like "our client" appears without a keyword hit)
    if "our client" in text or "on behalf of" in text:
        return False, "excluded: agency language ('our client' / 'on behalf of')"

    return True, "no red flags detected (manually verify company page if uncertain)"
