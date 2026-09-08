import re
from config import EXCLUDE_COMPANY_KEYWORDS, EXCLUDE_DOMAINS

ATS_SLUG_PATTERN = re.compile(
    r"(?:greenhouse\.io|lever\.co|smartrecruiters\.com|jobvite\.com|icims\.com|ashbyhq\.com)/([a-zA-Z0-9\-]+)"
)
WORKDAY_PATTERN = re.compile(r"([a-zA-Z0-9\-]+)\.wd\d*\.myworkdayjobs\.com")


def extract_company_slug(url):
    m = ATS_SLUG_PATTERN.search(url)
    if m:
        return m.group(1)
    m = WORKDAY_PATTERN.search(url)
    if m:
        return m.group(1)
    return None


def verify_company(company_name, url, posting_text):
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

    if "our client" in text or "on behalf of" in text:
        return False, "excluded: agency language ('our client' / 'on behalf of')"

    return True, "no red flags detected (manually verify company page if uncertain)"
