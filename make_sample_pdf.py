from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

def create_lending_policy_pdf(filename="loan_policy_document.pdf"):
    print(f"📄 Generating mock 10-page PDF: {filename}...")
    
    # Setup document
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Heading1'], fontSize=24, leading=28, alignment=TA_CENTER, spaceAfter=20
    )
    h1_style = ParagraphStyle(
        'SectionH1', parent=styles['Heading2'], fontSize=16, leading=20, spaceBefore=15, spaceAfter=10
    )
    body_style = ParagraphStyle(
        'PolicyBody', parent=styles['Normal'], fontSize=10, leading=14, alignment=TA_JUSTIFY, spaceAfter=8
    )

    story = []

    # --- PAGE 1: COVER PAGE ---
    story.append(Spacer(1, 150))
    story.append(Paragraph("JPMORGAN CHASE & CO.", title_style))
    story.append(Paragraph("CONSUMER LENDING & CREDIT RISK POLICY BRIEF", ParagraphStyle('Sub', fontSize=14, alignment=TA_CENTER)))
    story.append(Spacer(1, 40))
    story.append(Paragraph("Version: 2026.4<br/>Effective Date: July 2026<br/>Classification: Internal Use Only", ParagraphStyle('Meta', alignment=TA_CENTER)))
    story.append(PageBreak())

    # --- PAGES 2-10: CORE POLICY SECTIONS ---
    sections = [
        (
            "SECTION 1: DEBT-TO-INCOME (DTI) REQUIREMENTS",
            "The maximum allowable Debt-to-Income (DTI) ratio for a standard consumer residential mortgage is strictly capped at 43%. Any applicant exceeding a 43% DTI must be automatically routed to senior underwriting for an exception review. No exceptions are permitted for applicant files demonstrating a DTI greater than 50% under any circumstance. Front-end DTI ratios, calculating housing expenses exclusively, should ideally target a maximum threshold of 28% to maintain optimal credit rating tracking."
        ),
        (
            "SECTION 2: CROSS-SELLING TRIGGERS",
            "During the financial assessment, if an applicant's bank statements reveal recurring external payments greater than $500 per month to competing merchant processing platforms, the loan officer must flag the account for a JPMC Merchant Services transition pitch. Additional cross-selling initiatives dictate that high-net-worth clients maintaining cash balances exceeding $250,000 across checking vehicles must be formally introduced to a dedicated Chase Wealth Management advisor within three business days of loan origination."
        ),
        (
            "SECTION 3: CREDIT SCORE THRESHOLDS AND PRICING TIERS",
            "The minimum acceptable FICO score for prime residential mortgage packaging is evaluated at 620. Applicants maintaining credit tiers between 620 and 679 are classified as Tier-3 Risk, necessitating a mandatory 0.50% interest rate premium adjustment. Tiers between 680 and 739 represent Tier-2 Risk portfolios. Super-prime applicants demonstrating documented credit metrics of 740 or higher qualify for baseline preferred pricing matrices, removing structural pricing overlays."
        ),
        (
            "SECTION 4: LOAN-TO-VALUE (LTV) CONSTRAINTS",
            "Standard conventional financing structures permit maximum baseline Loan-to-Value (LTV) limits up to 80% without requiring Private Mortgage Insurance (PMI). Borrowers requesting high-LTV financing up to 95% must clear secondary employment verification check-calls and register continuous secondary escrow reserves covering a trailing twelve-month operational horizon. Cash-out refinancing frameworks enforce a structural ceiling capping maximum exposure strictly at 75% LTV."
        ),
        (
            "SECTION 5: VERIFICATION OF INCOME AND EMPLOYMENT",
            "All residential originations require validation utilizing two consecutive years of corporate W-2 statements alongside the consecutive accumulation of 30 days of recent physical pay stubs. For self-employed applicants, underwriting guidelines require a comprehensive delivery of two years of signed federal individual and business tax returns, supplemented by a Year-to-Date (YTD) profit and loss statement certified by a licensed Certified Public Accountant (CPA)."
        ),
        (
            "SECTION 6: ASSET VERIFICATION AND RESERVE REQUIREMENTS",
            "Borrowers must demonstrate clear liquid reserves sufficient to clear closing costs alongside distinct asset baselines safeguarding subsequent payment requirements. Standard primary residences require a minimum reserve holding equivalent to 3 months of principal, interest, taxes, and insurance (PITI). Secondary investment properties trigger elevated verification mandates, requiring a full 6-month PITI liquid reserve statement."
        ),
        (
            "SECTION 7: COLLATERAL APPRAISAL GUIDELINES",
            "Independent full physical appraisals are mandatory for all standard loan structures. Automated Valuation Models (AVMs) are only permissible for streamlined loan modifications below an aggregate balance threshold of $250,000. Properties indicating structural deficiencies, active environmental hazards, or severe zoning non-compliance metrics must be rejected from active collateral pools until independent remediation certifications are produced."
        ),
        (
            "SECTION 8: UNDERWRITING EXCEPTIONS AND ESCALATIONS",
            "Compensating factors required to support an underwriting exception include verified cash reserves doubling standard requirements, significant documented down payment enhancements exceeding 30%, or verified secondary co-signers meeting super-prime criteria. All exception forms must clearly log sign-offs from both a Regional Credit Director and an active Senior Underwriting Officer."
        ),
        (
            "SECTION 9: COMPLIANCE AND FAIR LENDING AUDITS",
            "Every loan application file remains subject to automated Quality Control (QC) auditing logic prior to formal document release. Underwriters must guarantee adherence to the Equal Credit Opportunity Act (ECOA) frameworks. Any processing delay exceeding standard 45-day cycle windows requires formal delivery of an Adverse Action or Notice of Incomplete Application disclosure to the primary applicant."
        )
    ]

    for title, content in sections:
        story.append(Paragraph(title, h1_style))
        # Add repeated text blocks to fill out the page space realistically
        full_page_text = (content + " ") * 4 
        story.append(Paragraph(full_page_text, body_style))
        story.append(PageBreak())

    # Build the document
    doc.build(story)
    print("✅ Sample PDF successfully created!")

if __name__ == "__main__":
    create_lending_policy_pdf()