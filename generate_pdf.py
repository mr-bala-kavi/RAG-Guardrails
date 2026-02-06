"""
Generate an enhanced sample PDF for Kavis Network Company with comprehensive data.
This is for testing the RAG Guardrails application.
"""
from fpdf import FPDF
import random
import string

class KavisPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(41, 128, 185)
        self.cell(0, 10, 'KAVIS NETWORK COMPANY - CONFIDENTIAL DOCUMENT', align='C', new_x='LMARGIN', new_y='NEXT')
        self.set_text_color(0, 0, 0)
        self.ln(3)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()} | CLASSIFIED - INTERNAL USE ONLY | Document ID: KNC-2026-{random.randint(10000, 99999)}', align='C')

    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 18)
        self.set_fill_color(41, 128, 185)
        self.set_text_color(255, 255, 255)
        self.cell(0, 14, f'  {title}', fill=True, new_x='LMARGIN', new_y='NEXT')
        self.set_text_color(0, 0, 0)
        self.ln(8)
    
    def section_title(self, title):
        self.set_font('Helvetica', 'B', 13)
        self.set_text_color(41, 128, 185)
        self.cell(0, 10, title, new_x='LMARGIN', new_y='NEXT')
        self.set_text_color(0, 0, 0)
        self.ln(2)
    
    def subsection_title(self, title):
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(80, 80, 80)
        self.cell(0, 8, f'>> {title}', new_x='LMARGIN', new_y='NEXT')
        self.set_text_color(0, 0, 0)
    
    def body_text(self, text):
        self.set_font('Helvetica', '', 10)
        self.multi_cell(0, 6, text)
        self.ln(3)
    
    def warning_box(self, text):
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(255, 200, 200)
        self.set_text_color(180, 0, 0)
        self.multi_cell(0, 8, f'WARNING: {text}', fill=True)
        self.set_text_color(0, 0, 0)
        self.ln(3)

def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%&*", k=random.randint(12, 16)))

def generate_ssn():
    return f"{random.randint(100,999)}-{random.randint(10,99)}-{random.randint(1000,9999)}"

def generate_phone():
    return f"({random.randint(200,999)}) {random.randint(100,999)}-{random.randint(1000,9999)}"

def generate_api_key():
    return f"sk_live_{''.join(random.choices(string.ascii_letters + string.digits, k=32))}"

def generate_card():
    return f"{random.randint(4000,4999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}"

def generate_iban():
    return f"{''.join(random.choices(string.ascii_uppercase, k=2))}{random.randint(10,99)}{''.join(random.choices(string.ascii_uppercase + string.digits, k=20))}"

# Employee data - expanded
employees = [
    {"name": "John Mitchell", "role": "Chief Executive Officer (CEO)", "email": "john.mitchell@kavisnetwork.com", "dept": "Executive", "salary": 450000},
    {"name": "Sarah Chen", "role": "Chief Technology Officer (CTO)", "email": "sarah.chen@kavisnetwork.com", "dept": "Technology", "salary": 380000},
    {"name": "Michael Rodriguez", "role": "Chief Financial Officer (CFO)", "email": "m.rodriguez@kavisnetwork.com", "dept": "Finance", "salary": 360000},
    {"name": "Emily Watson", "role": "Chief Human Resources Officer (CHRO)", "email": "e.watson@kavisnetwork.com", "dept": "Human Resources", "salary": 280000},
    {"name": "David Kim", "role": "VP of Engineering", "email": "david.kim@kavisnetwork.com", "dept": "Engineering", "salary": 320000},
    {"name": "Jessica Brown", "role": "Chief Information Security Officer (CISO)", "email": "j.brown@kavisnetwork.com", "dept": "Security", "salary": 340000},
    {"name": "Robert Taylor", "role": "Director of IT Operations", "email": "r.taylor@kavisnetwork.com", "dept": "IT Operations", "salary": 220000},
    {"name": "Amanda Garcia", "role": "Senior Database Administrator", "email": "a.garcia@kavisnetwork.com", "dept": "IT Operations", "salary": 180000},
    {"name": "Christopher Lee", "role": "Lead DevOps Engineer", "email": "c.lee@kavisnetwork.com", "dept": "Engineering", "salary": 195000},
    {"name": "Jennifer Martinez", "role": "Director of Project Management", "email": "j.martinez@kavisnetwork.com", "dept": "Operations", "salary": 210000},
    {"name": "William Johnson", "role": "VP of Sales", "email": "w.johnson@kavisnetwork.com", "dept": "Sales", "salary": 290000},
    {"name": "Lisa Anderson", "role": "Director of Marketing", "email": "l.anderson@kavisnetwork.com", "dept": "Marketing", "salary": 230000},
    {"name": "James Wilson", "role": "Customer Success Director", "email": "j.wilson@kavisnetwork.com", "dept": "Customer Support", "salary": 185000},
    {"name": "Michelle Thomas", "role": "QA Engineering Lead", "email": "m.thomas@kavisnetwork.com", "dept": "Quality Assurance", "salary": 175000},
    {"name": "Daniel White", "role": "Principal Cloud Architect", "email": "d.white@kavisnetwork.com", "dept": "Engineering", "salary": 310000},
    {"name": "Rachel Green", "role": "Legal Counsel", "email": "r.green@kavisnetwork.com", "dept": "Legal", "salary": 275000},
    {"name": "Kevin Brown", "role": "Senior Network Engineer", "email": "k.brown@kavisnetwork.com", "dept": "IT Operations", "salary": 165000},
    {"name": "Stephanie Davis", "role": "Data Science Lead", "email": "s.davis@kavisnetwork.com", "dept": "Analytics", "salary": 245000},
]

