#!/usr/bin/env python3
"""
TradeFlow Competitive Audit - Body PDF (ReportLab)
Pre-Phase 2 Strategic Review
"""

import os, sys, hashlib
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, CondPageBreak
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus import SimpleDocTemplate

# ━━ Cascade Palette (auto-generated) ━━
PAGE_BG       = colors.HexColor('#f6f6f5')
SECTION_BG    = colors.HexColor('#ecebe9')
CARD_BG       = colors.HexColor('#f0efeb')
TABLE_STRIPE  = colors.HexColor('#f3f2f1')
HEADER_FILL   = colors.HexColor('#584f34')
COVER_BLOCK   = colors.HexColor('#7d755d')
BORDER        = colors.HexColor('#d3cfc3')
ICON          = colors.HexColor('#7f6f40')
ACCENT        = colors.HexColor('#93761f')
ACCENT_2      = colors.HexColor('#7253d0')
TEXT_PRIMARY   = colors.HexColor('#181816')
TEXT_MUTED     = colors.HexColor('#87847d')
SEM_SUCCESS   = colors.HexColor('#508863')
SEM_WARNING   = colors.HexColor('#a68b53')
SEM_ERROR     = colors.HexColor('#97453d')
SEM_INFO      = colors.HexColor('#496887')

# ━━ Font Registration ━━
import platform
_IS_MAC = platform.system() == 'Darwin'
FONT_DIR = os.path.expanduser('~/.openclaw/workspace/fonts') if _IS_MAC else '/usr/share/fonts'

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

pdfmetrics.registerFont(TTFont('FreeSerif', f'{FONT_DIR}/truetype/freefont/FreeSerif.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-Bold', f'{FONT_DIR}/truetype/freefont/FreeSerifBold.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-Italic', f'{FONT_DIR}/truetype/freefont/FreeSerifItalic.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-BoldItalic', f'{FONT_DIR}/truetype/freefont/FreeSerifBoldItalic.ttf'))
registerFontFamily('FreeSerif', normal='FreeSerif', bold='FreeSerif-Bold', italic='FreeSerif-Italic', boldItalic='FreeSerif-BoldItalic')

# ━━ Styles ━━
PAGE_W, PAGE_H = A4
LEFT_M = 0.85 * inch
RIGHT_M = 0.85 * inch
TOP_M = 0.75 * inch
BOT_M = 0.75 * inch
AVAIL_W = PAGE_W - LEFT_M - RIGHT_M

h1_style = ParagraphStyle(
    name='H1', fontName='FreeSerif-Bold', fontSize=20, leading=28,
    textColor=TEXT_PRIMARY, spaceBefore=18, spaceAfter=10, alignment=TA_LEFT
)
h2_style = ParagraphStyle(
    name='H2', fontName='FreeSerif-Bold', fontSize=14, leading=20,
    textColor=HEADER_FILL, spaceBefore=14, spaceAfter=8, alignment=TA_LEFT
)
h3_style = ParagraphStyle(
    name='H3', fontName='FreeSerif-Bold', fontSize=11.5, leading=16,
    textColor=TEXT_PRIMARY, spaceBefore=10, spaceAfter=6, alignment=TA_LEFT
)
body_style = ParagraphStyle(
    name='Body', fontName='FreeSerif', fontSize=10.5, leading=17,
    textColor=TEXT_PRIMARY, spaceBefore=0, spaceAfter=6, alignment=TA_JUSTIFY
)
body_left = ParagraphStyle(
    name='BodyLeft', fontName='FreeSerif', fontSize=10.5, leading=17,
    textColor=TEXT_PRIMARY, spaceBefore=0, spaceAfter=6, alignment=TA_LEFT
)
muted_style = ParagraphStyle(
    name='Muted', fontName='FreeSerif-Italic', fontSize=9.5, leading=14,
    textColor=TEXT_MUTED, spaceBefore=2, spaceAfter=4, alignment=TA_LEFT
)
bullet_style = ParagraphStyle(
    name='Bullet', fontName='FreeSerif', fontSize=10.5, leading=17,
    textColor=TEXT_PRIMARY, spaceBefore=2, spaceAfter=4,
    leftIndent=18, bulletIndent=6, alignment=TA_LEFT
)
callout_style = ParagraphStyle(
    name='Callout', fontName='FreeSerif-Bold', fontSize=11, leading=17,
    textColor=ACCENT, spaceBefore=6, spaceAfter=6, leftIndent=12,
    borderPadding=(6, 6, 6, 6), alignment=TA_LEFT
)

# Table styles
th_style = ParagraphStyle(
    name='TH', fontName='FreeSerif-Bold', fontSize=9.5, leading=13,
    textColor=colors.white, alignment=TA_CENTER
)
td_style = ParagraphStyle(
    name='TD', fontName='FreeSerif', fontSize=9, leading=13,
    textColor=TEXT_PRIMARY, alignment=TA_CENTER
)
td_left = ParagraphStyle(
    name='TDLeft', fontName='FreeSerif', fontSize=9, leading=13,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT
)
td_bold = ParagraphStyle(
    name='TDBold', fontName='FreeSerif-Bold', fontSize=9, leading=13,
    textColor=TEXT_PRIMARY, alignment=TA_LEFT
)

TABLE_HEADER_COLOR = HEADER_FILL
TABLE_ROW_ODD = TABLE_STRIPE
TABLE_ROW_EVEN = colors.white

# TOC styles
toc_l0 = ParagraphStyle(name='TOCL0', fontName='FreeSerif-Bold', fontSize=12, leftIndent=20, leading=22, textColor=TEXT_PRIMARY)
toc_l1 = ParagraphStyle(name='TOCL1', fontName='FreeSerif', fontSize=10.5, leftIndent=40, leading=18, textColor=TEXT_MUTED)

