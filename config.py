"""Configuration for the creative Instructional Design Job Search Agent."""

# Creative design/development roles only. LMS administration has been removed.
TARGET_TITLES = [
    "Senior Instructional Designer", "Sr. Instructional Designer",
    "Lead Instructional Designer", "Principal Instructional Designer",
    "Instructional Design Manager", "Senior Course Developer",
    "Course Developer", "Senior Learning Experience Designer",
    "Learning Experience Designer", "Learning Experience Design Manager",
    "Learning Architect", "Senior Learning Architect",
    "Senior eLearning Developer", "eLearning Developer",
    "Digital Learning Designer", "Senior Digital Learning Designer",
    "Curriculum Designer", "Senior Curriculum Designer",
    "Curriculum Developer", "Senior Curriculum Developer",
    "Training Content Developer", "Learning Content Designer",
    "Multimedia Learning Designer", "Learning Design Manager",
    "Director of Instructional Design", "Director of Learning Experience",
]

# Fully remote jobs: a stated range qualifies only when its lower bound is at
# least $90,000. Unknown-salary postings are retained but clearly flagged.
REMOTE_MIN_SALARY = 90000
ALLOW_UNKNOWN_REMOTE_SALARY = True

# Hybrid/onsite jobs: retain only when pay can reach at least $125,000 AND the
# posting explicitly offers relocation assistance. Onsite without relocation
# is always excluded.
HYBRID_MIN_SALARY = 125000
REQUIRE_RELOCATION_FOR_HYBRID = True

REQUIRE_BENEFITS_MENTION = False
PREFER_BONUS_MENTION = True

# Title/function exclusions. These are checked primarily against the title,
# preventing creative roles from being rejected merely for mentioning an LMS.
EXCLUDED_TITLE_PHRASES = [
    "lms administrator", "learning management system administrator",
    "lms analyst", "lms specialist", "lms coordinator", "lms manager",
    "learning systems administrator", "learning systems analyst",
    "platform administrator", "system administrator",
]
EXCLUDED_COMPANIES = ["docebo"]

EXCLUDE_KEYWORDS = ["tax", "taxation", "tax preparer", "tax accountant"]
EXCLUDE_UNLESS_REMOTE = True

# Aggregator result pages are not accepted. The final URL must be a specific,
# openable vacancy/application page from the direct employer or its ATS.
EXCLUDED_SOURCE_NAMES = ["remote rocketship"]
EXCLUDED_AGGREGATOR_DOMAINS = [
    "remoterocketship.com", "linkedin.com", "indeed.com", "ziprecruiter.com",
    "glassdoor.com", "simplyhired.com", "monster.com", "careerbuilder.com",
]
REQUIRE_SPECIFIC_JOB_URL = True
REQUIRE_DIRECT_EMPLOYER = True

ATS_DOMAINS = [
    "boards.greenhouse.io", "job-boards.greenhouse.io", "jobs.lever.co",
    "myworkdayjobs.com", "jobs.smartrecruiters.com", "recruiting.paylocity.com",
    "careers.icims.com", "jobs.jobvite.com", "bamboohr.com", "ashbyhq.com",
]

# Remote Rocketship and Docebo have been removed. Board pages may be used only
# to discover a vacancy; the result survives only if it resolves to the direct
# employer's specific vacancy page.
NICHE_BOARDS = [
    {"name": "ATD Job Bank", "url": "https://jobs.td.org/jobs/", "parser": "generic_links"},
    {"name": "Teamed for Learning", "url": "https://www.teamedforlearning.com/job-board/", "parser": "generic_links"},
    {"name": "Remotive - Education", "url": "https://remotive.com/remote-jobs/education", "parser": "remotive"},
    {"name": "We Work Remotely", "url": "https://weworkremotely.com/categories/remote-management-and-finance-jobs", "parser": "weworkremotely"},
    {"name": "HigherEdJobs", "url": "https://www.higheredjobs.com/search/advanced_action.cfm?Keyword=instructional+designer", "parser": "generic_links"},
    {"name": "Built In Remote", "url": "https://builtin.com/jobs/remote/learning-development", "parser": "generic_links"},
    {"name": "Chronicle of Higher Ed", "url": "https://jobs.chronicle.com/search/?q=instructional+designer", "parser": "generic_links"},
    {"name": "eLearning Industry Jobs", "url": "https://elearningindustry.com/jobs", "parser": "generic_links"},
]

RUN_DAYS = ["Mon", "Wed", "Fri"]
RUN_TIME_LOCAL = "07:30"
DELIVERY_METHOD = "email"
EMAIL_TO = "REPLACE_ME@example.com"
EMAIL_SUBJECT_PREFIX = "[Creative ID Job Agent]"

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