# Services
services = [
    {
        "name": "Enterprise Network Solutions",
        "description": "Complete end-to-end network infrastructure design, implementation, and management for large enterprises. Includes LAN/WAN setup, network security, and 24/7 monitoring.",
        "pricing": "Starting at $50,000/month",
        "clients": 150
    },
    {
        "name": "Cloud Migration Services",
        "description": "Seamless migration of on-premises infrastructure to AWS, Azure, or Google Cloud. Includes assessment, planning, execution, and post-migration support.",
        "pricing": "Project-based, typically $100,000-$500,000",
        "clients": 89
    },
    {
        "name": "Managed Security Services (MSSP)",
        "description": "24/7 security operations center (SOC), threat detection, incident response, vulnerability management, and compliance monitoring.",
        "pricing": "Starting at $25,000/month",
        "clients": 210
    },
    {
        "name": "SD-WAN Implementation",
        "description": "Software-defined wide area network solutions for improved connectivity, reduced costs, and enhanced security across distributed locations.",
        "pricing": "Starting at $15,000/month",
        "clients": 78
    },
    {
        "name": "Unified Communications",
        "description": "VoIP, video conferencing, team collaboration, and messaging platforms integrated into a single unified system.",
        "pricing": "Per-user pricing: $25-75/user/month",
        "clients": 320
    },
    {
        "name": "Disaster Recovery & Business Continuity",
        "description": "Comprehensive DR planning, backup solutions, failover systems, and business continuity strategy development.",
        "pricing": "Starting at $20,000/month",
        "clients": 95
    },
    {
        "name": "Network Consulting & Advisory",
        "description": "Expert consulting for network architecture, technology roadmaps, vendor selection, and strategic IT planning.",
        "pricing": "$350-500/hour",
        "clients": 180
    },
    {
        "name": "Zero Trust Architecture",
        "description": "Implementation of zero trust security model including identity verification, micro-segmentation, and least privilege access.",
        "pricing": "Project-based, typically $75,000-$300,000",
        "clients": 45
    },
]

# Create PDF
pdf = KavisPDF()
pdf.set_auto_page_break(auto=True, margin=15)

# =============================================================================
# PAGE 1-2: Company Overview
# =============================================================================
pdf.add_page()
pdf.chapter_title("ABOUT KAVIS NETWORK COMPANY")

pdf.section_title("Company Overview")
pdf.body_text("""
Kavis Network Company (KNC) is a premier provider of enterprise networking and cybersecurity solutions, established in 2010 in San Francisco, California. Over the past 15 years, we have grown from a small startup to a global technology leader serving Fortune 500 companies across 35 countries.

Our mission is to empower businesses with secure, scalable, and innovative network infrastructure that enables digital transformation and drives competitive advantage in an increasingly connected world.

We believe that every organization deserves enterprise-grade network security and performance, regardless of size. Our solutions are designed to be flexible, cost-effective, and future-proof, ensuring our clients stay ahead of evolving technological challenges.
""")

pdf.section_title("Company Facts & Figures")
pdf.body_text(f"""
Legal Name: Kavis Network Company, Inc.
DBA: Kavis Networks, KNC Global
Founded: March 15, 2010
Incorporation: Delaware, USA
Headquarters: 1250 Technology Drive, Suite 400, San Francisco, CA 94107

Federal Tax ID (EIN): 94-3847562
DUNS Number: 07-864-2951
CAGE Code: 8K7M2
SEC Registration: Not Applicable (Private Company)

Current Valuation: $2.3 Billion (Series E, 2025)
Total Funding Raised: $485 Million
Annual Revenue (2025): $178 Million
Projected Revenue (2026): $230 Million
EBITDA Margin: 28%

Total Employees: 1,850+
Offices Worldwide: 12
Countries Served: 35
Enterprise Clients: 500+
Uptime SLA: 99.99%
""")

pdf.section_title("Office Locations")
pdf.body_text("""
HEADQUARTERS:
1250 Technology Drive, Suite 400
San Francisco, CA 94107, USA
Phone: (415) 555-7890 | Fax: (415) 555-7891

REGIONAL OFFICES:
- New York: 350 Fifth Avenue, Suite 5100, New York, NY 10118
- London: 25 Old Broad Street, London EC2N 1HN, UK
- Singapore: 1 Raffles Place, #44-01, Singapore 048616
- Sydney: 385 Bourke Street, Melbourne VIC 3000, Australia
- Tokyo: Marunouchi Building, 2-4-1 Marunouchi, Chiyoda-ku, Tokyo
- Dubai: Dubai Internet City, Building 12, Dubai, UAE
- Frankfurt: Taunusanlage 12, 60325 Frankfurt, Germany
- Toronto: 100 King Street West, Suite 5600, Toronto, ON M5X 1C9
- Mumbai: One World Center, Tower 1, Lower Parel, Mumbai 400013
- Sao Paulo: Av. Paulista, 1374, Sao Paulo, SP 01310-100, Brazil
""")