# ━━ TocDocTemplate ━━
class TocDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if hasattr(flowable, 'bookmark_name'):
            level = getattr(flowable, 'bookmark_level', 0)
            text = getattr(flowable, 'bookmark_text', '')
            key = getattr(flowable, 'bookmark_key', '')
            self.notify('TOCEntry', (level, text, self.page, key))

# ━━ Helpers ━━
def heading(text, style, level=0):
    key = 'h_%s' % hashlib.md5(text.encode()).hexdigest()[:8]
    p = Paragraph('<a name="%s"/>%s' % (key, text), style)
    p.bookmark_name = text
    p.bookmark_level = level
    p.bookmark_text = text
    p.bookmark_key = key
    return p

def safe_keep(elements):
    total = 0
    for el in elements:
        w, h = el.wrap(AVAIL_W, PAGE_H)
        total += h
    max_h = PAGE_H * 0.4
    if total <= max_h:
        return [KeepTogether(elements)]
    elif len(elements) >= 2:
        return [KeepTogether(elements[:2])] + list(elements[2:])
    return list(elements)

def make_table(headers, rows, col_ratios=None):
    if col_ratios is None:
        col_ratios = [1.0 / len(headers)] * len(headers)
    col_widths = [r * AVAIL_W for r in col_ratios]
    # Scale up if too narrow
    tw = sum(col_widths)
    if tw < AVAIL_W * 0.85:
        scale = (AVAIL_W * 0.92) / tw
        col_widths = [w * scale for w in col_widths]
    data = [[Paragraph('<b>%s</b>' % h, th_style) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), td_style) if not isinstance(c, Paragraph) else c for c in row])
    t = Table(data, colWidths=col_widths, hAlign='CENTER')
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.4, BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        bg = TABLE_ROW_ODD if i % 2 == 0 else TABLE_ROW_EVEN
        style_cmds.append(('BACKGROUND', (0, i), (-1, i), bg))
    t.setStyle(TableStyle(style_cmds))
    return t

# ━━ Page number footer ━━
from reportlab.platypus import PageTemplate, Frame

def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont('FreeSerif', 9)
    canvas.setFillColor(TEXT_MUTED)
    page_num = canvas.getPageNumber()
    if page_num > 1:
        canvas.drawCentredString(PAGE_W / 2, 0.4 * inch, str(page_num - 1))
    canvas.restoreState()

# ━━ Build Document ━━
OUTPUT = '/home/z/my-project/download/tradeflow-audit-body.pdf'

frame = Frame(LEFT_M, BOT_M, AVAIL_W, PAGE_H - TOP_M - BOT_M, id='normal')
template = PageTemplate(id='normal', frames=frame, onPage=add_page_number)

doc = TocDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=LEFT_M, rightMargin=RIGHT_M,
    topMargin=TOP_M, bottomMargin=BOT_M,
    title='TradeFlow Competitive Audit',
    author='TradeFlow',
    subject='Pre-Phase 2 Competitive Analysis'
)
doc.pageTemplates = [template]

story = []

# ── TOC ──
toc = TableOfContents()
toc.levelStyles = [toc_l0, toc_l1]
story.append(Paragraph('<b>Table of Contents</b>', ParagraphStyle(
    name='TOCTitle', fontName='FreeSerif-Bold', fontSize=22, leading=30,
    textColor=TEXT_PRIMARY, spaceBefore=6, spaceAfter=18, alignment=TA_LEFT
)))
story.append(toc)
story.append(PageBreak())

# ══════════════════════════════════════════════════════════
# CHAPTER 1: Executive Summary
# ══════════════════════════════════════════════════════════
story.extend([
    heading('<b>1. Executive Summary</b>', h1_style, 0),
    Spacer(1, 8),
    Paragraph(
        'This audit benchmarks TradeFlow Phase 1 against 11 competitors spanning consumer remittance, '
        'B2B FX, comparison engines, and payment infrastructure. The analysis was conducted to inform '
        'strategic decisions before commencing Phase 2 (Invoicing and Receivables) and to ensure that '
        'the platform builds on its unique positioning rather than drifting toward feature parity with '
        'established players. The findings reveal that TradeFlow occupies a genuinely uncontested niche: '
        'no competitor currently offers multi-rail payment comparison that includes PAPSS as a settlement layer.',
        body_style
    ),
    Paragraph(
        'The research covered Wise, SendWave, Chipper Cash, AZA Finance, Fonbnk, Remitly, Monito, '
        'Flutterwave, Paystack, Africa\'s Talking, and Pfegha. Across all 11 competitors, zero mention '
        'PAPSS or AfCFTA on their consumer-facing platforms. The $5 billion-plus in annual savings that '
        'PAPSS could unlock for African cross-border payments remains completely untapped by any '
        'existing tool. Furthermore, no competitor compares payment infrastructure rails (PAPSS versus '
        'SWIFT versus mobile money versus stablecoin); they only compare remittance providers (Wise versus '
        'Remitly versus Western Union). This distinction is critical and represents TradeFlow\'s core '
        'differentiator going forward.',
        body_style
    ),
    Paragraph(
        'Phase 1 has established the foundational FX comparison engine with 20 African currencies, '
        'five payment methods (PAPSS, SWIFT, Mobile Money, Western Union, MoneyGram), and a clean, '
        'responsive web interface. However, several gaps exist when measured against best-in-class '
        'benchmarks, particularly around live rate data, historical charting, user accounts, and rate alert '
        'functionality. This audit provides a detailed gap analysis, competitive feature matrix, and '
        'prioritized recommendations to guide Phase 2 and beyond.',
        body_style
    ),
])

