"""
Configuration for the Instructional Design Job Search Agent.
Edit the lists below to tune the search — no code changes needed elsewhere.
"""

TARGET_TITLES = [
    "Senior Instructional Designer", "Sr. Instructional Designer",
    "Lead Instructional Designer", "Instructional Design Manager",
    "Senior LMS Administrator", "LMS Administrator",
    "Senior Course Developer", "Course Developer",
    "Senior Learning Experience Designer", "Learning Experience Designer",
    "Learning Architect", "Senior Learning Architect",
    "Training Manager", "Senior Training Manager",
    "Director of Learning and Development", "Head of Learning and Development",
]

MIN_SALARY = 105000
REQUIRE_BENEFITS_MENTION = True
PREFER_BONUS_MENTION = True
PREFER_REMOTE = True
EXCLUDE_KEYWORDS = ["tax", "taxation", "tax preparer", "tax accountant"]
EXCLUDE_UNLESS_REMOTE = True

ATS_DOMAINS = [
    "boards.greenhouse.io", "jobs.lever.co", "myworkdayjobs.com",
    "jobs.smartrecruiters.com", "recruiting.paylocity.com",
    "careers.icims.com", "jobs.jobvite.com", "*.bamboohr.com", "ashbyhq.com",
]

# Each board now has a "parser" key telling the scraper which extraction
# strategy to use, since generic link-scanning misses most real sites.
NICHE_BOARDS = [
    {"name": "ATD Job Bank", "url": "https://jobs.td.org/jobs/", "parser": "generic_links"},
    {"name": "Teamed for Learning", "url": "https://www.teamedforlearning.com/job-board/", "parser": "generic_links"},
    {"name": "Remote Rocketship - L&D", "url": "https://www.remoterocketship.com/us/jobs/learning-and-development", "parser": "remoterocketship"},
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
EMAIL_SUBJECT_PREFIX = "[ID Job Agent]"

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