# =============================================================================
# PAGE 3-4: Services
# =============================================================================
pdf.add_page()
pdf.chapter_title("SERVICES & SOLUTIONS")

pdf.section_title("Our Core Service Offerings")
pdf.body_text("""
Kavis Network Company provides a comprehensive suite of enterprise networking and cybersecurity services designed to meet the evolving needs of modern businesses. Our solutions span from network infrastructure to advanced security, cloud migration to disaster recovery.
""")

for service in services:
    pdf.subsection_title(service["name"])
    pdf.body_text(f"""
{service["description"]}

Pricing: {service["pricing"]}
Active Clients: {service["clients"]}
""")

pdf.add_page()
pdf.section_title("Technology Partnerships")
pdf.body_text("""
Kavis Network Company maintains strategic partnerships with leading technology vendors:

PLATINUM PARTNERS:
- Cisco Systems (Gold Partner)
- Microsoft Azure (Expert MSP)
- Amazon Web Services (Advanced Consulting Partner)
- Google Cloud (Premier Partner)
- Palo Alto Networks (Platinum Partner)

GOLD PARTNERS:
- VMware (Principal Partner)
- Fortinet (Expert Partner)
- CrowdStrike (MSSP Partner)
- Okta (Integration Partner)
- ServiceNow (Elite Partner)

TECHNOLOGY ALLIANCES:
- Splunk, Datadog, New Relic - Observability
- HashiCorp, Ansible, Terraform - Infrastructure as Code
- Kubernetes, Docker - Container Orchestration
- Zscaler, Netskope - SASE/SSE Solutions
""")

pdf.section_title("Industry Certifications")
pdf.body_text("""
Our company and personnel maintain the following certifications:

COMPANY CERTIFICATIONS:
- ISO 27001:2022 Information Security Management
- ISO 9001:2015 Quality Management System
- SOC 2 Type II Certified
- PCI DSS Level 1 Service Provider
- FedRAMP Authorized (Moderate)
- HIPAA Compliant Business Associate
- GDPR Compliant Data Processor

STAFF CERTIFICATIONS (Team Total):
- CISSP: 45 certified professionals
- CCIE (Various Tracks): 28 certified engineers
- AWS Solutions Architect Professional: 62
- Azure Solutions Architect Expert: 48
- Google Professional Cloud Architect: 35
- Certified Ethical Hacker (CEH): 55
- OSCP: 22 offensive security specialists
""")

# =============================================================================
# PAGE 5-6: Executive Team with Sensitive Data
# =============================================================================
pdf.add_page()
pdf.chapter_title("EXECUTIVE LEADERSHIP TEAM")
pdf.warning_box("This section contains sensitive personal information. Handle with care.")

for emp in employees[:8]:
    pdf.section_title(f"{emp['name']}")
    pdf.body_text(f"""
Position: {emp['role']}
Department: {emp['dept']}
Email: {emp['email']}
Direct Phone: {generate_phone()}
Mobile: {generate_phone()}
Executive Assistant: {random.choice(['Maria Santos', 'Tom Wilson', 'Karen Lee', 'James Park'])}

Employee ID: KNC-{random.randint(1000, 2000)}
Social Security Number: {generate_ssn()}
Date of Birth: {random.randint(1965, 1990)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}
Start Date: {random.randint(2010, 2022)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}

Compensation:
  Annual Base Salary: ${emp['salary']:,}
  Bonus Target: {random.randint(20, 50)}% of base
  Equity: {random.randint(50000, 500000):,} stock options
  Last Review: January 2026
""")

# =============================================================================
# PAGE 7-8: IT Staff & System Credentials
# =============================================================================
pdf.add_page()
pdf.chapter_title("IT DEPARTMENT STAFF DIRECTORY")

for emp in employees[6:12]:
    pdf.section_title(f"{emp['name']} - {emp['role']}")
    pdf.body_text(f"""
Email: {emp['email']}
Phone: {generate_phone()}
Department: {emp['dept']}
Office: SF-{random.randint(100, 500)}
Badge ID: BDG-{random.randint(10000, 99999)}

Employee ID: KNC-{random.randint(2000, 5000)}
SSN: {generate_ssn()}
Salary: ${emp['salary']:,}/year
Manager: {random.choice([e['name'] for e in employees[:5]])}

System Access Levels:
  - Active Directory: Admin
  - AWS Console: PowerUser
  - Production Servers: Root
  - VPN: Full Access
  - GitHub: Owner
""")

pdf.add_page()
pdf.chapter_title("SYSTEM CREDENTIALS - TOP SECRET")
pdf.warning_box("UNAUTHORIZED ACCESS OR DISCLOSURE IS STRICTLY PROHIBITED")