# Key stats callout
stats_data = [
    [Paragraph('<b>Metric</b>', th_style), Paragraph('<b>Finding</b>', th_style), Paragraph('<b>Implication</b>', th_style)],
    [Paragraph('PAPSS mentions', td_left), Paragraph('0 of 11 competitors', td_style), Paragraph('Uncontested positioning', td_left)],
    [Paragraph('Multi-rail comparison', td_left), Paragraph('0 of 11 competitors', td_style), Paragraph('Unique product category', td_left)],
    [Paragraph('Intra-Africa FX focus', td_left), Paragraph('Only 2 (AZA, Chipper)', td_style), Paragraph('Underserved corridor', td_left)],
    [Paragraph('Avg. SSA remittance cost', td_left), Paragraph('8.45% for $200', td_style), Paragraph('Massive demand for transparency', td_left)],
]
story.append(Spacer(1, 12))
stats_table = Table(stats_data, colWidths=[AVAIL_W*0.25, AVAIL_W*0.30, AVAIL_W*0.45], hAlign='CENTER')
stats_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_COLOR),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('GRID', (0, 0), (-1, -1), 0.4, BORDER),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('BACKGROUND', (0, 1), (-1, 1), TABLE_ROW_EVEN),
    ('BACKGROUND', (0, 2), (-1, 2), TABLE_ROW_ODD),
    ('BACKGROUND', (0, 3), (-1, 3), TABLE_ROW_EVEN),
    ('BACKGROUND', (0, 4), (-1, 4), TABLE_ROW_ODD),
]))
story.append(stats_table)
story.append(Spacer(1, 6))
story.append(Paragraph('<i>Table 1: Key competitive landscape findings</i>', muted_style))
story.append(Spacer(1, 18))

# ══════════════════════════════════════════════════════════
# CHAPTER 2: TradeFlow Phase 1 Current State
# ══════════════════════════════════════════════════════════
story.extend([
    heading('<b>2. TradeFlow Phase 1: Current State</b>', h1_style, 0),
    Spacer(1, 8),
    heading('<b>2.1 What Was Built</b>', h2_style, 1),
    Paragraph(
        'TradeFlow Phase 1 delivered a single-page web application with an FX comparison calculator '
        'as its core feature. The application is built on Next.js 16 with Prisma ORM, SQLite database, '
        'Tailwind CSS 4, and shadcn/ui components. The landing page serves triple duty as marketing '
        'collateral, educational content about PAPSS, and the functional calculator. The architecture is '
        'designed to be extensible: the Prisma schema includes User, Business, FxRateSnapshot, and '
        'ComparisonLog models, with NextAuth integration prepared but not yet activated. The codebase '
        'follows zero-trust principles with input validation via Zod on all API endpoints.',
        body_style
    ),
    heading('<b>2.2 Feature Inventory</b>', h2_style, 1),
])

features_data = [
    [Paragraph('<b>Feature</b>', th_style), Paragraph('<b>Status</b>', th_style), Paragraph('<b>Notes</b>', th_style)],
    [Paragraph('FX comparison calculator', td_left), Paragraph('Live', td_style), Paragraph('5 methods, 20+ currencies', td_left)],
    [Paragraph('PAPSS routing display', td_left), Paragraph('Live', td_style), Paragraph('Always shown first when eligible', td_left)],
    [Paragraph('Savings banner', td_left), Paragraph('Live', td_style), Paragraph('Shows amount and percent saved', td_left)],
    [Paragraph('Quick-amount presets', td_left), Paragraph('Live', td_style), Paragraph('Currency-adaptive buttons', td_left)],
    [Paragraph('Currency swap', td_left), Paragraph('Live', td_style), Paragraph('One-click direction reversal', td_left)],
    [Paragraph('Dark mode', td_left), Paragraph('Live', td_style), Paragraph('System-aware via next-themes', td_left)],
    [Paragraph('Responsive design', td_left), Paragraph('Live', td_style), Paragraph('Mobile-first, works on all screens', td_left)],
    [Paragraph('Anonymous comparison logging', td_left), Paragraph('Live', td_style), Paragraph('IP + UA, no PII', td_left)],
    [Paragraph('Auth system (NextAuth)', td_left), Paragraph('Schema only', td_style), Paragraph('DB models exist, UI not wired', td_left)],
    [Paragraph('Business profiles', td_left), Paragraph('Schema only', td_style), Paragraph('Prisma model ready', td_left)],
    [Paragraph('Live FX rates', td_left), Paragraph('Not implemented', td_style), Paragraph('Using hardcoded 2025 rates', td_left)],
    [Paragraph('Rate history charts', td_left), Paragraph('Not implemented', td_style), Paragraph('No charting yet', td_left)],
    [Paragraph('Rate alerts', td_left), Paragraph('Not implemented', td_style), Paragraph('No notification system', td_left)],
]
story.append(Spacer(1, 6))
feat_table = Table(features_data, colWidths=[AVAIL_W*0.35, AVAIL_W*0.20, AVAIL_W*0.45], hAlign='CENTER')
feat_cmds = [
    ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_COLOR),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('GRID', (0, 0), (-1, -1), 0.4, BORDER),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]
for i in range(1, len(features_data)):
    bg = TABLE_ROW_ODD if i % 2 == 0 else TABLE_ROW_EVEN
    feat_cmds.append(('BACKGROUND', (0, i), (-1, i), bg))
feat_table.setStyle(TableStyle(feat_cmds))
story.append(feat_table)
story.append(Spacer(1, 6))
story.append(Paragraph('<i>Table 2: TradeFlow Phase 1 feature inventory</i>', muted_style))
story.append(Spacer(1, 12))

