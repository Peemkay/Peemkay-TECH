"""Static content for the portfolio site.

Kept as plain Python data structures (rather than a database) since this
content changes rarely and ships with the code. Edit the lists/dicts below
to update copy across the site.
"""

NAV_LINKS = [
    {"label": "Home", "endpoint": "home"},
    {"label": "About", "endpoint": "about"},
    {"label": "Skills", "endpoint": "skills"},
    {"label": "Services", "endpoint": "services"},
    {"label": "Sectors", "endpoint": "sectors"},
    {"label": "Projects", "endpoint": "projects"},
    {"label": "Contact", "endpoint": "contact"},
]

STATS = [
    {"value": "10+", "label": "Software Systems Shipped"},
    {"value": "6+", "label": "Sectors Served"},
    {"value": "3", "label": "Platforms — Web, Mobile & Desktop"},
    {"value": "100%", "label": "Security-First Engineering"},
]

VALUE_PROPS = [
    {
        "icon": "shield",
        "title": "Security-First Engineering",
        "text": (
            "Every system is designed with authentication, data protection and "
            "access control in mind from day one — not bolted on afterward. "
            "Experience building software that has to earn trust in sensitive, "
            "regulated environments."
        ),
    },
    {
        "icon": "layers",
        "title": "Cross-Platform Versatility",
        "text": (
            "One engineer, every surface — responsive web apps, native-feel "
            "Android & Windows apps with Flutter, and Python backends that tie "
            "it all together with clean REST APIs."
        ),
    },
    {
        "icon": "globe",
        "title": "Sector Fluency",
        "text": (
            "From defense-signal communications to fashion e-commerce, the "
            "same engineering discipline adapts to each industry's real "
            "constraints — offline reliability, payments, compliance, uptime."
        ),
    },
    {
        "icon": "check-circle",
        "title": "Reliable Delivery",
        "text": (
            "Clear scoping, honest timelines, and production-ready code — "
            "documented, tested where it matters, and built to be handed over "
            "or maintained long after launch."
        ),
    },
]

# ---------------------------------------------------------------------------
# Skills
# ---------------------------------------------------------------------------
SKILL_GROUPS = [
    {
        "title": "Languages",
        "icon": "code",
        "skills": ["Python", "Dart", "JavaScript", "PHP", "Java", "SQL", "HTML5 & CSS3"],
    },
    {
        "title": "Frameworks & Libraries",
        "icon": "layers",
        "skills": ["Flask", "Django", "Flutter", "Laravel", "REST APIs", "Jinja2", "Bootstrap"],
    },
    {
        "title": "AI & Computer Vision",
        "icon": "eye",
        "skills": ["DeepFace", "OpenCV", "Facial Recognition Pipelines", "TensorFlow / Keras"],
    },
    {
        "title": "Security & Identity",
        "icon": "shield",
        "skills": [
            "Biometric Authentication",
            "Role-Based Access Control",
            "Secure Session Management",
            "Offline-First Data Sync",
        ],
    },
    {
        "title": "Data & Storage",
        "icon": "database",
        "skills": ["PostgreSQL", "SQLite", "MySQL", "Firebase"],
    },
    {
        "title": "Platforms",
        "icon": "cpu",
        "skills": ["Android", "Windows Desktop", "Web", "Cross-Platform (Flutter)"],
    },
    {
        "title": "Tools & Workflow",
        "icon": "tool",
        "skills": ["Git & GitHub", "VS Code", "Android Studio", "Postman", "Linux", "PythonAnywhere"],
    },
]

# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------
SERVICES = [
    {
        "slug": "custom-software",
        "icon": "code",
        "title": "Custom Software Development",
        "summary": "Purpose-built web, mobile and desktop applications designed around how your organisation actually works.",
        "bullets": [
            "Requirements discovery & technical architecture",
            "Web applications (Flask / Django)",
            "Cross-platform mobile & desktop apps (Flutter)",
            "Clean handover documentation",
        ],
    },
    {
        "slug": "defense-solutions",
        "icon": "shield",
        "title": "Government & Defense Technology Solutions",
        "summary": "Secure, offline-capable systems engineered for signal units, command structures and other defense & government operations.",
        "bullets": [
            "Secure communications & dispatch management platforms",
            "Biometric identity verification & access control",
            "Offline-first, low-connectivity resilient design",
            "Confidential engagements with NDA-based workflows",
        ],
    },
    {
        "slug": "ai-computer-vision",
        "icon": "eye",
        "title": "AI & Computer Vision Solutions",
        "summary": "Facial recognition, identity verification and vision pipelines built for real deployment conditions, not just demos.",
        "bullets": [
            "Facial verification & biometric matching",
            "DeepFace / OpenCV powered pipelines",
            "On-device and server-side inference options",
            "Cross-platform integration (mobile, web, desktop)",
        ],
    },
    {
        "slug": "ecommerce-platforms",
        "icon": "shopping-bag",
        "title": "E-Commerce & Business Platforms",
        "summary": "Full storefronts with inventory, order management and locally-relevant payment flows — not just a template shop.",
        "bullets": [
            "Product catalogue, cart & checkout",
            "Region-based shipping & manual/bank-transfer payments",
            "Admin dashboards for day-to-day store management",
            "Order tracking & customer accounts",
        ],
    },
    {
        "slug": "mobile-apps",
        "icon": "smartphone",
        "title": "Cross-Platform Mobile App Development",
        "summary": "A single Flutter codebase delivering consistent, native-feel apps across Android, Windows and the web.",
        "bullets": [
            "Flutter apps for Android, Windows & Web",
            "Offline-first architecture & local data sync",
            "Platform-aware UI that still feels native",
            "Play Store / enterprise distribution support",
        ],
    },
    {
        "slug": "api-integration",
        "icon": "git-merge",
        "title": "API Development & Systems Integration",
        "summary": "REST APIs and integration layers that connect your existing tools, databases and third-party services reliably.",
        "bullets": [
            "REST API design & implementation",
            "Third-party service & payment integrations",
            "Database design (PostgreSQL / MySQL / SQLite)",
            "Legacy system integration",
        ],
    },
    {
        "slug": "support-consulting",
        "icon": "life-buoy",
        "title": "Maintenance, Support & Consulting",
        "summary": "Ongoing support, security reviews and technical consulting for systems already in production.",
        "bullets": [
            "Bug fixes & feature iteration",
            "Performance & security review",
            "Deployment & hosting setup (incl. PythonAnywhere)",
            "Technical advisory for new projects",
        ],
    },
]

# ---------------------------------------------------------------------------
# Sectors
# ---------------------------------------------------------------------------
SECTORS = [
    {
        "title": "Government & Defense",
        "icon": "shield",
        "image": "covers/sector-defense.png",
        "proven": True,
        "text": (
            "Secure communications, dispatch management and biometric identity "
            "verification systems built for defense signal units. Engagements "
            "in this sector are handled under strict confidentiality — project "
            "names and public details shown here are limited to what is "
            "already publicly shareable."
        ),
        "projects": ["E-COMCEN / NASDS", "NAFacial"],
    },
    {
        "title": "Education",
        "icon": "book-open",
        "image": "covers/sector-education.png",
        "proven": True,
        "text": "Student and academic portals that make information access and administration simpler for institutions and learners alike.",
        "projects": ["NASS Student Portal"],
    },
    {
        "title": "E-Commerce & Retail",
        "icon": "shopping-bag",
        "image": "covers/sector-ecommerce.png",
        "proven": True,
        "text": "Full production storefronts with catalogue, cart, checkout, regional shipping and payment workflows tailored to local markets.",
        "projects": ["Swagcitybymercy"],
    },
    {
        "title": "Enterprise & Professional Services",
        "icon": "briefcase",
        "image": "covers/sector-enterprise.png",
        "proven": True,
        "text": "Digital platforms for service-based businesses — from marketing sites to internal tools that streamline operations.",
        "projects": ["Peemkay-SOFTTECH"],
    },
    {
        "title": "Media & Entertainment",
        "icon": "music",
        "image": "covers/sector-media.png",
        "proven": True,
        "text": "Content-driven web platforms built for scale, discoverability and a smooth reading/browsing experience.",
        "projects": ["9jawavelyrics"],
    },
    {
        "title": "Healthcare",
        "icon": "activity",
        "image": "covers/sector-healthcare.png",
        "proven": False,
        "text": "Ready to bring the same security-first, offline-resilient engineering approach to patient records, scheduling and clinical workflow tools.",
        "projects": [],
    },
    {
        "title": "Finance & Fintech",
        "icon": "credit-card",
        "image": "covers/sector-fintech.png",
        "proven": False,
        "text": "Available for secure transaction platforms, dashboards and financial tooling that demand accuracy and strong access control.",
        "projects": [],
    },
    {
        "title": "Startups & New Ventures",
        "icon": "trending-up",
        "image": "covers/sector-startups.png",
        "proven": False,
        "text": "MVP-to-production builds for founders who need a technical partner who can design, build and ship without hand-holding.",
        "projects": [],
    },
]

# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------
PROJECTS = [
    {
        "slug": "e-comcen",
        "image": "covers/project-e-comcen.png",
        "title": "E-COMCEN / NASDS",
        "category": "defense",
        "category_label": "Government & Defense",
        "confidential": True,
        "summary": (
            "Secure communications and dispatch management platform for a "
            "military signal corps — admin and dispatcher applications with "
            "offline-first sync."
        ),
        "description": (
            "A comprehensive dispatch and communications management system "
            "built for defense signal units, comprising a main administration "
            "application and a companion dispatcher app. Handles incoming, "
            "outgoing, local and external dispatch logging with full "
            "offline-capable synchronisation."
        ),
        "highlights": [
            "Biometric authentication & session security",
            "Offline-first architecture with background sync",
            "Multi-language support",
            "Separate admin & dispatcher applications sharing one data model",
        ],
        "tech": ["Flutter", "Dart", "SQLite", "Biometric Auth"],
        "repo": "https://github.com/Peemkay/e-comcen",
    },
    {
        "slug": "nafacial",
        "image": "covers/project-nafacial.png",
        "title": "NAFacial",
        "category": "defense",
        "category_label": "Government & Defense · AI",
        "confidential": True,
        "summary": (
            "Cross-platform biometric facial verification system for "
            "identity authentication and access control."
        ),
        "description": (
            "A facial verification application built for consistent behaviour "
            "across Android, Windows and web, using a Python-based computer "
            "vision pipeline for face matching alongside a harmonised Flutter "
            "design system across platforms."
        ),
        "highlights": [
            "DeepFace / OpenCV powered recognition pipeline",
            "Consistent UX across Android, Windows & Web",
            "Platform-aware component library",
            "Built for identity verification & access-control workflows",
        ],
        "tech": ["Flutter", "Python", "DeepFace", "OpenCV", "Computer Vision"],
        "repo": "https://github.com/Peemkay/nafacial",
    },
    {
        "slug": "swagcitybymercy",
        "image": "covers/project-swagcitybymercy.png",
        "title": "Swagcitybymercy",
        "category": "ecommerce",
        "category_label": "E-Commerce",
        "confidential": False,
        "summary": (
            "Production Django e-commerce platform for a Lagos-based luxury "
            "apparel boutique with local payment workflows."
        ),
        "description": (
            "A full storefront built for a real fashion boutique — product "
            "catalogue with size/stock-aware carts, region-based shipping, "
            "manual bank-transfer payment confirmation, order tracking and a "
            "complete admin panel for day-to-day store operations."
        ),
        "highlights": [
            "Naira bank-transfer checkout with proof-of-payment upload",
            "Region-based shipping (Lagos / Nigeria / International)",
            "Full admin panel — products, stock, orders, settings",
            "Guest checkout & customer order-history dashboard",
        ],
        "tech": ["Python", "Django", "PostgreSQL", "Bootstrap"],
        "repo": "https://github.com/Peemkay/Swagcitybymercy",
    },
    {
        "slug": "peemkay-softtech",
        "image": "covers/project-peemkay-softtech.png",
        "title": "Peemkay-SOFTTECH",
        "category": "web",
        "category_label": "Enterprise",
        "confidential": False,
        "summary": "Digital services platform presenting web, mobile and desktop development offerings across industries.",
        "description": (
            "A services and capability showcase built to present software "
            "development offerings — web, mobile and desktop — to prospective "
            "clients across multiple industries."
        ),
        "highlights": [
            "Multi-service capability showcase",
            "Cross-platform build",
            "Industry-agnostic positioning",
        ],
        "tech": ["Flutter", "Dart"],
        "repo": "https://github.com/Peemkay/Peemkay-SOFTTECH",
    },
    {
        "slug": "nass-portal",
        "image": "covers/project-nass-portal.png",
        "title": "NASS Student Portal",
        "category": "web",
        "category_label": "Education",
        "confidential": False,
        "summary": "A student/academic web portal for institutional information access and administration.",
        "description": (
            "A web-based student portal designed to simplify how learners and "
            "administrators interact with academic records and institutional "
            "information."
        ),
        "highlights": [
            "Student-facing information portal",
            "Simplified academic administration",
        ],
        "tech": ["HTML5", "CSS3", "JavaScript"],
        "repo": "https://github.com/Peemkay/nass_portal",
    },
    {
        "slug": "pidiread",
        "image": "covers/project-pidiread.png",
        "title": "PidiRead",
        "category": "mobile",
        "category_label": "Mobile · Productivity",
        "confidential": False,
        "summary": "A mobile app for organising and reading PDF documents on the go.",
        "description": (
            "A Flutter productivity app focused on helping users organise, "
            "browse and read PDF files with a clean, distraction-free reading "
            "experience."
        ),
        "highlights": [
            "Local PDF library organisation",
            "Smooth in-app reading experience",
        ],
        "tech": ["Flutter", "Dart"],
        "repo": "https://github.com/Peemkay/PidiRead",
    },
    {
        "slug": "laravel-gvk",
        "image": "covers/project-laravel-gvk.png",
        "title": "laravel-gvk",
        "category": "opensource",
        "category_label": "Open Source · Dev Tools",
        "confidential": False,
        "summary": "An open-source toolkit that simplifies Laravel development workflows.",
        "description": (
            "A developer tool offering powerful utilities and seamless "
            "integration for more efficient Laravel project workflows — "
            "shared publicly for the wider PHP/Laravel community."
        ),
        "highlights": [
            "Streamlined Laravel developer workflow",
            "Published as open source",
        ],
        "tech": ["PHP", "Laravel"],
        "repo": "https://github.com/Peemkay/laravel-gvk",
    },
    {
        "slug": "9jawavelyrics",
        "image": "covers/project-9jawavelyrics.png",
        "title": "9jawavelyrics",
        "category": "web",
        "category_label": "Media & Entertainment",
        "confidential": False,
        "summary": "A content-driven web platform for browsing song lyrics at scale.",
        "description": (
            "A media-focused web application serving lyric content with a "
            "fast, browsable interface built for a high volume of pages."
        ),
        "highlights": [
            "High-volume content browsing",
            "Fast, search-friendly page structure",
        ],
        "tech": ["JavaScript", "HTML5", "CSS3"],
        "repo": "https://github.com/Peemkay/9jawavelyrics",
    },
]