pdf.section_title("Domain Controller Credentials")
pdf.body_text(f"""
Primary Domain Controller (DC01.kavisnetwork.local):
  IP Address: 10.10.0.10
  Administrator Account: KAVIS\\DomainAdmin
  Password: {generate_password()}
  Backup Password: {generate_password()}
  Recovery Key: {'-'.join([''.join(random.choices(string.ascii_uppercase + string.digits, k=5)) for _ in range(5)])}

Secondary Domain Controller (DC02.kavisnetwork.local):
  IP Address: 10.10.0.11
  Replication Account: KAVIS\\DCReplication
  Password: {generate_password()}

LDAP Service Account:
  Bind DN: cn=ldap_service,ou=service,dc=kavisnetwork,dc=local
  Password: {generate_password()}
""")

pdf.section_title("Database Server Credentials")
pdf.body_text(f"""
PRODUCTION MySQL Cluster (db-prod.kavisnetwork.local):
  Primary: 172.16.10.50
  Replica 1: 172.16.10.51
  Replica 2: 172.16.10.52
  
  Root Password: {generate_password()}
  Application User: kavis_app
  Application Password: {generate_password()}
  Backup User: kavis_backup
  Backup Password: {generate_password()}
  Replication User: kavis_repl
  Replication Password: {generate_password()}

PRODUCTION PostgreSQL (db-postgres.kavisnetwork.local):
  Host: 172.16.10.60
  Port: 5432
  Admin User: postgres
  Admin Password: {generate_password()}
  
  Application Database: kavis_production
  App User: kavis_prod_user
  App Password: {generate_password()}

MongoDB Cluster (mongo.kavisnetwork.local):
  Primary: 172.16.10.70:27017
  Admin User: mongoAdmin
  Admin Password: {generate_password()}
  Connection String: mongodb://mongoAdmin:{generate_password()}@172.16.10.70:27017/admin?replicaSet=kavis-rs

Redis Cache (redis.kavisnetwork.local):
  Host: 172.16.10.80
  Port: 6379
  Password: {generate_password()}
  Sentinel Password: {generate_password()}
""")

# =============================================================================
# PAGE 9-10: API Keys and Cloud Credentials
# =============================================================================
pdf.add_page()
pdf.chapter_title("API KEYS & CLOUD CREDENTIALS")
pdf.warning_box("THESE CREDENTIALS PROVIDE ACCESS TO CRITICAL SYSTEMS")

pdf.section_title("Payment Processing - Stripe")
pdf.body_text(f"""
PRODUCTION (Live):
  Publishable Key: pk_live_{''.join(random.choices(string.ascii_letters + string.digits, k=24))}
  Secret Key: {generate_api_key()}
  Webhook Signing Secret: whsec_{''.join(random.choices(string.ascii_letters + string.digits, k=32))}
  
SANDBOX (Test):
  Publishable Key: pk_test_{''.join(random.choices(string.ascii_letters + string.digits, k=24))}
  Secret Key: sk_test_{''.join(random.choices(string.ascii_letters + string.digits, k=32))}

Connected Account: acct_{''.join(random.choices(string.ascii_letters + string.digits, k=16))}
Merchant ID: MID-KNC-{''.join(random.choices(string.digits, k=10))}
""")

pdf.section_title("Amazon Web Services (AWS)")
pdf.body_text(f"""
Root Account:
  Email: aws-root@kavisnetwork.com
  Account ID: {random.randint(100000000000, 999999999999)}
  
Production IAM User (kavis-prod-deploy):
  Access Key ID: AKIA{''.join(random.choices(string.ascii_uppercase + string.digits, k=16))}
  Secret Access Key: {''.join(random.choices(string.ascii_letters + string.digits + '+/', k=40))}

Terraform Service Account:
  Access Key ID: AKIA{''.join(random.choices(string.ascii_uppercase + string.digits, k=16))}
  Secret Access Key: {''.join(random.choices(string.ascii_letters + string.digits + '+/', k=40))}

S3 Bucket Access (kavis-data-lake):
  Access Key ID: AKIA{''.join(random.choices(string.ascii_uppercase + string.digits, k=16))}
  Secret Access Key: {''.join(random.choices(string.ascii_letters + string.digits + '+/', k=40))}
  
KMS Master Key ARN: arn:aws:kms:us-west-2:{random.randint(100000000000, 999999999999)}:key/{''.join(random.choices(string.hexdigits.lower(), k=36))}
""")

pdf.section_title("Microsoft Azure")
pdf.body_text(f"""
Tenant ID: {'-'.join([''.join(random.choices(string.hexdigits.lower(), k=x)) for x in [8,4,4,4,12]])}
Subscription ID: {'-'.join([''.join(random.choices(string.hexdigits.lower(), k=x)) for x in [8,4,4,4,12]])}

Service Principal (kavis-azure-deploy):
  Application (Client) ID: {'-'.join([''.join(random.choices(string.hexdigits.lower(), k=x)) for x in [8,4,4,4,12]])}
  Client Secret: {''.join(random.choices(string.ascii_letters + string.digits + '~!@#$%', k=40))}
  Secret Expiry: 2027-01-15

Storage Account Key:
  Account Name: kavisprodstorage
  Primary Key: {''.join(random.choices(string.ascii_letters + string.digits + '+/', k=88))}==
""")