story.extend([
    heading('<b>2.3 Technical Stack Assessment</b>', h2_style, 1),
    Paragraph(
        'The technology choices for Phase 1 are sound and align with SaaS best practices. Next.js 16 provides '
        'server-side rendering, API routes, and middleware support essential for compliance features in later '
        'phases. Prisma ORM with SQLite is appropriate for early-stage development and can be migrated to '
        'PostgreSQL or Turso for production without schema changes. The shadcn/ui component library '
        'ensures accessibility and consistency. Tailwind CSS 4 enables rapid styling iteration. Zod validation '
        'on all API endpoints enforces zero-trust data handling. The package includes React Query, Zustand, '
        'and Recharts, indicating readiness for complex state management and data visualization in Phase 2.',
        body_style
    ),
    Paragraph(
        'However, the current deployment uses SQLite with a local database file, which is not suitable for '
        'multi-instance production environments. Additionally, the FX rates are hardcoded approximations from '
        '2025 rather than live market data, which significantly limits the tool\'s practical utility for real '
        'decision-making. These are the two most critical gaps to address before the product can serve real users.',
        body_style
    ),
])

# ══════════════════════════════════════════════════════════
# CHAPTER 3: Competitive Landscape
# ══════════════════════════════════════════════════════════
story.extend([
    heading('<b>3. Competitive Landscape Analysis</b>', h1_style, 0),
    Spacer(1, 8),
    heading('<b>3.1 Competitor Classification</b>', h2_style, 1),
    Paragraph(
        'The 11 competitors analyzed fall into four distinct categories, each with different capabilities, '
        'target audiences, and relevance to TradeFlow. Understanding these categories is essential for '
        'positioning because TradeFlow does not compete directly with any single player; rather, it occupies '
        'a meta-layer above them by comparing their payment rails side by side. The four categories are: '
        'consumer remittance providers (Wise, SendWave, Remitly, Chipper Cash), B2B FX specialists (AZA '
        'Finance), comparison engines (Monito), payment infrastructure platforms (Flutterwave, Paystack, '
        'Africa\'s Talking), and niche players (Fonbnk, Pfegha).',
        body_style
    ),
    heading('<b>3.2 Consumer Remittance Providers</b>', h2_style, 1),
    heading('<b>3.2.1 Wise (formerly TransferWise)</b>', h3_style, 1),
    Paragraph(
        'Wise is the global benchmark for FX transparency and serves as the primary quality standard for '
        'TradeFlow to measure against. With 12.8 million customers and operations in 80-plus countries, Wise '
        'has demonstrated that transparency is a viable business model, not just an ethical choice. Their approach '
        'of displaying the mid-market rate with a clear fee breakdown has set industry expectations. Lyssna UX '
        'research from March 2026 shows that 70% of Wise users correctly identify the total cost of their '
        'transfer, compared to significantly lower comprehension rates for competitors who embed markups in '
        'their exchange rates. This is powerful evidence that transparency drives both user trust and retention.',
        body_style
    ),
    Paragraph(
        'For African corridors specifically, Wise supports only 6 African currencies and routes all '
        'transfers through USD or EUR hubs, adding double conversion costs for intra-African pairs. They do '
        'not support direct GHS-to-KES or NGN-to-TZS transfers. This is a structural limitation that PAPSS '
        'was designed to solve, and it represents a significant opportunity for TradeFlow to highlight. Wise also '
        'offers Wise Platform API for businesses, batch payments, and a multi-currency account, features that '
        'TradeFlow should benchmark for Phase 3 and Phase 4 capabilities.',
        body_style
    ),
    heading('<b>3.2.2 SendWave</b>', h3_style, 1),
    Paragraph(
        'SendWave operates a mobile-first remittance service focused on diaspora-to-Africa corridors. They '
        'support 8 African countries with cash pickup and mobile money delivery. SendWave deliberately hides '
        'FX markups within their exchange rates, providing a poor transparency benchmark. Their strength lies '
        'in mobile UX: the app is designed for first-time smartphone users with large touch targets, minimal '
        'text, and a streamlined 3-tap transfer flow. TradeFlow should study SendWave\'s mobile UX patterns '
        'for its own mobile optimization, while actively contrasting SendWave\'s hidden costs with TradeFlow\'s '
        'transparent comparison output. SendWave was acquired by Zepz (WorldRemit\'s parent) in 2022, giving it '
        'financial backing but also corporate inertia that a lean startup can exploit.',
        body_style
    ),
    heading('<b>3.2.3 Remitly</b>', h3_style, 1),
    Paragraph(
        'Remitly serves 15-plus African countries from diaspora sender markets. They offer economy and express '
        'delivery tiers, with delivery speed being a primary differentiator. Like SendWave, Remitly shows the '
        'transfer fee but hides the FX markup, resulting in partial transparency. Their mobile app is well-rated '
        'and they offer a "price match guarantee" against competitors, which creates an interesting dynamic: '
        'TradeFlow could potentially partner with Remitly for affiliate referrals while simultaneously using the '
        'price match guarantee as a bargaining tool for users. Remitly went public on NASDAQ in 2021 and has '
        'since expanded into bill payments and digital banking, showing the trajectory from remittance to '
        'full financial services that TradeFlow\'s phased roadmap mirrors.',
        body_style
    ),
    heading('<b>3.2.4 Chipper Cash</b>', h3_style, 1),
    Paragraph(
        'Chipper Cash is the most directly relevant competitor because it uniquely supports direct intra-Africa '
        'FX pairs across 8 currencies without routing through USD. They use Ripple\'s blockchain rails for '
        'settlement, which provides instant finality but introduces crypto regulatory complexity. Chipper Cash '
        'has raised over $300 million in venture capital and claims 5 million users. However, their FX '
        'transparency is rated as poor: they display neither the mid-market rate nor the markup percentage. '
        'This is a critical weakness that TradeFlow can exploit. Chipper Cash also offers stock and crypto '
        'trading features, suggesting they are evolving toward a super-app model rather than a focused FX tool. '
        'TradeFlow should maintain focus on its comparison and transparency niche rather than trying to match '
        'Chipper Cash\'s feature breadth.',
        body_style
    ),
    heading('<b>3.3 B2B FX Specialist</b>', h2_style, 1),
    heading('<b>3.3.1 AZA Finance</b>', h3_style, 1),
    Paragraph(
        'AZA Finance (formerly Binkabi) is the deepest African FX specialist, offering 200-plus currency pairs '
        'with proprietary liquidity sourcing. They serve businesses rather than consumers, with a minimum '
        'transfer size that excludes retail users. Their API-first approach is the benchmark for TradeFlow\'s '
        'Phase 3 payment API. AZA does not publicly display rates or fees, requiring a login and KYC '
        'completion before any pricing is revealed. This lack of transparency is common in B2B FX and creates '
        'an opportunity for TradeFlow to serve as the transparent discovery layer that directs businesses to '
        'providers like AZA for execution. AZA\'s direct settlement capability for intra-African pairs, without '
        'USD intermediary routing, is exactly what PAPSS enables at scale, making them both a benchmark and a '
        'potential integration partner for TradeFlow\'s later phases.',
        body_style
    ),
    heading('<b>3.4 Comparison Engines</b>', h2_style, 1),
    heading('<b>3.4.1 Monito</b>', h3_style, 1),
    Paragraph(
        'Monito is the closest existing product to what TradeFlow aspires to become. They compare 30-plus '
        'remittance providers across thousands of corridors, ranking results by total recipient amount. Monito '
        'earns revenue through affiliate commissions when users click through to complete a transfer with a '
        'listed provider. They also offer a "Monito Score" that factors in regulatory licenses, customer reviews, '
        'and service quality, going beyond pure price comparison. However, Monito has three critical gaps that '
        'TradeFlow can fill. First, they compare remittance companies (Wise, Remitly, Western Union), not payment '
        'rails (PAPSS, SWIFT, mobile money). Second, their intra-Africa coverage is weak, focusing primarily on '
        'diaspora-to-home corridors. Third, they have zero PAPSS awareness, meaning they cannot surface the '
        'cheapest option for African businesses trading within the continent. The affiliate monetization model is '
        'directly applicable to TradeFlow\'s Phase 3 and Phase 4 strategy.',
        body_style
    ),
    heading('<b>3.5 Payment Infrastructure Platforms</b>', h2_style, 1),
    heading('<b>3.5.1 Flutterwave</b>', h3_style, 1),
    Paragraph(
        'Flutterwave is Africa\'s largest payment infrastructure company, processing payments across 34 African '
        'countries and 150-plus currencies. Acquired by Stripe, they provide payment gateways, merchant '
        'tools, and cross-border transfer capabilities. However, Flutterwave is not a consumer-facing FX '
        'comparison tool. Their cross-border product routes most transfers through USD rather than direct '
        'currency pairs, adding cost. Flutterwave\'s Barter product offers virtual dollar cards for African '
        'businesses, addressing a different pain point than TradeFlow. The key takeaway from Flutterwave is their '
        'API-first architecture and their success in building developer-friendly payment tools, which should '
        'inform TradeFlow\'s Phase 3 API design. Flutterwave also demonstrates that regulatory compliance at '
        'scale across 34 African jurisdictions is achievable, providing a roadmap for TradeFlow\'s expansion.',
        body_style
    ),
    heading('<b>3.5.2 Paystack</b>', h3_style, 1),
    Paragraph(
        'Paystack (also Stripe-acquired) is a payment gateway focused on domestic payment collection in Nigeria, '
        'Ghana, Kenya, South Africa, and Egypt. They are not a cross-border FX product and do not offer currency '
        'conversion or international transfer comparison. Paystack\'s relevance to TradeFlow is primarily as a '
        'potential Phase 3 integration partner: businesses that use TradeFlow for FX comparison could execute '
        'payments through Paystack\'s infrastructure. Their checkout experience and merchant dashboard are '
        'industry-leading and should inform TradeFlow\'s invoice payment flow in Phase 2. The Stripe acquisition '
        'gives both Paystack and Flutterwave global credibility and access to advanced fraud detection systems '
        'that TradeFlow will need to build or partner for in later phases.',
        body_style
    ),
    heading('<b>3.5.3 Africa\'s Talking</b>', h3_style, 1),
    Paragraph(
        'Africa\'s Talking provides communication and payment APIs including SMS, USSD, voice, and mobile money '
        'integration across 10-plus African countries. They are not a cross-border FX product but offer the '
        'deepest mobile money API coverage on the continent. For TradeFlow, Africa\'s Talking is relevant in two '
        'ways. First, their mobile money integration could power the "Mobile Money" payment method comparison '
        'with real fee data rather than estimates. Second, their SMS and USSD APIs could enable rate alert '
        'notifications via text message, which is critical for reaching users in markets where smartphone '
        'penetration is lower. Africa\'s Talking\'s developer documentation and SDK quality are benchmarks for '
        'TradeFlow\'s own API documentation.',
        body_style
    ),
    heading('<b>3.6 Niche and Emerging Players</b>', h2_style, 1),
    Paragraph(
        'Fonbnk converts prepaid mobile airtime to USDC stablecoin and back, targeting unbanked populations. '
        'While innovative, their market presence is minimal and their stablecoin-based approach introduces '
        'regulatory uncertainty. However, Fonbnk represents the stablecoin rail that TradeFlow should consider '
        'adding as a sixth comparison method in future phases, particularly as Nigerian and Kenyan regulators '
        'develop clearer stablecoin frameworks. Pfegha is a Cameroon-only mobile wallet with negligible cross-border '
        'capability and is not a competitive threat. It is included in this audit only for completeness of the '
        'African payment landscape mapping.',
        body_style
    ),
])

