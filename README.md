# Instructional Design Job Search Agent

Automated Mon/Wed/Fri job search for Senior-level Instructional Design, LMS
Administrator, Course Developer, Learning Experience Designer, Learning
Architect, and Training Manager roles — sourced from **company career pages
and niche L&D job boards only**, never LinkedIn or Indeed.

## What it does

1. **Crawls niche/direct L&D job boards** (`scraper.py: crawl_niche_boards`) —
   ATD Job Bank, Teamed for Learning, Remote Rocketship, Remotive, We Work
   Remotely, HigherEdJobs.
2. **Searches company career pages directly** via Google Custom Search,
   restricted to major ATS platforms (Greenhouse, Lever, Workday,
   SmartRecruiters, iCIMS, Jobvite, BambooHR, Ashby). These are the
   employer's own branded application pages — not a third-party aggregator.
3. **Filters** out postings below $105k, tax-titled roles (unless remote),
   defense/military contractors, staffing/recruiting agencies, and offshore
   (India/Pakistan-based) third-party recruiter postings -- only direct
   employers are kept. Flags remote/bonus/benefits language for ranking.
4. **Scores and ranks** postings (remote + bonus + benefits + salary-floor-met
   all add points) so the best matches surface first.
5. **Checks company reputation** for red flags -- searches for Glassdoor
   review snippets mentioning the marketing/design/creative teams and flags
   language like "toxic culture," "high turnover," "understaffed," or
   "creative team is ignored." Flagged companies are penalized in ranking
   and clearly marked in red in the email, but not auto-excluded -- you
   make the final call after a quick manual Glassdoor check.
6. **Emails you a digest** (HTML table + CSV attachment) 3x/week.

## Setup (10 minutes)

1. Install dependencies: `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and fill in:
   - `GOOGLE_API_KEY` / `GOOGLE_CSE_ID` — free tier gives 100 queries/day
     (plenty for this use case). Sign up at
     https://developers.google.com/custom-search/v1/overview and create a
     Programmable Search Engine at https://programmablesearchengine.google.com/
     configured to search the whole web (or restrict to the ATS domains in
     `config.py`).
   - `SMTP_USER` / `SMTP_PASS` — a Gmail address + App Password (or any SMTP
     account) to send the digest from.
3. Edit `config.py`:
   - `EMAIL_TO` — your inbox
   - `TARGET_TITLES` — add/remove title variants
   - `MIN_SALARY` — currently $105,000
   - `EXCLUDE_KEYWORDS` — currently just tax-related terms
4. Test manually: `python run_agent.py`
5. Check `output/job_digest_<date>.csv` for results.

## Scheduling (Mon/Wed/Fri, 7:30 AM MST)

**Option A — Replit Scheduled Deployment (recommended, no server needed):**
Deploy this project on Replit and set a Scheduled Deployment with cron
`30 14 * * 1,3,5` (7:30 AM MST = 14:30 UTC during MST; adjust for daylight
saving if your host uses UTC year-round — Arizona does not observe DST, so
this offset is fixed).

**Option B — cron on your own machine/server:**
```
30 7 * * 1,3,5 cd /path/to/id-job-agent && /usr/bin/python3 run_agent.py >> agent.log 2>&1
```

**Option C — GitHub Actions** (free, runs in the cloud):
Add a `.github/workflows/job-agent.yml` with `schedule: cron: '30 14 * * 1,3,5'`
and store secrets (GOOGLE_API_KEY, SMTP_USER, etc.) in repo Settings > Secrets.

## Reputation check (Marketing/Design team red flags)

`reputation_check.py` uses the same Google Custom Search API (already
configured for career-page discovery) to pull public Glassdoor review
snippets mentioning the company alongside marketing/design/creative team
terms, then scans for red-flag phrases: toxic culture, high turnover,
understaffed, micromanagement, layoffs, low morale, burnout, "creative team
is ignored," etc.

- Flagged companies get a **-3 score penalty** (pushed lower in ranking) and
  a red-highlighted row with a warning label in the emailed digest.
- This is a **triage signal, not a verdict** -- Glassdoor blocks direct
  scraping, so results come from search-engine snippets only, which may
  miss context or nuance. Always open the actual Glassdoor page for any
  company you're seriously considering before ruling it out or in.
- Edit `RED_FLAG_PHRASES` and `DEPARTMENT_TERMS` in `reputation_check.py`
  to tune sensitivity.

## Exclusion rules (hard filters)

These apply regardless of remote status or salary:

- **Defense/military contractors** — Lockheed Martin, Raytheon/RTX, Northrop
  Grumman, General Dynamics, L3Harris, Booz Allen, Leidos, SAIC, CACI,
  Palantir, Anduril, and generic signals like "security clearance required,"
  "DoD contractor," "cleared facility."
- **Staffing/recruiting agencies** — Robert Half, Randstad, Adecco, Kelly
  Services, Insight Global, TEKsystems, Kforce, and similar third-party
  firms, plus generic agency language like "on behalf of our client."
- **Offshore recruiters** — firms and language patterns commonly associated
  with India/Pakistan-based third-party recruiting (Pvt Ltd, Hexaware,
  Mastech Digital, Genpact staffing, etc.), and explicit "recruiter based in
  India/Pakistan" mentions.
- **Company verification** (`company_check.py`) — cross-checks the posting
  URL against known ATS company slugs (e.g. `greenhouse.io/acmecorp`) to
  confirm it's the employer's own branded career page, and rejects agency
  language ("our client," "on behalf of") even if the specific firm isn't on
  the keyword list yet.

Edit `DEFENSE_CONTRACTOR_KEYWORDS`, `STAFFING_AGENCY_KEYWORDS`,
`OFFSHORE_RECRUITER_KEYWORDS`, and `EXCLUDE_DOMAINS` in `config.py` any time
you spot a new company/agency you want blocked -- no code changes needed.

## Known limitations & tuning notes

- Some job boards (ATD Job Bank, Remote Rocketship) return 403 to basic
  scrapers — they may require a rendered browser (Selenium/Playwright) or a
  proper API. If they block requests, the agent still runs fine using the
  other boards + Google CSE company-site search; consider adding
  Playwright later if you want full coverage.
- Salary detection is regex-based and only catches postings that state a
  number. Many company sites omit salary — those are silently excluded by
  default. If you'd rather see them flagged as "salary unknown — check
  manually" instead of dropped, tell me and I'll adjust the filter logic.
- Benefits/bonus detection is a keyword flag for ranking, not a hard filter,
  since short search snippets often don't mention them even when true.
- Add more companies to `ATS_DOMAINS` (e.g., specific corporate Workday
  tenants) once you identify target employers you want prioritized.

## Files

- `config.py` — all tunable settings (titles, salary floor, exclusions, schedule)
- `scraper.py` — crawls boards + searches ATS-hosted career pages, filters, scores, writes CSV
- `mailer.py` — builds and sends the HTML email digest
- `run_agent.py` — the script the scheduler actually calls
- `.env.example` — template for required credentials