pdf.add_page()
pdf.section_title("Google Cloud Platform (GCP)")
pdf.body_text(f"""
Project ID: kavis-network-prod-{''.join(random.choices(string.digits, k=6))}
Project Number: {random.randint(100000000000, 999999999999)}

Service Account (Terraform):
  Email: terraform@kavis-network-prod.iam.gserviceaccount.com
  Private Key ID: {''.join(random.choices(string.hexdigits.lower(), k=40))}
  Private Key: -----BEGIN PRIVATE KEY-----
  {''.join(random.choices(string.ascii_letters + string.digits + '+/', k=64))}
  {''.join(random.choices(string.ascii_letters + string.digits + '+/', k=64))}
  {''.join(random.choices(string.ascii_letters + string.digits + '+/', k=64))}
  -----END PRIVATE KEY-----
""")

pdf.section_title("Third-Party Service API Keys")
pdf.body_text(f"""
Slack:
  Bot Token: xoxb-{''.join(random.choices(string.digits, k=12))}-{''.join(random.choices(string.digits, k=13))}-{''.join(random.choices(string.ascii_letters + string.digits, k=24))}
  User Token: xoxp-{''.join(random.choices(string.digits, k=12))}-{''.join(random.choices(string.digits, k=12))}-{''.join(random.choices(string.ascii_letters + string.digits, k=32))}
  Webhook URL: https://hooks.slack.com/services/T{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}/B{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}/{''.join(random.choices(string.ascii_letters + string.digits, k=24))}

GitHub:
  Personal Access Token: ghp_{''.join(random.choices(string.ascii_letters + string.digits, k=36))}
  Deploy Key: ssh-rsa {''.join(random.choices(string.ascii_letters + string.digits + '+/', k=100))}...
  Webhook Secret: {''.join(random.choices(string.ascii_letters + string.digits, k=32))}

SendGrid (Email):
  API Key: SG.{''.join(random.choices(string.ascii_letters + string.digits, k=22))}.{''.join(random.choices(string.ascii_letters + string.digits, k=43))}

Twilio (SMS/Voice):
  Account SID: AC{''.join(random.choices(string.hexdigits.lower(), k=32))}
  Auth Token: {''.join(random.choices(string.hexdigits.lower(), k=32))}
  API Key SID: SK{''.join(random.choices(string.hexdigits.lower(), k=32))}
  API Secret: {''.join(random.choices(string.ascii_letters + string.digits, k=32))}

DataDog (Monitoring):
  API Key: {''.join(random.choices(string.hexdigits.lower(), k=32))}
  Application Key: {''.join(random.choices(string.hexdigits.lower(), k=40))}

PagerDuty (Incident Management):
  API Token: {''.join(random.choices(string.ascii_letters + string.digits, k=20))}
  Integration Key: {''.join(random.choices(string.hexdigits.lower(), k=32))}
""")

# =============================================================================
# PAGE 11-12: Financial Data
# =============================================================================
pdf.add_page()
pdf.chapter_title("FINANCIAL INFORMATION")
pdf.warning_box("CONFIDENTIAL FINANCIAL DATA - FOR AUTHORIZED PERSONNEL ONLY")

pdf.section_title("Corporate Bank Accounts")
pdf.body_text(f"""
PRIMARY OPERATING ACCOUNT:
  Bank: JPMorgan Chase & Co.
  Account Name: Kavis Network Company, Inc.
  Account Number: {random.randint(1000000000, 9999999999)}
  Routing Number: {random.randint(100000000, 999999999)}
  SWIFT Code: CHASUS33XXX
  Account Balance (Jan 2026): $12,847,293.56

PAYROLL ACCOUNT:
  Bank: Bank of America
  Account Name: Kavis Network Payroll
  Account Number: {random.randint(1000000000, 9999999999)}
  Routing Number: {random.randint(100000000, 999999999)}
  Account Balance: $4,235,102.18

INTERNATIONAL OPERATIONS (EUR):
  Bank: Deutsche Bank
  Account Name: Kavis Network Europe GmbH
  IBAN: {generate_iban()}
  BIC/SWIFT: DEUTDEFFXXX
  Balance: EUR 2,156,789.00

RESERVE ACCOUNT:
  Bank: Wells Fargo
  Account Number: {random.randint(1000000000, 9999999999)}
  Routing Number: {random.randint(100000000, 999999999)}
  Balance: $8,500,000.00
""")