# ══════════════════════════════════════════════════════════
# CHAPTER 4: Feature-by-Feature Comparison
# ══════════════════════════════════════════════════════════
story.extend([
    heading('<b>4. Feature-by-Feature Comparison</b>', h1_style, 0),
    Spacer(1, 8),
    heading('<b>4.1 Scoring Methodology</b>', h2_style, 1),
    Paragraph(
        'Each competitor was scored on six dimensions relevant to TradeFlow\'s positioning: African Focus (depth '
        'of African currency and corridor coverage), FX Transparency (how clearly total costs are communicated), '
        'PAPSS Awareness (explicit mention or integration of PAPSS infrastructure), Comparison Capability '
        '(ability to compare multiple providers or methods side by side), Mobile UX (quality of mobile '
        'experience), and API and Developer Tools (availability and quality of programmatic access). Scores '
        'range from 0 to 5, with 5 indicating best-in-class. The overall relevance score weights dimensions '
        'based on their importance to TradeFlow\'s specific niche.',
        body_style
    ),
])

# Scoring matrix
score_headers = ['Competitor', 'Africa', 'FX Trans.', 'PAPSS', 'Compare', 'Mobile', 'API/Dev', 'Overall']
score_rows = [
    ['Monito', '3/5', '5/5', '0/5', '5/5', '3/5', '1/5', 'HIGH'],
    ['Wise', '3/5', '5/5', '0/5', '2/5', '4/5', '4/5', 'HIGH'],
    ['AZA Finance', '5/5', '2/5', '0/5', '1/5', '1/5', '4/5', 'MEDIUM'],
    ['Chipper Cash', '5/5', '1/5', '0/5', '1/5', '4/5', '1/5', 'MEDIUM'],
    ['Flutterwave', '5/5', '2/5', '0/5', '1/5', '3/5', '4/5', 'MEDIUM'],
    ['Remitly', '4/5', '2/5', '0/5', '1/5', '4/5', '1/5', 'LOW-MED'],
    ['SendWave', '4/5', '1/5', '0/5', '1/5', '5/5', '1/5', 'LOW'],
    ['Fonbnk', '3/5', '1/5', '0/5', '1/5', '2/5', '1/5', 'LOW'],
    ['Africa\'s Talking', '4/5', 'N/A', '0/5', 'N/A', '1/5', '5/5', 'LOW'],
    ['Paystack', '3/5', 'N/A', '0/5', 'N/A', '1/5', '4/5', 'LOW'],
    ['Pfegha', '1/5', '1/5', '0/5', '1/5', '1/5', '1/5', 'NEGLIGIBLE'],
]
score_ratios = [0.18, 0.10, 0.10, 0.10, 0.10, 0.10, 0.14, 0.18]
score_table_data = [[Paragraph('<b>%s</b>' % h, th_style) for h in score_headers]]
for row in score_rows:
    score_table_data.append([Paragraph(c, td_left if i == 0 else (td_bold if i == len(row)-1 else td_style)) for i, c in enumerate(row)])
