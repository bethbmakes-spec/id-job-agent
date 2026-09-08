"""
Configuration for the Instructional Design Job Search Agent.
Edit the lists below to tune the search — no code changes needed elsewhere.
"""

# ---- Job titles to search for (Boolean OR) ----
TARGET_TITLES = [
    "Senior Instructional Designer",
    "Sr. Instructional Designer",
    "Lead Instructional Designer",
    "Instructional Design Manager",
    "Senior LMS Administrator",
    "LMS Administrator",
    "Senior Course Developer",
    "Course Developer",
    "Senior Learning Experience Designer",
    "Learning Experience Designer",
    "Learning Architect",
    "Senior Learning Architect",
    "Training Manager",
    "Senior Training Manager",
    "Director of Learning and Development",
    "Head of Learning and Development",
]

# ---- Hard filters ----
MIN_SALARY = 105000          # USD/year, minimum acceptable base pay
REQUIRE_BENEFITS_MENTION = True   # posting must mention "benefits" (health/401k/PTO etc.)
PREFER_BONUS_MENTION = True       # not a hard filter — boosts ranking, doesn't exclude
PREFER_REMOTE = True              # not a hard filter — boosts ranking
EXCLUDE_KEYWORDS = ["tax", "taxation", "tax preparer", "tax accountant"]  # excluded unless job is remote
EXCLUDE_UNLESS_REMOTE = True      # if EXCLUDE_KEYWORDS found, only exclude when NOT remote

# ---- Hard excludes (never included, regardless of remote status) ----
# Defense / military contractors — company name and posting-text signals
DEFENSE_CONTRACTOR_KEYWORDS = [
    "lockheed martin", "raytheon", "rtx corporation", "northrop grumman",
    "general dynamics", "l3harris", "l3 technologies", "boeing defense",
    "booz allen hamilton", "leidos", "saic", "science applications international",
    "caci", "parsons corporation", "bae systems", "textron systems",
    "huntington ingalls", "anduril", "palantir", "national security agency",
    "defense contractor", "dod contractor", "cleared facility",
    "top secret clearance", "security clearance required", "dod clearance",
    "department of defense", "military training systems", "army contract",
    "navy contract", "air force contract", "defense industry",
]

# Staffing / recruiting agencies — only DIRECT employers wanted, not 3rd-party
# staffing firms placing candidates at client companies.
STAFFING_AGENCY_KEYWORDS = [
    "staffing agency", "staffing firm", "recruiting agency", "recruitment agency",
    "talent agency", "on behalf of our client", "our client is seeking",
    "one of our clients", "c2c", "corp to corp", "contract to hire staffing",
    "robert half", "randstad", "adecco", "kelly services", "manpower",
    "insight global", "aston carter", "actalent", "kforce", "teksystems",
    "apex systems", "collabera", "volt technical", "yoh", "cybercoders",
    "artech", "mindlance", "hexaware staffing", "ust global staffing",
]

# Known offshore recruiting/staffing firms (frequently India/Pakistan-based
# third-party recruiters posting US roles) — exclude their postings outright.
OFFSHORE_RECRUITER_KEYWORDS = [
    "pvt ltd", "pvt. ltd", "private limited", "hexaware", "wipro", "infosys bpm",
    "tcs (recruiter)", "cognizant staffing", "hcl technologies recruiter",
    "mastech digital", "ust global", "sysmind", "diverse lynx", "compunnel",
    "cliecon solutions", "nityo infotech", "vaco llc india", "genpact staffing",
    "recruiter based in india", "recruiter based in pakistan", "offshore recruiter",
]

EXCLUDE_COMPANY_KEYWORDS = (
    DEFENSE_CONTRACTOR_KEYWORDS + STAFFING_AGENCY_KEYWORDS + OFFSHORE_RECRUITER_KEYWORDS
)

# Domains belonging to staffing/recruiting agencies -- if a posting or contact
# email/domain matches one of these, hard-exclude regardless of other signals.
EXCLUDE_DOMAINS = [
    "roberthalf.com", "randstad.com", "adecco.com", "kellyservices.com",
    "manpower.com", "insightglobal.com", "astoncarter.com", "actalentservices.com",
    "kforce.com", "teksystems.com", "apexsystemsinc.com", "collabera.com",
    "volt.com", "yoh.com", "cybercoders.com", "artechinfo.com", "mindlance.com",
    "mastechdigital.com", "ust-global.com", "sysmind.com", "diverselynx.com",
    "compunnel.com", "genpact.com",
]

REQUIRE_DIRECT_EMPLOYER = True   # only keep postings confirmed as direct company hires

# ---- Sources ----
# 1) Company career-page pattern search via Google Custom Search (site-restricted to common ATS platforms)
ATS_DOMAINS = [
    "boards.greenhouse.io",
    "jobs.lever.co",
    "myworkdayjobs.com",
    "jobs.smartrecruiters.com",
    "recruiting.paylocity.com",
    "careers.icims.com",
    "jobs.jobvite.com",
    "*.bamboohr.com",
    "ashbyhq.com",
]

# 2) Niche/direct L&D job boards to crawl directly (no LinkedIn/Indeed)
NICHE_BOARDS = [
    {"name": "ATD Job Bank", "url": "https://jobs.td.org/jobs/"},
    {"name": "Teamed for Learning", "url": "https://www.teamedforlearning.com/job-board/"},
    {"name": "Remote Rocketship - L&D", "url": "https://www.remoterocketship.com/us/jobs/learning-and-development/"},
    {"name": "Remotive - Education", "url": "https://remotive.com/remote-jobs/education"},
    {"name": "We Work Remotely", "url": "https://weworkremotely.com/categories/remote-management-and-finance-jobs"},
    {"name": "HigherEdJobs", "url": "https://www.higheredjobs.com/search/advanced_action.cfm?Keyword=instructional+designer"},
]

# ---- Schedule ----
RUN_DAYS = ["Mon", "Wed", "Fri"]   # as requested; can add "Sat" for a weekend catch-up
RUN_TIME_LOCAL = "07:30"           # 24h local time, Tucson/MST

# ---- Delivery ----
DELIVERY_METHOD = "email"          # email digest per clarifying-question answer
EMAIL_TO = "REPLACE_ME@example.com"
EMAIL_SUBJECT_PREFIX = "[ID Job Agent]"
