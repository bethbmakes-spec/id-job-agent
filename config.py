"""
Configuration for the Instructional Design / L&D Job Search Agent.
Edit the lists below to tune the search — no code changes needed elsewhere.
"""

# Expanded roles you’re a fit for (instructional/creative + LMS + T&D)

TARGET_TITLES = [
    # Core ID / LXD
    "Senior Instructional Designer",
    "Sr. Instructional Designer",
    "Lead Instructional Designer",
    "Instructional Designer",
    "Instructional Design Consultant",
    "Learning Experience Designer",
    "Senior Learning Experience Designer",
    "Learning Designer",
    "Senior Learning Designer",
    "Curriculum Designer",
    "Curriculum Developer",
    "Senior Curriculum Developer",
    "Instructional Technologist",
    "Educational Technologist",
    "Learning Technologist",

    # LMS / platforms
    "Senior LMS Administrator",
    "LMS Administrator",
    "Learning Management System Administrator",
    "LMS Manager",
    "Learning Systems Manager",
    "Learning Technology Manager",

    # Training / L&D leadership (still creative side, not HR generalist)
    "Training Manager",
    "Senior Training Manager",
    "Learning and Development Manager",
    "L&D Manager",
    "Learning Programs Manager",
    "Enablement Manager",
    "Learning Architect",
    "Senior Learning Architect",
    "Learning Consultant",

    # Strategy / solutions roles adjacent to ID
    "Learning Solutions Architect",
    "Learning Strategist",
    "Learning Experience Architect",
]

# Salary floor (relaxed to 90k; scoring still favors higher bands)
MIN_SALARY = 90000

# Currently not excluding by generic keyword; we handle undesired roles via
# company / agency / defense filters instead.
EXCLUDE_KEYWORDS = []
EXCLUDE_UNLESS_REMOTE = False

# Preferences used in scoring (already wired up in scraper.py)
REQUIRE_BENEFITS_MENTION = True
PREFER_BONUS_MENTION = True
PREFER_REMOTE = True

# ATS / company career sites searched via Google Custom Search
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

# Niche L&D / training job boards and communities (no LinkedIn/Indeed)
NICHE_BOARDS = [
    {"name": "ATD Job Bank", "url": "https://jobs.td.org/jobs/", "parser": "generic_links"},
    {"name": "Teamed for Learning", "url": "https://www.teamedforlearning.com/job-board/", "parser": "generic_links"},
    {"name": "Remote Rocketship - L&D", "url": "https://www.remoterocketship.com/us/jobs/learning-and-development", "parser": "remoterocketship"},
    {"name": "Remotive - Education", "url": "https://remotive.com/remote-jobs/education", "parser": "remotive"},
    # Higher ed / instructional tech & design
    {"name": "HigherEdJobs - Instructional Tech & Design", "url": "https://www.higheredjobs.com/admin/search.cfm?JobCat=218", "parser": "generic_links"},
    # EdTech-focused ID & L&D roles
    {"name": "EdTech - Instructional Design Jobs", "url": "https://www.edtech.com/jobs/instructional-design-jobs", "parser": "generic_links"},
    {"name": "EdTech - Learning & Development Jobs", "url": "https://www.edtech.com/jobs/learning-development-jobs", "parser": "generic_links"},
    # eLearning / vendor ecosystem boards
    {"name": "eLearning Industry Jobs", "url": "https://elearningindustry.com/jobs", "parser": "generic_links"},
    {"name": "Docebo Learning Career Board", "url": "https://community.docebo.com/the-learning-career-board-55", "parser": "generic_links"},
]

# Schedule preferences (used for docs / reference; actual scheduling is via GitHub Actions)
RUN_DAYS = ["Mon", "Wed", "Fri"]
RUN_TIME_LOCAL = "07:30"  # Arizona time

# Delivery settings
DELIVERY_METHOD = "email"
EMAIL_TO = "REPLACE_ME@example.com"
EMAIL_SUBJECT_PREFIX = "[ID Job Agent]"

# ---- Exclusion rules (same as your current file) ----

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

STAFFING_AGENCY_KEYWORDS = [
    "staffing agency", "staffing firm", "recruiting agency", "recruitment agency",
    "talent agency", "on behalf of our client", "our client is seeking",
    "one of our clients", "c2c", "corp to corp", "contract to hire staffing",
    "robert half", "randstad", "adecco", "kelly services", "manpower",
    "insight global", "aston carter", "actalent", "kforce", "teksystems",
    "apex systems", "collabera", "volt technical", "yoh", "cybercoders",
    "artech", "mindlance", "hexaware staffing", "ust global staffing",
]

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

EXCLUDE_DOMAINS = [
    "roberthalf.com", "randstad.com", "adecco.com", "kellyservices.com",
    "manpower.com", "insightglobal.com", "astoncarter.com", "actalentservices.com",
    "kforce.com", "teksystems.com", "apexsystemsinc.com", "collabera.com",
    "volt.com", "yoh.com", "cybercoders.com", "artechinfo.com", "mindlance.com",
    "mastechdigital.com", "ust-global.com", "sysmind.com", "diverselynx.com",
    "compunnel.com", "genpact.com",
]

REQUIRE_DIRECT_EMPLOYER = True