score_t = Table(score_table_data, colWidths=[r*AVAIL_W for r in score_ratios], hAlign='CENTER')
score_cmds = [
    ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_COLOR),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('GRID', (0, 0), (-1, -1), 0.4, BORDER),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 4),
    ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
]
for i in range(1, len(score_table_data)):
    bg = TABLE_ROW_ODD if i % 2 == 0 else TABLE_ROW_EVEN
    score_cmds.append(('BACKGROUND', (0, i), (-1, i), bg))
score_t.setStyle(TableStyle(score_cmds))
story.append(Spacer(1, 12))
story.append(score_t)
story.append(Spacer(1, 6))
story.append(Paragraph('<i>Table 3: Competitor scoring matrix (1-5 scale, overall relevance weighted)</i>', muted_style))
story.append(Spacer(1, 18))

# ══════════════════════════════════════════════════════════
# CHAPTER 5: Gap Analysis
# ══════════════════════════════════════════════════════════
story.extend([
    heading('<b>5. Gap Analysis: TradeFlow vs. Benchmarks</b>', h1_style, 0),
    Spacer(1, 8),
    heading('<b>5.1 Critical Gaps (Must Fix Before Phase 2)</b>', h2_style, 1),
    Paragraph(
        'Three gaps are classified as critical because they directly undermine the product\'s core value '
        'proposition of helping users make informed payment decisions. Without addressing these, TradeFlow\'s '
        'comparisons are theoretically interesting but practically unreliable for real financial decisions.',
        body_style
    ),
    Paragraph(
        '<b>Live FX Rates.</b> The current implementation uses hardcoded exchange rate approximations from '
        '2025. In a market where African currencies fluctuate significantly (the Nigerian Naira lost over 60% '
        'of its value against the USD in 2023-2024), stale rates make the entire comparison unreliable. Wise '
        'updates rates every 60 seconds. Monito queries provider APIs in real-time. TradeFlow should integrate '
        'central bank APIs (Bank of Ghana, Central Bank of Kenya, CBN) and fallback to aggregated feeds like '
        'ExchangeRate-API or Open Exchange Rates. The FxRateSnapshot model in the Prisma schema is already '
        'designed to store rate history, indicating this was always planned.',
        body_style
    ),
    Paragraph(
        '<b>Production Database.</b> SQLite with a local file is not viable for a multi-user production system. '
        'The comparison logging feature already writes to the database, and any concurrent access from multiple '
        'server instances (Vercel, Docker) will cause locking issues. Migration to PostgreSQL (Supabase, Neon) '
        'or Turso (libSQL) should be completed before activating user authentication. The Prisma schema requires '
        'minimal changes for this migration, making it a low-effort, high-impact fix.',
        body_style
    ),
    Paragraph(
        '<b>User Authentication.</b> While the Prisma schema includes User, Account, and Session models for '
        'NextAuth, and the package.json includes next-auth as a dependency, there is no sign-in UI, no auth '
        'middleware, and no protected routes. Phase 2\'s invoicing feature requires authenticated users to create '
        'and manage invoices. Without auth, the platform cannot persist user preferences, save comparison '
        'history, or send rate alerts. This is the foundational enabler for all subsequent phases.',
        body_style
    ),
    heading('<b>5.2 Important Gaps (Should Address in Phase 2)</b>', h2_style, 1),
    Paragraph(
        '<b>Historical Rate Charts.</b> Both Wise and Monito offer rate history visualization. Wise shows '
        '30-day rate trends alongside their transfer calculator. This feature builds trust by demonstrating '
        'rate volatility and helping users time their transfers. TradeFlow has Recharts in the dependency list, '
        'indicating charting capability was anticipated. The FxRateSnapshot model can store historical rates, '
        'enabling rate trend charts once live data is flowing. This should be implemented as part of the Phase 2 '
        'calculator enhancement, not deferred to a later phase.',
        body_style
    ),
    Paragraph(
        '<b>Delivery Method Filters.</b> Monito allows users to filter by delivery method (cash pickup, bank '
        'deposit, mobile money, home delivery). For African corridors, delivery method is often more important '
        'than price: a supplier in rural Kenya may only have access to mobile money, making bank transfer results '
        'irrelevant. Adding delivery method filters would significantly improve the practical utility of TradeFlow\'s '
        'comparison results for real African business scenarios. This is a medium-effort enhancement with high '
        'user impact.',
        body_style
    ),
    Paragraph(
        '<b>Amount-Specific Fee Structures.</b> The current FX engine applies percentage-based fee calculations. '
        'In reality, many providers use tiered fee structures (for example, Western Union charges different '
        'percentage fees for amounts below and above $500). The flat fee minimum and maximum caps in the current '
        'engine are a reasonable approximation, but they should be replaced with corridor-specific fee tables '
        'that reflect actual provider pricing. This data can be sourced from provider websites, the World Bank\'s '
        'Remittance Prices Worldwide database, and user-submitted reports.',
        body_style
    ),
    heading('<b>5.3 Nice-to-Have Gaps (Phase 3+)</b>', h2_style, 1),
    Paragraph(
        '<b>Rate Alerts.</b> Monito offers email alerts when rates for a specific corridor reach a user-defined '
        'threshold. For African businesses that make regular cross-border payments, knowing when the GHS-to-KES '
        'rate improves by 2% could save thousands of dollars annually. This requires the notification infrastructure '
        '(email via Resend or SendGrid, SMS via Africa\'s Talking) and a scheduled job system (cron or queue) to '
        'monitor rates and trigger alerts. This is a powerful retention feature that should be planned for Phase 3, '
        'once authenticated users and live rates are in place.',
        body_style
    ),
    Paragraph(
        '<b>Mobile App / PWA.</b> SendWave demonstrates that mobile-first design is critical for African markets. '
        'While TradeFlow\'s responsive web design works on mobile browsers, a Progressive Web App with offline '
        'rate caching, push notifications for rate alerts, and home screen installation would significantly improve '
        'the mobile experience. Next.js supports PWA configuration, and the existing Service Worker architecture '
        'from the FreeWave project provides reusable patterns for implementing this.',
        body_style
    ),
    Paragraph(
        '<b>Stablecoin Rail Comparison.</b> Fonbnk and Stellar-based solutions represent an emerging payment '
        'rail that could complement or undercut traditional methods. As Nigerian and Kenyan regulators develop '
        'stablecoin frameworks, adding USDC/cUSDT as a sixth comparison method would position TradeFlow as a '
        'forward-looking platform. This requires careful regulatory monitoring and should only be implemented '
        'when clarity exists in key markets. The phased architecture already supports adding new payment methods '
        'to the engine without structural changes.',
        body_style
    ),
])