PROJECT_CATEGORIES = [
    {"key": "all", "label": "All Projects"},
    {"key": "defense", "label": "Government & Defense"},
    {"key": "ecommerce", "label": "E-Commerce"},
    {"key": "web", "label": "Web Platforms"},
    {"key": "mobile", "label": "Mobile"},
    {"key": "opensource", "label": "Open Source"},
]

# ---------------------------------------------------------------------------
# About page
# ---------------------------------------------------------------------------
APPROACH_STEPS = [
    {
        "title": "Discover",
        "text": "Understand the real problem, constraints and stakeholders before writing a line of code — including compliance or confidentiality requirements.",
    },
    {
        "title": "Design",
        "text": "Architect the system: data models, security boundaries, and the platforms it needs to run on.",
    },
    {
        "title": "Develop",
        "text": "Build in focused, reviewable increments with clean, documented code — not throwaway prototypes.",
    },
    {
        "title": "Secure & Test",
        "text": "Validate authentication, access control and edge cases — especially for offline, low-connectivity or sensitive environments.",
    },
    {
        "title": "Deploy",
        "text": "Ship to production with proper configuration, monitoring and a clear handover.",
    },
    {
        "title": "Support",
        "text": "Stay available for fixes, iteration and scaling as the project's needs grow.",
    },
]

CORE_VALUES = [
    {
        "title": "Security by Design",
        "text": "Authentication, access control and data protection are part of the architecture, not an afterthought.",
    },
    {
        "title": "Confidentiality",
        "text": "Government, defense and enterprise clients get NDA-respecting workflows and discretion by default.",
    },
    {
        "title": "Cross-Sector Versatility",
        "text": "The same rigor applies whether the system serves a signal unit or a fashion boutique.",
    },
    {
        "title": "Clean, Maintainable Engineering",
        "text": "Code that the next developer — or future you — can actually read, extend and trust.",
    },
]