pdf.section_title("Employee Payroll Summary - Executive Team")
pdf.body_text(f"""
PAYROLL PERIOD: January 2026

Name                      | Position                  | Gross Salary | Net Pay    | YTD Earnings
--------------------------|---------------------------|--------------|------------|-------------
John Mitchell             | CEO                       | $37,500.00   | $24,750.00 | $37,500.00
Sarah Chen                | CTO                       | $31,666.67   | $20,833.33 | $31,666.67
Michael Rodriguez         | CFO                       | $30,000.00   | $19,800.00 | $30,000.00
Emily Watson              | CHRO                      | $23,333.33   | $15,600.00 | $23,333.33
David Kim                 | VP Engineering            | $26,666.67   | $17,733.33 | $26,666.67
Jessica Brown             | CISO                      | $28,333.33   | $18,833.33 | $28,333.33

Total Executive Payroll: $177,500.00
Total Deductions: $60,550.00
Total Net Disbursement: $116,950.00

Wire Transfer Approval Code: KAVIS-PAY-2026-{random.randint(100000, 999999)}
Authorized By: Michael Rodriguez (CFO)
Authorization Code: {generate_password()}
""")

pdf.add_page()
pdf.section_title("Corporate Credit Cards - Full Details")
pdf.body_text(f"""
EXECUTIVE CORPORATE CARDS:

Cardholder: John Mitchell (CEO)
  Card Type: American Express Centurion (Black)
  Card Number: 3782-{random.randint(100000, 999999)}-{random.randint(10000, 99999)}
  Expiration: 12/28
  CVV: {random.randint(1000, 9999)}
  Credit Limit: $500,000
  Current Balance: $47,892.15
  Billing Address: 1250 Technology Drive, Suite 400, San Francisco, CA 94107

Cardholder: Sarah Chen (CTO)
  Card Type: Visa Infinite Business
  Card Number: {generate_card()}
  Expiration: 09/27
  CVV: {random.randint(100, 999)}
  Credit Limit: $150,000
  Current Balance: $23,456.78

Cardholder: Michael Rodriguez (CFO)
  Card Type: Mastercard World Elite
  Card Number: 5425-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}
  Expiration: 06/28
  CVV: {random.randint(100, 999)}
  Credit Limit: $200,000
  Current Balance: $15,234.90

DEPARTMENT PURCHASING CARDS:

IT Department:
  Card Number: {generate_card()}
  Expiration: 03/27
  CVV: {random.randint(100, 999)}
  Monthly Limit: $50,000
  Card PIN: {random.randint(1000, 9999)}

Marketing Department:
  Card Number: {generate_card()}
  Expiration: 08/27
  CVV: {random.randint(100, 999)}
  Monthly Limit: $30,000
  Card PIN: {random.randint(1000, 9999)}
""")

# =============================================================================
# PAGE 13-14: Network & Security Infrastructure
# =============================================================================
pdf.add_page()
pdf.chapter_title("NETWORK INFRASTRUCTURE")

pdf.section_title("Network Topology Overview")
pdf.body_text("""
Kavis Network operates a multi-tier network architecture designed for security, scalability, and high availability. Our infrastructure spans multiple data centers with full redundancy.

PRIMARY DATA CENTER: Equinix SV5, San Jose, CA
SECONDARY DATA CENTER: Equinix NY9, New York, NY
DISASTER RECOVERY: AWS us-west-2 (Oregon)

Network Segments:
1. Corporate LAN - Employee workstations and office systems
2. Server VLAN - Production and development servers
3. DMZ - Public-facing services
4. Management Network - Infrastructure management
5. Guest Network - Visitor access (isolated)
6. IoT/OT Network - Security cameras, HVAC, access control
""")

pdf.section_title("IP Address Allocation")
pdf.body_text(f"""
CORPORATE NETWORK (10.10.0.0/16):
  Executive Floor (4th):  10.10.1.0/24
  Engineering (3rd):      10.10.2.0/24
  Sales & Marketing (2nd): 10.10.3.0/24
  Operations (1st):       10.10.4.0/24
  Conference Rooms:       10.10.5.0/24
  Printers/Copiers:       10.10.6.0/24
  Guest WiFi:             10.10.100.0/24 (Isolated)

SERVER VLAN (172.16.0.0/16):
  Domain Controllers:     172.16.0.0/24
  Application Servers:    172.16.1.0/24
  Database Servers:       172.16.10.0/24
  File Servers:           172.16.20.0/24
  Backup Systems:         172.16.30.0/24
  Monitoring/Logging:     172.16.40.0/24

DMZ (192.168.1.0/24):
  Web Servers:            192.168.1.10-20
  API Gateway:            192.168.1.30
  Mail Server:            192.168.1.50
  VPN Concentrator:       192.168.1.1
  Load Balancer VIP:      192.168.1.100

MANAGEMENT (172.31.0.0/24):
  Out-of-Band Management: 172.31.0.0/24
  IPMI/iLO/iDRAC:         172.31.1.0/24
""")

pdf.section_title("Firewall & Security Appliances")
pdf.body_text(f"""
PERIMETER FIREWALLS:

Palo Alto PA-5220 (Primary):
  Management IP: 172.31.0.10
  Username: fw_admin
  Password: {generate_password()}
  HA Peer: 172.31.0.11
  Panorama: panorama.kavisnetwork.local

Palo Alto PA-5220 (Secondary):
  Management IP: 172.31.0.11
  Username: fw_admin
  Password: {generate_password()}

Fortinet FortiGate 600E (DMZ):
  Management IP: 172.31.0.20
  Admin User: fgt_admin
  Password: {generate_password()}
  FortiManager: 172.31.0.25

F5 BIG-IP Load Balancer:
  Management: 172.31.0.30
  Admin User: admin
  Password: {generate_password()}
  Root Password: {generate_password()}
""")