# ══════════════════════════════════════════════════════════
# CHAPTER 6: TradeFlow's Unique Positioning
# ══════════════════════════════════════════════════════════
story.extend([
    heading('<b>6. TradeFlow Unique Positioning</b>', h1_style, 0),
    Spacer(1, 8),
    heading('<b>6.1 The White Space</b>', h2_style, 1),
    Paragraph(
        'TradeFlow has identified and occupied a genuinely uncontested market position. The white space can be '
        'defined along three dimensions that no existing competitor addresses simultaneously. First, PAPSS-aware '
        'comparison: no tool compares PAPSS routing against traditional methods for African corridors. Second, '
        'multi-rail comparison: existing tools compare providers (Wise versus Remitly), not infrastructure (PAPSS '
        'versus SWIFT versus mobile money versus stablecoin). Third, intra-Africa focus: Monito and Wise focus on '
        'diaspora-to-home corridors, while the $205 billion in annual African cross-border payments between '
        'African countries is largely unserved by comparison tools.',
        body_style
    ),
    Paragraph(
        'This triple white space is not accidental. It exists because PAPSS is still in its early adoption phase, '
        'with CBN mandating adoption in Nigeria but regulatory barriers slowing uptake in other jurisdictions. '
        'The opportunity is time-sensitive: as PAPSS adoption accelerates (driven by AfCFTA trade growth and '
        'central bank mandates), competitors will eventually recognize this space. TradeFlow\'s first-mover '
        'advantage depends on establishing brand recognition and data density before well-funded entrants arrive.',
        body_style
    ),
    heading('<b>6.2 Positioning Statement</b>', h2_style, 1),
    Paragraph(
        'Based on the competitive analysis, TradeFlow\'s positioning should be refined as follows: "TradeFlow is '
        'the first and only comparison engine that shows African businesses how much they save by using PAPSS '
        'instead of traditional cross-border payment methods. We compare payment rails, not just providers, '
        'so you see the true cost of every option including SWIFT, mobile money, MTOs, and fintech platforms." '
        'This positioning is defensible because it requires deep knowledge of African payment infrastructure, '
        'corridor-specific fee structures, and PAPSS settlement mechanics that generalist tools like Monito lack.',
        body_style
    ),
])

