# Instructional Design Job Search Agent

Automated Mon/Wed/Fri job search for Senior-level Instructional Design, LMS
Administrator, Course Developer, Learning Experience Designer, Learning
Architect, and Training Manager roles — sourced from **company career pages
and niche L&D job boards only**, never LinkedIn or Indeed.

## Sources currently searched

**Niche/direct L&D job boards** (each has its own tailored parser in `scraper.py`):
- ATD Job Bank (may 403 — see Known Limitations)
- Teamed for Learning
- Remote Rocketship — L&D (most reliable source so far)
- Remotive — Education
- We Work Remotely
- HigherEdJobs
- Built In Remote
- Chronicle of Higher Ed
- eLearning Industry Jobs

**Company career pages** via Google Custom Search, restricted to major ATS
platforms: Greenhouse, Lever, Workday, SmartRecruiters, Paylocity, iCIMS,
Jobvite, BambooHR, Ashby. **This only runs if `GOOGLE_API_KEY` and
`GOOGLE_CSE_ID` are both set** — without them, you only get niche-board
results (this is why you were only seeing Remote Rocketship hits).

## Why some sources return 0 results

Different sites block scrapers differently:
- **403 Forbidden** (ATD Job Bank) = the site actively blocks non-browser
  traffic. A realistic browser User-Agent (already added) helps some sites
  but not all; fully bypassing this requires a headless browser tool like
  Playwright/Selenium — not included by default to keep this lightweight.
- **0 results but no error** (Teamed for Learning, We Work Remotely,
  HigherEdJobs, Built In) = the page loaded fine, but its HTML structure
  doesn't match the current parser's search pattern (common when a site
  uses heavy JavaScript rendering, or unusual class names). These need a
  custom parser tuned to the live HTML — open the site, view page source,
  and tell me what job listings look like there and I'll write a matching
  parser function.

## Adding more sites yourself

1. Add an entry to `NICHE_BOARDS` in `config.py`:
   ```python
   {"name": "Site Name", "url": "https://example.com/jobs", "parser": "generic_links"}
   ```
2. If `generic_links` returns 0 results for that site, that site needs a
   custom parser function in `scraper.py` (see `parse_remoterocketship`,
   `parse_remotive`, `parse_weworkremotely` for examples) — tell me the
   site and I'll write one.

## Getting the company-career-page search working (biggest coverage boost)

If `GOOGLE_API_KEY` / `GOOGLE_CSE_ID` aren't set, you're missing the
Greenhouse/Lever/Workday/etc. company-page search entirely — this is
usually where the best senior-level direct-employer postings show up.
Double check both secrets are set correctly in GitHub Actions (Settings →
Secrets and variables → Actions) and spelled exactly `GOOGLE_API_KEY` and
`GOOGLE_CSE_ID`.

## What it does

1. Crawls niche/direct L&D job boards with per-site parsers.
2. Searches company career pages directly via Google Custom Search (ATS domains above).
3. Filters out postings below $105k, tax-titled roles (unless remote),
   defense/military contractors, staffing/recruiting agencies, and offshore
   (India/Pakistan-based) third-party recruiter postings — only direct
   employers are kept. Flags remote/bonus/benefits language for ranking.
4. Scores and ranks postings (remote + bonus + benefits + salary-floor-met
   all add points) so the best matches surface first.
5. Checks company reputation for red flags — searches for Glassdoor review
   snippets mentioning the marketing/design/creative teams and flags
   language like "toxic culture," "high turnover," "understaffed." Flagged
   companies are penalized in ranking and marked in red in the email, but
   not auto-excluded.
6. Emails you a digest (HTML table + CSV attachment) 3x/week.

## Setup (10 minutes)

1. Install dependencies: `pip install -r requirements.txt`
2. Set these as environment variables / GitHub Secrets:
   - `GOOGLE_API_KEY` / `GOOGLE_CSE_ID` — needed for company career-page search
   - `SMTP_USER` / `SMTP_PASS` — Gmail address + App Password (not your normal password)
3. Edit `config.py`:
   - `EMAIL_TO` — your inbox
   - `TARGET_TITLES` — add/remove title variants
   - `MIN_SALARY` — currently $105,000
   - `NICHE_BOARDS` — add more job boards
4. Test manually: `python run_agent.py`
5. Check `output/job_digest_<date>.csv` for results.

## Scheduling (Mon/Wed/Fri)

Currently running via **GitHub Actions** — see `.github/workflows/job-agent.yml`
in the repo. Cron: `30 14 * * 1,3,5` (7:30 AM Arizona time; AZ has no DST so
this offset stays fixed year-round).

## Exclusion rules (hard filters)

- **Defense/military contractors** — Lockheed Martin, Raytheon/RTX, Northrop
  Grumman, General Dynamics, L3Harris, Booz Allen, Leidos, SAIC, CACI,
  Palantir, Anduril, plus signals like "security clearance required."
- **Staffing/recruiting agencies** — Robert Half, Randstad, Adecco, Kelly
  Services, Insight Global, TEKsystems, Kforce, plus "on behalf of our client."
- **Offshore recruiters** — India/Pakistan-based third-party firms (Hexaware,
  Mastech Digital, Genpact staffing, "Pvt Ltd" naming), and explicit
  "recruiter based in India/Pakistan" mentions.
- **Company verification** (`company_check.py`) — confirms the posting URL
  matches a known ATS company slug (e.g. `greenhouse.io/acmecorp`), and
  rejects agency language even if the firm isn't keyword-listed yet.

Edit keyword lists in `config.py` any time.

## Files

- `config.py` — tunable settings (titles, salary floor, boards, exclusions)
- `scraper.py` — crawls boards (per-site parsers) + ATS career-page search, filters, scores, writes CSV
- `company_check.py` — direct-employer verification
- `reputation_check.py` — Glassdoor red-flag triage
- `mailer.py` — builds and sends the HTML email digest
- `run_agent.py` — entry point the scheduler calls
- `.env.example` — template for required credentials