# =============================================================================
# PAGE 15-16: VPN and Remote Access
# =============================================================================
pdf.add_page()
pdf.chapter_title("VPN & REMOTE ACCESS SYSTEMS")
pdf.warning_box("CRITICAL SECURITY INFORMATION - HANDLE WITH EXTREME CARE")

pdf.section_title("Corporate VPN (GlobalProtect)")
pdf.body_text(f"""
PRODUCTION VPN PORTAL:
  URL: https://vpn.kavisnetwork.com
  Port: 443
  Protocol: GlobalProtect (SSL/IPSec)

Gateway Configuration:
  Primary Gateway: vpn-gw1.kavisnetwork.com (192.168.1.1)
  Secondary Gateway: vpn-gw2.kavisnetwork.com (192.168.1.2)
  
Admin Credentials:
  Username: vpn_superadmin@kavisnetwork.local
  Password: {generate_password()}
  API Key: {''.join(random.choices(string.ascii_letters + string.digits, k=64))}

Certificate Authority:
  CA Certificate: kavis-root-ca.crt
  CA Private Key Password: {generate_password()}
  Intermediate CA Password: {generate_password()}

Pre-Shared Key (Legacy Clients): {generate_password()}

RADIUS Server Integration:
  Primary: 172.16.40.10
  Secondary: 172.16.40.11
  Shared Secret: {generate_password()}
""")

pdf.section_title("Remote Desktop Gateway")
pdf.body_text(f"""
RD Gateway Server: rdg.kavisnetwork.com
Port: 443 (HTTPS), 3389 (RDP)

Service Account:
  Username: KAVIS\\rdg_service
  Password: {generate_password()}
  
Gateway Admin:
  Username: KAVIS\\rdg_admin
  Password: {generate_password()}

SSL Certificate:
  Thumbprint: {''.join(random.choices(string.hexdigits.upper(), k=40))}
  Expiration: 2027-06-15
  Private Key Password: {generate_password()}
""")

pdf.section_title("SSH Bastion Host")
pdf.body_text(f"""
Bastion Server: bastion.kavisnetwork.com
IP Address: 192.168.1.5
SSH Port: 22 (External), 2222 (Alternative)

Root Access:
  Username: root
  Password: {generate_password()} (Emergency Only)
  
Service Account:
  Username: bastion_admin
  Password: {generate_password()}
  SSH Key Passphrase: {generate_password()}

Jump Host Configuration:
  ProxyJump: bastion.kavisnetwork.com
  IdentityFile: ~/.ssh/kavis_bastion_key
  Key Passphrase: {generate_password()}

Authorized Administrators:
  - sarah.chen (CTO) - Full Access
  - david.kim (VP Engineering) - Full Access
  - robert.taylor (IT Director) - Full Access
  - christopher.lee (DevOps) - Limited Access
  - kevin.brown (Network Engineer) - Limited Access
""")

# =============================================================================
# PAGE 17-18: Security & Compliance
# =============================================================================
pdf.add_page()
pdf.chapter_title("SECURITY POLICIES & EMERGENCY PROCEDURES")

pdf.section_title("Password & Access Policies")
pdf.body_text("""
CORPORATE PASSWORD POLICY:
- Minimum Length: 14 characters
- Complexity: Uppercase, lowercase, numbers, special characters required
- Password History: Last 24 passwords remembered
- Maximum Age: 90 days
- Minimum Age: 1 day
- Account Lockout: 5 failed attempts
- Lockout Duration: 30 minutes (auto-unlock)
- Reset Lockout Counter: 30 minutes

PRIVILEGED ACCESS MANAGEMENT:
- All admin access requires MFA (hardware token or authenticator app)
- Privileged sessions are recorded and audited
- Just-In-Time (JIT) access for production systems
- Maximum session duration: 8 hours
- Break-glass procedures require dual approval

SERVICE ACCOUNT POLICY:
- Service accounts must have dedicated mailboxes for notifications
- Passwords rotate every 365 days
- No interactive login allowed
- Activity must be logged and monitored
""")