# ══════════════════════════════════════════════════════════
# CHAPTER 7: Strategic Recommendations
# ══════════════════════════════════════════════════════════
story.extend([
    heading('<b>7. Strategic Recommendations for Phase 2+</b>', h1_style, 0),
    Spacer(1, 8),
    heading('<b>7.1 Phase 2 Priorities (Invoicing and Receivables)</b>', h2_style, 1),
    Paragraph(
        'Phase 2 should deliver three outcomes beyond the core invoicing feature. First, activate user '
        'authentication using the existing NextAuth schema with email and Google OAuth providers. This is '
        'non-negotiable because invoices require an authenticated creator. Second, migrate to a production database '
        '(recommended: Turso for cost efficiency or Supabase for the free tier and built-in auth). Third, '
        'integrate live FX rates from central bank APIs with a 60-second cache, displaying the rate timestamp '
        'and source on every comparison result. These three infrastructure upgrades are prerequisites for the '
        'invoicing feature to function in a real-world context.',
        body_style
    ),
    Paragraph(
        'For the invoicing feature itself, the competitive audit reveals that no competitor offers invoice '
        'functionality with built-in PAPSS cost optimization. This means TradeFlow can define the category rather '
        'than compete within it. The invoice should include an "estimated PAPSS savings" line item that shows the '
        'receiver how much they would save if the invoice were paid via PAPSS versus traditional methods. This '
        'turns every invoice into a PAPSS advocacy tool and differentiates TradeFlow invoices from generic '
        'invoicing products like Wave, Zoho, or Invoice Ninja.',
        body_style
    ),
    heading('<b>7.2 Phase 3 Priorities (Payment Facilitation API)</b>', h2_style, 1),
    Paragraph(
        'Phase 3 should implement the affiliate and partnership model that Monito has validated. Rather than '
        'becoming a payment processor (which requires expensive licensing), TradeFlow should serve as the '
        'transparent discovery layer that connects businesses to existing payment providers. The API should '
        'return structured comparison results that developers can embed in their own applications, with affiliate '
        'referral links for each payment method. Flutterwave\'s Barter API and Africa\'s Talking\'s payment API '
        'are potential integration partners. The affiliate revenue model means TradeFlow earns when users act on '
        'its recommendations, creating a sustainable business without needing to hold or transfer funds.',
        body_style
    ),
    heading('<b>7.3 Phase 4 Priorities (Trade Marketplace)</b>', h2_style, 1),
    Paragraph(
        'The trade marketplace should be built on the data density that Phases 1-3 generate. By Phase 4, '
        'TradeFlow will have data on thousands of comparison queries, revealing which corridors are most in '
        'demand, which payment methods are most popular, and what the typical transaction sizes are. This data '
        'should inform marketplace features: curated supplier directories for high-demand corridors, verified '
        'business profiles with PAPSS capability badges, and corridor-specific trade intelligence reports. The '
        'marketplace is the long-term monetization engine, but it depends entirely on the trust and data built '
        'in earlier phases. Attempting to launch a marketplace without the FX comparison and invoicing foundation '
        'would result in an empty marketplace with no network effects.',
        body_style
    ),
    heading('<b>7.4 Cross-Phase Requirements</b>', h2_style, 1),
    Paragraph(
        'Several capabilities span all phases and should be treated as continuous investments rather than phase-gated '
        'features. Compliance infrastructure (KYC/AML verification, data residency, regulatory monitoring) must be '
        'built incrementally from Phase 2 onward because regulatory requirements will expand as the product moves '
        'from anonymous comparison to authenticated invoicing to payment facilitation. Performance monitoring and '
        'analytics should track comparison volume, corridor demand, conversion to paid actions, and user retention. '
        'SEO and content marketing should target corridor-specific keywords (for example, "GHS to KES transfer cost" '
        'or "PAPSS payment Nigeria") to capture organic search demand that currently has no authoritative answer.',
        body_style
    ),
])

# ══════════════════════════════════════════════════════════
# CHAPTER 8: Risk Assessment
# ══════════════════════════════════════════════════════════
story.extend([
    heading('<b>8. Risk Assessment</b>', h1_style, 0),
    Spacer(1, 8),
    Paragraph(
        'The competitive audit also surfaces several risks that could undermine TradeFlow\'s positioning if '
        'not actively managed. The most significant risk is that a well-funded competitor (Flutterwave, Stripe, '
        'or a new entrant) recognizes the PAPSS comparison opportunity and builds a competing product with '
        'superior resources. The mitigation is speed: TradeFlow must establish brand recognition and user trust '
        'before this happens. A second risk is PAPSS adoption stalling due to regulatory fragmentation across '
        'African central banks. If PAPSS fails to gain traction, the core value proposition weakens. The '
        'mitigation is to frame TradeFlow as an "African cross-border payment cost comparison" tool that '
        'happens to include PAPSS as one rail among many, rather than a "PAPSS-only" tool.',
        body_style
    ),
    Paragraph(
        'A third risk is data accuracy: if TradeFlow\'s fee estimates are significantly different from what users '
        'actually pay, trust will erode quickly. The mitigation is to implement user-reported actual costs (a '
        '"Did you save as much as we predicted?" feedback loop) and continuously calibrate the engine against '
        'real-world data. A fourth risk is regulatory risk around providing financial information without a '
        'license. TradeFlow does not execute payments and therefore may not require a money transmitter license, '
        'but legal review is needed in each target market. The compliance-by-design principle from the original '
        'project brief should guide all architectural decisions to minimize regulatory exposure.',
        body_style
    ),
])

# Build
doc.pageTemplates = [template]
doc.multiBuild(story)
print(f'Body PDF generated: {OUTPUT}')