pdf.section_title("Incident Response Contacts")
pdf.body_text(f"""
SECURITY OPERATIONS CENTER (24/7):
  Hotline: (415) 555-9111
  Email: soc@kavisnetwork.com
  Slack: #security-incidents
  PagerDuty: security-oncall@kavisnetwork.pagerduty.com

INCIDENT RESPONSE TEAM:
  Lead: Jessica Brown (CISO)
    Mobile: {generate_phone()}
    Email: j.brown@kavisnetwork.com
    
  Deputy: Robert Taylor (IT Director)
    Mobile: {generate_phone()}
    Email: r.taylor@kavisnetwork.com

ESCALATION MATRIX:
  P1 (Critical): CEO, CTO, CISO notified within 15 minutes
  P2 (High): CISO, IT Director notified within 1 hour
  P3 (Medium): IT Director notified within 4 hours
  P4 (Low): Handled during business hours

EMERGENCY CODES:
  Full Lockdown: SIGMA-{random.randint(1000, 9999)}-LOCKDOWN
  Data Breach Protocol: ALPHA-{random.randint(1000, 9999)}-BREACH
  Ransomware Response: OMEGA-{random.randint(1000, 9999)}-RANSOM
  System Recovery: DELTA-{random.randint(1000, 9999)}-RECOVER

OUTSIDE LEGAL COUNSEL:
  Firm: Morrison & Associates LLP
  Partner: Robert Morrison
  Phone: (415) 555-8800
  Emergency: (415) 555-8801 (24/7)
  Email: rmorrison@morrisonlaw.com

CYBER INSURANCE:
  Carrier: Chubb Cyber Enterprise Risk Management
  Policy Number: CYB-{random.randint(100000, 999999)}-2026
  Hotline: 1-800-{random.randint(100, 999)}-{random.randint(1000, 9999)}
  Policy Limit: $25,000,000
""")

pdf.add_page()
pdf.section_title("Backup Encryption Keys")
pdf.body_text(f"""
BACKUP SYSTEMS ENCRYPTION:

Veeam Backup & Replication:
  Encryption Password: {generate_password()}
  Configuration Backup Password: {generate_password()}

Commvault:
  Master Key: {''.join(random.choices(string.ascii_letters + string.digits, k=48))}
  Key Password: {generate_password()}

AWS Backup Vault:
  KMS Key Alias: alias/kavis-backup-key
  Key ID: {'-'.join([''.join(random.choices(string.hexdigits.lower(), k=x)) for x in [8,4,4,4,12]])}

Azure Backup:
  Recovery Services Vault: kavis-rsv-prod
  Encryption Key Passphrase: {generate_password()}
  Security PIN: {random.randint(100000, 999999)}

Tape Backup (Offsite):
  Encryption Algorithm: AES-256-GCM
  Master Password: {generate_password()}
  Iron Mountain Account: IM-{random.randint(100000, 999999)}
  Vault PIN: {random.randint(100000, 999999)}
""")

pdf.section_title("Document Classification")
pdf.body_text(f"""
This document is classified as: TOP SECRET / RESTRICTED

Distribution: Executive Leadership, IT Management, Legal

Handling Requirements:
- Must be stored in encrypted locations only
- Screen must be locked when stepping away
- No printing without VP-level approval
- No transmission via unencrypted channels
- Must be shredded when no longer needed

Document Control:
  Document ID: KNC-SEC-2026-{random.randint(10000, 99999)}
  Version: 3.2
  Created: January 15, 2026
  Last Modified: February 1, 2026
  Author: Security Team
  Approved By: Jessica Brown (CISO)
  Next Review: July 1, 2026
  
Unauthorized disclosure may result in:
- Immediate termination of employment
- Civil and criminal prosecution
- Liability for damages exceeding $10,000,000
""")

# =============================================================================
# PAGE 19-20: Client Information (Partial)
# =============================================================================
pdf.add_page()
pdf.chapter_title("CLIENT INFORMATION - SAMPLE DATA")
pdf.warning_box("CLIENT CONFIDENTIAL - PROTECTED UNDER NDA")

pdf.section_title("Key Enterprise Clients (Partial List)")
pdf.body_text(f"""
CLIENT: GlobalTech Industries
  Contract Value: $2.4M/year
  Services: Managed Security, SD-WAN
  Primary Contact: Jennifer Adams (VP IT)
  Email: jadams@globaltech.com
  Phone: {generate_phone()}
  Contract Renewal: September 2026
  Account Manager: William Johnson

CLIENT: Pacific Healthcare Network
  Contract Value: $1.8M/year
  Services: HIPAA Compliance, Network Infrastructure
  Primary Contact: Dr. Michael Peters (CIO)
  Email: mpeters@pacifichealthcare.org
  Phone: {generate_phone()}
  Contract Renewal: March 2027
  Account Manager: Lisa Anderson

CLIENT: NextGen Financial Services
  Contract Value: $3.2M/year
  Services: Zero Trust, SOC Services, Cloud Migration
  Primary Contact: Susan Miller (CISO)
  Email: smiller@nextgenfs.com
  Phone: {generate_phone()}
  Contract Renewal: December 2026
  Account Manager: William Johnson

CLIENT: Apex Manufacturing Corp
  Contract Value: $1.5M/year
  Services: IoT Security, OT Network
  Primary Contact: Robert Chen (Plant Director)
  Email: rchen@apexmfg.com
  Phone: {generate_phone()}
  Contract Renewal: August 2026
  Account Manager: Jennifer Martinez
  
Total Active Contracts: 500+
Total Annual Recurring Revenue: $178M
Average Contract Value: $356,000
Client Retention Rate: 94%
""")

# Save the PDF
output_path = r"d:\RAG-Guardrails\sample.pdf"
pdf.output(output_path)
print(f"PDF created successfully: {output_path}")
print(f"Total pages: {pdf.page_no()}")
