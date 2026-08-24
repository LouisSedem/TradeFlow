#!/usr/bin/env python3
"""TradeFlow Global Competitive Benchmark Audit - Body PDF (ReportLab)"""

import os, sys, hashlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'skills', 'pdf', 'scripts'))
from pdf import install_font_fallback

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, Image
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
import platform

# ── Font Setup ──
_IS_MAC = platform.system() == 'Darwin'
FONT_DIR = os.path.expanduser('~/.openclaw/workspace/fonts') if _IS_MAC else '/usr/share/fonts'

pdfmetrics.registerFont(TTFont('FreeSerif', f'{FONT_DIR}/truetype/freefont/FreeSerif.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-Bold', f'{FONT_DIR}/truetype/freefont/FreeSerifBold.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-Italic', f'{FONT_DIR}/truetype/freefont/FreeSerifItalic.ttf'))
pdfmetrics.registerFont(TTFont('FreeSerif-BoldItalic', f'{FONT_DIR}/truetype/freefont/FreeSerifBoldItalic.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans', f'{FONT_DIR}/truetype/dejavu/DejaVuSansMono.ttf'))

registerFontFamily('FreeSerif', normal='FreeSerif', bold='FreeSerif-Bold',
                    italic='FreeSerif-Italic', boldItalic='FreeSerif-BoldItalic')
registerFontFamily('DejaVuSans', normal='DejaVuSans', bold='DejaVuSans')

install_font_fallback()

# ── Cascade Palette ──
PAGE_BG       = colors.HexColor('#f3f2f1')
SECTION_BG    = colors.HexColor('#f2f2f1')
CARD_BG       = colors.HexColor('#e8e7e4')
TABLE_STRIPE  = colors.HexColor('#eeeeeb')
HEADER_FILL   = colors.HexColor('#68614b')
COVER_BLOCK   = colors.HexColor('#8c7f58')
BORDER        = colors.HexColor('#d8d3c2')
ICON          = colors.HexColor('#9c8b58')
ACCENT        = colors.HexColor('#95771c')
ACCENT_2      = colors.HexColor('#52a4bf')
TEXT_PRIMARY   = colors.HexColor('#1a1917')
TEXT_MUTED     = colors.HexColor('#827f78')
SEM_SUCCESS   = colors.HexColor('#448359')
SEM_WARNING   = colors.HexColor('#a6843f')
SEM_ERROR     = colors.HexColor('#99544e')
SEM_INFO      = colors.HexColor('#55789a')

# ── Page Setup ──
PAGE_W, PAGE_H = A4
LEFT_M = 1.0 * inch
RIGHT_M = 1.0 * inch
TOP_M = 0.9 * inch
BOTTOM_M = 0.9 * inch
CONTENT_W = PAGE_W - LEFT_M - RIGHT_M

OUTPUT = os.path.join(os.path.dirname(__file__), '..', 'download', 'global-audit-body.pdf')

# ── Styles ──
body_style = ParagraphStyle(
    name='Body', fontName='FreeSerif', fontSize=10.5, leading=17,
    alignment=TA_JUSTIFY, spaceAfter=8, textColor=TEXT_PRIMARY
)
h1_style = ParagraphStyle(
    name='H1', fontName='FreeSerif-Bold', fontSize=20, leading=26,
    spaceBefore=18, spaceAfter=10, textColor=TEXT_PRIMARY
)
h2_style = ParagraphStyle(
    name='H2', fontName='FreeSerif-Bold', fontSize=14, leading=20,
    spaceBefore=14, spaceAfter=8, textColor=TEXT_PRIMARY
)
h3_style = ParagraphStyle(
    name='H3', fontName='FreeSerif-Bold', fontSize=11.5, leading=16,
    spaceBefore=10, spaceAfter=6, textColor=TEXT_PRIMARY
)
bullet_style = ParagraphStyle(
    name='Bullet', fontName='FreeSerif', fontSize=10.5, leading=17,
    leftIndent=18, bulletIndent=6, spaceAfter=4, textColor=TEXT_PRIMARY,
    alignment=TA_LEFT
)
caption_style = ParagraphStyle(
    name='Caption', fontName='FreeSerif-Italic', fontSize=9, leading=13,
    alignment=TA_CENTER, spaceBefore=3, spaceAfter=6, textColor=TEXT_MUTED
)
callout_style = ParagraphStyle(
    name='Callout', fontName='FreeSerif-Bold', fontSize=11, leading=16,
    leftIndent=12, borderPadding=6, spaceBefore=6, spaceAfter=6,
    textColor=ACCENT, alignment=TA_LEFT
)
header_cell_style = ParagraphStyle(
    name='HeaderCell', fontName='FreeSerif-Bold', fontSize=9.5, leading=13,
    alignment=TA_CENTER, textColor=colors.white
)
cell_style = ParagraphStyle(
    name='Cell', fontName='FreeSerif', fontSize=9, leading=13,
    alignment=TA_CENTER, textColor=TEXT_PRIMARY
)
cell_left_style = ParagraphStyle(
    name='CellLeft', fontName='FreeSerif', fontSize=9, leading=13,
    alignment=TA_LEFT, textColor=TEXT_PRIMARY
)
toc_h1 = ParagraphStyle(
    name='TOCH1', fontName='FreeSerif-Bold', fontSize=12, leading=20,
    leftIndent=0, textColor=TEXT_PRIMARY
)
toc_h2 = ParagraphStyle(
    name='TOCH2', fontName='FreeSerif', fontSize=10.5, leading=18,
    leftIndent=20, textColor=TEXT_PRIMARY
)

# ── Helpers ──
def add_heading(text, style, level=0):
    key = f'h_{hashlib.md5(text.encode()).hexdigest()[:8]}'
    p = Paragraph(f'<a name="{key}"/>{text}', style)
    p.bookmark_name = key
    p.bookmark_level = level
    p.bookmark_text = text
    p.bookmark_key = key
    return p

def make_table(headers, rows, col_ratios=None):
    avail = CONTENT_W
    if col_ratios is None:
        col_ratios = [1.0 / len(headers)] * len(headers)
    col_widths = [r * avail for r in col_ratios]
    data = [[Paragraph(f'<b>{h}</b>', header_cell_style) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), cell_left_style if i == 0 else cell_style) for i, c in enumerate(row)])
    t = Table(data, colWidths=col_widths, hAlign='CENTER')
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), HEADER_FILL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        bg = colors.white if i % 2 == 1 else TABLE_STRIPE
        style_cmds.append(('BACKGROUND', (0, i), (-1, i), bg))
    t.setStyle(TableStyle(style_cmds))
    return t

def safe_keep(elements):
    total_h = sum(e.wrap(CONTENT_W, PAGE_H)[1] for e in elements)
    max_h = PAGE_H * 0.4
    if total_h <= max_h:
        return [KeepTogether(elements)]
    elif len(elements) >= 2:
        return [KeepTogether(elements[:2])] + list(elements[2:])
    return list(elements)

# ── TocDocTemplate ──
class TocDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if hasattr(flowable, 'bookmark_name'):
            level = getattr(flowable, 'bookmark_level', 0)
            text = getattr(flowable, 'bookmark_text', '')
            key = getattr(flowable, 'bookmark_key', '')
            self.notify('TOCEntry', (level, text, self.page, key))

def page_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('FreeSerif', 8)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawRightString(PAGE_W - RIGHT_M, BOTTOM_M - 20, f'Page {doc.page}')
    canvas.drawString(LEFT_M, BOTTOM_M - 20, 'TradeFlow Global Competitive Benchmark Audit')
    canvas.restoreState()

doc = TocDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=LEFT_M, rightMargin=RIGHT_M,
    topMargin=TOP_M, bottomMargin=BOTTOM_M,
    title='TradeFlow Global Competitive Benchmark Audit',
    author='Z.ai', creator='Z.ai',
    subject='Competitive analysis of TradeFlow vs global cross-border payment platforms'
)

# ── Build Story ──
story = []

# TOC
toc = TableOfContents()
toc.levelStyles = [toc_h1, toc_h2]
story.append(toc)
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# CHAPTER 1: Executive Summary
# ═══════════════════════════════════════════════════════════════
story.append(add_heading('<b>1. Executive Summary</b>', h1_style, 0))
story.append(Paragraph(
    'TradeFlow is a PAPSS-optimized cross-border FX comparison platform designed for African businesses '
    'trading under the AfCFTA framework. Following a successful first competitive audit focused on African '
    'competitors and the implementation of six priority recommendations (live FX rates, historical charts, '
    'authentication, delivery filters, rate alerts, and PWA support), this second audit expands the scope to '
    'benchmarks across four major global regions: North America, Asia, Europe, and the United Kingdom. The '
    'objective is to identify feature gaps, UX patterns, and monetization strategies employed by mature '
    'cross-border payment platforms that could inform TradeFlow roadmap decisions as it scales beyond Phase 1.',
    body_style
))
story.append(Spacer(1, 6))
story.append(Paragraph(
    'This audit examines twelve leading platforms across four regions, analyzing their approaches to FX '
    'transparency, user onboarding, delivery method diversity, mobile experience, API and integration '
    'ecosystems, regulatory compliance, and revenue models. Each regional section concludes with a gap '
    'analysis identifying specific capabilities TradeFlow should consider adopting or adapting for the African '
    'cross-border payment corridor. The final chapter synthesizes these findings into a prioritized '
    'recommendation roadmap aligned with TradeFlow four-phase product strategy.',
    body_style
))
story.append(Spacer(1, 12))

# Key Findings Callout
story.append(add_heading('<b>1.1 Key Findings at a Glance</b>', h2_style, 1))
story.append(Paragraph(
    'Across all four regions, several consistent patterns emerged that have direct implications for '
    'TradeFlow product strategy. First, every major competitor offers API-based integration for '
    'business customers, positioning FX comparison as infrastructure rather than a standalone tool. '
    'Second, mobile-first design is no longer optional; platforms like Wise, Remitly, and Airwallex have '
    'built their entire user journeys around mobile interfaces with minimal desktop offerings. Third, '
    'regulatory licensing is used as a competitive moat; Wise alone holds over 50 regulatory licenses '
    'globally, and this infrastructure enables instant settlement that competitors without licenses cannot match.',
    body_style
))
story.append(Spacer(1, 6))
story.append(Paragraph(
    'Fourth, dynamic pricing engines that adjust fees based on corridor volume, payment method, and delivery '
    'speed are now standard. Static fee tables are perceived as opaque by users accustomed to seeing '
    'real-time rate comparisons. Fifth, value-added services such as invoicing, payment tracking, supplier '
    'management, and multi-currency accounts serve as the primary conversion funnel from free comparison '
    'tools to paid SaaS subscriptions. These findings directly validate TradeFlow planned Phase 2 through '
    'Phase 4 features while highlighting specific implementation details that differentiate market leaders.',
    body_style
))

story.append(Spacer(1, 18))

# ═══════════════════════════════════════════════════════════════
# CHAPTER 2: North America
# ═══════════════════════════════════════════════════════════════
story.append(add_heading('<b>2. North America: Wise, Remitly, and CurrencyFair</b>', h1_style, 0))

story.append(add_heading('<b>2.1 Wise (formerly TransferWise)</b>', h2_style, 1))
story.append(Paragraph(
    'Wise, founded in 2011 and headquartered in London with a significant North American presence, is the '
    'global benchmark for transparent cross-border payments. The platform serves over 16 million customers '
    'across 80+ countries and processes billions of dollars in annual transfer volume. Wise core value '
    'proposition is deceptively simple: show users the real mid-market exchange rate and charge a transparent '
    'fee on top, eliminating the hidden markups that traditional banks and money transfer operators have '
    'relied upon for decades. This radical transparency has disrupted the entire industry and set the '
    'standard that every FX comparison platform, including TradeFlow, must now meet or exceed.',
    body_style
))
story.append(Spacer(1, 6))
story.append(Paragraph(
    'The Wise platform architecture is built on a proprietary local account network spanning over 80 countries, '
    'which enables transfers that settle locally rather than through the SWIFT correspondent banking network. '
    'This means a payment from the United States to the United Kingdom, for example, is routed through Wise '
    'local US and UK accounts, achieving same-day settlement at a fraction of the cost of a traditional wire '
    'transfer. The technical sophistication required to maintain this network is substantial, involving '
    'regulatory licensing in each jurisdiction, banking partnerships for local account issuance, and real-time '
    'liquidity management across dozens of currency positions. For TradeFlow, the PAPSS infrastructure '
    'provides a similar advantage for African corridors, and this parallel is worth emphasizing in product '
    'messaging: just as Wise bypassed SWIFT for major currencies, PAPSS bypasses correspondent banking for '
    'African currencies.',
    body_style
))
story.append(Spacer(1, 6))
story.append(Paragraph(
    'From a product design perspective, Wise interface is remarkably focused. The primary interaction is a '
    'single input field where users enter an amount and select currencies, immediately seeing the mid-market '
    'rate, the total fee, and the exact amount the recipient will receive. There are no complex settings, no '
    'tiered pricing confusion, and no distracting upsell prompts. This simplicity is the result of years of '
    'UX iteration and represents the gold standard for FX comparison interfaces. TradeFlow Phase 1 calculator '
    'follows a similar pattern, but the addition of PAPSS-specific corridor optimization and the ability to '
    'compare against mobile money and cash pickup methods provides differentiation that Wise does not offer '
    'for African corridors. Wise also offers multi-currency accounts (Wise Account), debit cards, and business '
    'API integration, which aligns closely with TradeFlow planned Phase 2-4 roadmap.',
    body_style
))

story.append(add_heading('<b>2.2 Remitly</b>', h2_style, 1))
story.append(Paragraph(
    'Remitly, headquartered in Seattle, Washington, focuses specifically on the remittance market with a strong '
    'emphasis on corridors serving immigrant communities in North America sending money to developing '
    'countries. The platform processes transfers to over 170 countries and has particularly strong presence in '
    'Latin American, Southeast Asian, and African corridors. Unlike Wise, which targets both businesses and '
    'individuals with a transparent mid-market rate model, Remitly offers a tiered delivery model that directly '
    'maps to TradeFlow current delivery method filter system: Economy transfers take 3-5 business days but '
    'offer lower fees, while Express transfers arrive within minutes for a premium. This tiered approach is '
    'particularly relevant for African corridors where recipients may prioritize speed (mobile money instant '
    'delivery) over cost savings (bank transfer with 2-3 day settlement).',
    body_style
))
story.append(Spacer(1, 6))
story.append(Paragraph(
    'Remitly mobile-first design philosophy offers important lessons for TradeFlow. Over 80% of Remitly '
    'transactions originate from mobile devices, and the entire user journey from initial download to first '
    'transfer completion is optimized for smartphone interaction. The app features one-tap repeat transfers, '
    'push notification delivery confirmations, biometric authentication, and integration with mobile money '
    'networks across Africa (including M-Pesa, MTN Mobile Money, and Airtel Money). TradeFlow PWA support is a '
    'step in the right direction, but Remitly native app experience with offline capability, device-level '
    'biometrics, and deep OS integration represents a higher bar that should be targeted as TradeFlow mobile '
    'strategy matures. Remitly also provides real-time transfer tracking with SMS and email notifications at '
    'each processing stage, a feature that TradeFlow Phase 2 payment tracking should emulate.',
    body_style
))

story.append(add_heading('<b>2.3 CurrencyFair</b>', h2_style, 1))
story.append(Paragraph(
    'CurrencyFair, founded in Ireland and serving North American customers through its registered operations, '
    'takes a fundamentally different approach to FX comparison by operating a peer-to-peer currency exchange '
    'marketplace. Rather than setting rates internally, CurrencyFair allows users to set their own exchange rates '
    'and match with other users willing to take the opposite side of the trade. This model can produce rates that '
    'are even closer to the mid-market rate than traditional money transfer services, particularly for high-volume '
    'corridors where there is sufficient liquidity. The marketplace model introduces an interesting parallel for '
    'TradeFlow: as PAPSS adoption grows and more banks connect to the system, a similar liquidity-driven rate '
    'optimization could emerge for African currency pairs that currently suffer from thin markets.',
    body_style
))
story.append(Spacer(1, 6))
story.append(Paragraph(
    'CurrencyFair business-focused features are particularly relevant for TradeFlow planned Phase 2 invoicing '
    'tools. The platform offers automated recurring transfers at user-specified rate thresholds, bulk payment '
    'processing for businesses paying multiple suppliers, and a dedicated business dashboard with multi-user '
    'access controls. These features address the exact pain points of African SMEs engaged in cross-border trade: '
    'the need to make regular payments to multiple suppliers across different currency zones, the desire to lock '
    'in favorable rates when they appear, and the requirement for audit trails and approval workflows in a '
    'business context. TradeFlow rate alert system (implemented in the first audit cycle) addresses the rate '
    'threshold notification piece, but extending this to automated execution would be a significant competitive '
    'advantage in Phase 2.',
    body_style
))

story.append(add_heading('<b>2.4 North America Gap Analysis</b>', h2_style, 1))
story.extend(safe_keep([
    Spacer(1, 10),
    make_table(
        ['Feature', 'Wise', 'Remitly', 'CurrencyFair', 'TradeFlow'],
        [
            ['Live FX Rates', 'Yes', 'Yes', 'Market-driven', 'Yes'],
            ['Delivery Filters', 'Bank only', '3 tiers', 'Bank + Wire', '4 methods'],
            ['Rate Alerts', 'Yes', 'No', 'Yes (auto-execute)', 'Yes (notify only)'],
            ['Mobile Money', 'Limited', 'Extensive', 'No', 'Yes (comparison)'],
            ['Historical Charts', 'Yes (1 year)', 'No', 'Yes (30 day)', 'Yes (30 day sim.)'],
            ['API for Business', 'Full REST API', 'Limited', 'Yes', 'Planned Phase 3'],
            ['Multi-currency Account', 'Yes', 'No', 'Yes', 'Planned Phase 2'],
            ['Recurring Payments', 'Yes', 'Yes', 'Yes', 'Not yet'],
        ],
        [0.20, 0.16, 0.16, 0.20, 0.28]
    ),
    Paragraph('<b>Table 1.</b> North America Competitive Feature Matrix', caption_style),
]))
story.append(Spacer(1, 12))

# ═══════════════════════════════════════════════════════════════
# CHAPTER 3: Asia
# ═══════════════════════════════════════════════════════════════
story.append(add_heading('<b>3. Asia: InstaReM, Airwallex, and Wise Asia</b>', h1_style, 0))

story.append(add_heading('<b>3.1 InstaReM</b>', h2_style, 1))
story.append(Paragraph(
    'InstaReM, headquartered in Singapore, has established itself as the dominant cross-border payment '
    'platform for Asia-Pacific corridors, processing transfers to over 80 countries with particular strength '
    'in South-South payment corridors that parallel the African trade flows TradeFlow targets. The platform '
    'was built from the ground up to serve the specific needs of emerging market corridors, including '
    'lower-value transfers, mobile wallet delivery, and regulatory compliance across jurisdictions with less '
    'mature financial infrastructure. This positioning makes InstaReM perhaps the most directly comparable '
    'global platform to TradeFlow in terms of target market characteristics, even though it operates in '
    'different geographies.',
    body_style
))
story.append(Spacer(1, 6))
story.append(Paragraph(
    'InstaReM approach to FX transparency is notably similar to TradeFlow Phase 1 implementation. The '
    'platform displays the exchange rate, total fees, and recipient amount upfront before any commitment is '
    'required. However, InstaReM goes further by providing a rate guarantee window: once a rate is quoted, it '
    'is locked for a specific period (typically 30 seconds to 2 minutes depending on corridor volatility), '
    'giving users confidence that the rate they see is the rate they will receive. This rate-locking mechanism '
    'is a feature that TradeFlow should consider implementing in Phase 2, particularly for PAPSS corridors where '
    'rates can fluctuate during the time it takes a user to complete a transfer instruction. Additionally, '
    'InstaReM provides a detailed fee breakdown that separates the platform service fee from the FX margin, '
    'allowing sophisticated users to understand exactly where their money is going.',
    body_style
))

story.append(add_heading('<b>3.2 Airwallex</b>', h2_style, 1))
story.append(Paragraph(
    'Airwallex, founded in Melbourne, Australia, and now headquartered in Hong Kong, represents the enterprise '
    'end of the cross-border payment spectrum. Unlike Wise or Remitly, which primarily serve individuals and '
    'small businesses, Airwallex targets mid-market and enterprise clients with a comprehensive financial '
    'infrastructure platform that includes FX treasury management, international payment processing, '
    'expense management, and embedded finance APIs. The platform processes over USD 50 billion in annual '
    'transaction volume and serves more than 100,000 businesses globally, including major enterprises like '
    'Xero, HubSpot, and Shoei. Airwallex approach demonstrates the revenue potential available when an FX '
    'comparison tool evolves into a full financial operations platform, which is precisely the trajectory '
    'TradeFlow four-phase roadmap describes.',
    body_style
))
story.append(Spacer(1, 6))
story.append(Paragraph(
    'The Airwallex API ecosystem is particularly instructive for TradeFlow Phase 3 planning. The platform offers '
    'a comprehensive REST API with dedicated SDKs for Python, Node.js, Java, and Ruby, enabling businesses to '
    'embed cross-border payment capabilities directly into their own applications and workflows. The API covers '
    'quote generation, payment creation, beneficiary management, account management, and webhook notifications '
    'for real-time payment status updates. Critically, Airwallex provides sandbox environments for developers '
    'to test integrations without risking real money, comprehensive API documentation with interactive '
    'examples, and dedicated developer support channels. This developer-experience-first approach to API '
    'product design should be a key reference for TradeFlow Phase 3 API development. The embedded finance '
    'trend that Airwallex pioneered in Asia is now expanding globally, and African fintechs that can offer '
    'similar embedded payment capabilities will be well-positioned to capture B2B SaaS revenue.',
    body_style
))

story.append(add_heading('<b>3.3 Wise Asia Pacific Operations</b>', h2_style, 1))
story.append(Paragraph(
    'Wise presence in the Asia-Pacific region demonstrates how a global FX platform adapts to local market '
    'conditions. In markets like India, the Philippines, and Indonesia, Wise has partnered with local banks and '
    'mobile wallet providers to enable last-mile delivery methods that go beyond bank deposits. In India, for '
    'example, Wise supports UPI (Unified Payments Interface) delivery, enabling instant transfers directly to '
    'recipients bank accounts or UPI IDs. In the Philippines, Wise integrates with GCash and Maya (formerly '
    'PayMaya), the two dominant mobile wallets. This localization strategy is directly applicable to '
    'TradeFlow: the platform already supports mobile money delivery comparison, but deepening integration with '
    'specific mobile money networks (M-Pesa, MTN Mobile Money, Airtel Money, MoMo) to enable instant delivery '
    'confirmation and real-time balance updates would significantly enhance the user experience and '
    'differentiate TradeFlow from competitors that treat Africa as a monolith.',
    body_style
))

story.append(add_heading('<b>3.4 Asia Gap Analysis</b>', h2_style, 1))
story.extend(safe_keep([
    Spacer(1, 10),
    make_table(
        ['Feature', 'InstaReM', 'Airwallex', 'Wise Asia', 'TradeFlow'],
        [
            ['Rate Lock Window', '30s - 2min', 'Custom', 'No', 'No'],
            ['Enterprise API', 'Limited', 'Full REST + SDKs', 'Full REST API', 'Planned Phase 3'],
            ['Mobile Wallet Depth', 'Moderate', 'Extensive', 'Deep (UPI, GCash)', 'Basic (comparison)'],
            ['Developer Sandbox', 'No', 'Yes', 'Yes', 'Not yet'],
            ['Fee Breakdown', 'Service + FX', 'Transparent', 'Single fee', 'Full breakdown'],
            ['Corridor Optimization', 'South-South focus', 'Global enterprise', 'Corridor-specific', 'PAPSS-optimized'],
            ['Treasury Management', 'No', 'Yes (advanced)', 'Multi-currency', 'Not yet'],
        ],
        [0.22, 0.18, 0.20, 0.20, 0.20]
    ),
    Paragraph('<b>Table 2.</b> Asia-Pacific Competitive Feature Matrix', caption_style),
]))
story.append(Spacer(1, 12))

# ═══════════════════════════════════════════════════════════════
# CHAPTER 4: Europe
# ═══════════════════════════════════════════════════════════════
story.append(add_heading('<b>4. Europe: Wise EU, Revolut Business, and CurrencyFair EU</b>', h1_style, 0))

story.append(add_heading('<b>4.1 Wise European Operations</b>', h2_style, 1))
story.append(Paragraph(
    'Wise European operations, headquartered in Brussels and regulated by the National Bank of Belgium as an '
    'authorized payment institution under PSD2 (Payment Services Directive 2), represent the most mature '
    'implementation of cross-border payment infrastructure in any single market. The European regulatory '
    'framework under PSD2 and the subsequent PSR (Payment Services Regulation) has created an environment '
    'where cross-border payments within the SEPA (Single Euro Payments Area) zone are functionally equivalent '
    'to domestic payments in terms of cost and speed. This regulatory environment has shaped Wise European '
    'product in specific ways that offer both lessons and cautionary notes for TradeFlow African market strategy.',
    body_style
))
story.append(Spacer(1, 6))
story.append(Paragraph(
    'The most significant lesson from Wise European operations is the power of regulatory integration to '
    'reduce friction. Within SEPA, a transfer from Germany to Spain costs the same as a transfer from Munich '
    'to Berlin and settles on the same timeline. PAPSS aims to achieve a similar effect for African currencies, '
    'and if successful, would create analogous opportunities for TradeFlow to expand its comparison engine to '
    'intra-African corridors with the same level of transparency and speed that SEPA enables in Europe. Wise '
    'has also leveraged Open Banking regulations under PSD2 to initiate payments directly from user bank '
    'accounts without requiring manual bank transfer instructions, reducing friction and improving conversion '
    'rates. As African markets develop their own Open Banking frameworks (Nigeria already has CBN Open Banking '
    'regulations, and Kenya is advancing similar initiatives), TradeFlow should plan to integrate account-to-account '
    'payment initiation capabilities that would mirror the Wise European Open Banking experience.',
    body_style
))

story.append(add_heading('<b>4.2 Revolut Business</b>', h2_style, 1))
story.append(Paragraph(
    'Revolut Business, the enterprise arm of the London-based fintech super-app, approaches cross-border payments '
    'from a fundamentally different angle than dedicated FX comparison platforms. Rather than focusing on '
    'transparency and comparison, Revolut Business bundles FX capabilities into a comprehensive financial '
    'management platform that includes business banking, corporate cards, expense management, invoicing, and '
    'multi-currency accounts. The platform serves over 500,000 business customers globally and offers exchange '
    'rates that are competitive with (though not always identical to) the mid-market rate, with premium tiers '
    'offering higher limits and additional features. Revolut Business strategy of using FX as a feature within a '
    'broader financial suite rather than as a standalone product is directly relevant to TradeFlow Phase 2-4 '
    'roadmap, which envisions evolving from an FX comparison tool into a comprehensive trade finance platform.',
    body_style
))
story.append(Spacer(1, 6))
story.append(Paragraph(
    'The Revolut Business user interface demonstrates several UX patterns that TradeFlow should study carefully. '
    'The platform uses a unified dashboard that displays all financial activity (transactions, card spending, '
    'FX conversions, invoices) in a single timeline view, reducing the cognitive load of managing cross-border '
    'financial operations. The FX conversion flow is embedded naturally within this dashboard: users see their '
    'multi-currency balances, can convert between currencies with a single tap, and immediately use the '
    'converted funds for payments or card transactions. This seamless integration of FX into a broader financial '
    'workflow is the end state that TradeFlow should aim for in its Phase 4 trade marketplace vision. Additionally, '
    'Revolut Business team management features (role-based access, approval workflows, spending limits) are '
    'essential for the B2B segment that TradeFlow will increasingly serve as it moves beyond individual '
    'comparison users to business customers with multiple stakeholders involved in payment decisions.',
    body_style
))

story.append(add_heading('<b>4.3 European Gap Analysis</b>', h2_style, 1))
story.extend(safe_keep([
    Spacer(1, 10),
    make_table(
        ['Feature', 'Wise EU', 'Revolut Business', 'CurrencyFair EU', 'TradeFlow'],
        [
            ['Open Banking Initiation', 'PSD2 Full', 'Partial', 'No', 'Not yet'],
            ['SEPA Integration', 'Native', 'Native', 'Via banks', 'N/A (PAPSS)'],
            ['Team Management', 'No', 'Full RBAC', 'Basic', 'Not yet'],
            ['Expense Management', 'No', 'Full suite', 'No', 'Not yet'],
            ['Corporate Cards', 'Yes', 'Yes', 'No', 'Not yet'],
            ['Invoicing', 'No', 'Yes', 'No', 'Planned Phase 2'],
            ['FX as Feature vs Product', 'Product', 'Feature (bundled)', 'Product', 'Product (evolving)'],
            ['Regulatory Moat', '50+ licenses', '40+ licenses', '10+ licenses', 'Emerging'],
        ],
        [0.22, 0.18, 0.20, 0.18, 0.22]
    ),
    Paragraph('<b>Table 3.</b> European Competitive Feature Matrix', caption_style),
]))
story.append(Spacer(1, 12))

# ═══════════════════════════════════════════════════════════════
# CHAPTER 5: United Kingdom
# ═══════════════════════════════════════════════════════════════
story.append(add_heading('<b>5. United Kingdom: Wise UK, OFX, and WorldRemit</b>', h1_style, 0))

story.append(add_heading('<b>5.1 Wise UK</b>', h2_style, 1))
story.append(Paragraph(
    'The United Kingdom is Wise home market and the location where the platform has its deepest integration with '
    'the local financial ecosystem. Regulated by the Financial Conduct Authority (FCA) as an Authorized Payment '
    'Institution, Wise UK offers the full suite of Wise capabilities including the Wise Account (multi-currency '
    'account with local UK account details), international transfers, the Wise debit card, and business-focused '
    'features such as batch payments and API integration. The UK market is particularly relevant for TradeFlow '
    'because of the significant trade and remittance flows between the UK and African countries: Nigeria, Ghana, '
    'Kenya, and South Africa are all among the top remittance corridors from the UK, and the UK-Africa trade '
    'relationship continues to grow under post-Brexit trade agreements.',
    body_style
))
story.append(Spacer(1, 6))
story.append(Paragraph(
    'Wise UK product design offers a specific lesson in trust-building through transparency that TradeFlow should '
    'emulate. Every Wise transfer confirmation screen displays a detailed cost breakdown showing the mid-market '
    'rate, the applied margin (if any), the service fee, and the total cost as a percentage of the transfer '
    'amount. This level of transparency has been a key driver of Wise customer acquisition through word-of-mouth '
    'referrals, as users can objectively demonstrate to friends and family that they are getting a better deal '
    'than traditional banks. TradeFlow PAPSS comparison already provides fee transparency, but extending this to '
    'show the percentage cost saving compared to the next-best alternative (as Wise does) would strengthen the '
    'value proposition and encourage organic referral growth within African business communities. Wise UK also '
    'provides FSCS (Financial Services Compensation Scheme) protection for UK-issued cards, demonstrating how '
    'regulatory consumer protection frameworks can be leveraged as trust signals in marketing.',
    body_style
))

story.append(add_heading('<b>5.2 OFX</b>', h2_style, 1))
story.append(Paragraph(
    'OFX (formerly OzForex), founded in Australia in 1998 and with significant UK operations, represents the '
    'high-value, relationship-driven segment of the cross-border payment market. Unlike Wise and Remitly, which '
    'are designed for self-service digital transactions, OFX targets customers making larger transfers '
    '(typically above GBP 5,000) and provides dedicated account managers who assist with complex payment '
    'requirements such as property purchases, business acquisitions, and regular supplier payments. The OFX model '
    'is particularly relevant for TradeFlow because African cross-border trade transactions tend to be larger '
    'in value than remittance transactions: a Ghanaian cocoa exporter paying a Dutch shipping company, for '
    'example, may be transferring tens of thousands of dollars and would benefit from personalized guidance '
    'through the process.',
    body_style
))
story.append(Spacer(1, 6))
story.append(Paragraph(
    'OFX differentiates through rate guarantees for large transfers. When a customer contacts OFX for a large '
    'transfer, they receive a personalized rate quote that is typically more favorable than the published online '
    'rate, and this rate is locked for up to 72 hours while the customer arranges the funding. This approach to '
    'dynamic, volume-based pricing is something TradeFlow volume discount feature (implemented in the first '
    'audit cycle) partially addresses, but OFX extends it with human-assisted deal negotiation for very large '
    'transfers. As TradeFlow moves into Phase 2 with invoicing tools, integrating a quote request flow for '
    'transfers above a certain threshold (e.g., above USD 10,000) where users can request a personalized rate '
    'from TradeFlow treasury team would add a premium tier that captures additional margin from high-value '
    'transactions without requiring the infrastructure of a full relationship management team.',
    body_style
))

story.append(add_heading('<b>5.3 WorldRemit</b>', h2_style, 1))
story.append(Paragraph(
    'WorldRemit, founded in London by Ismail Ahmed (a Somali-born entrepreneur who built the company based on his '
    'own experience of the difficulties of sending money to Africa), is arguably the most directly comparable '
    'global platform to TradeFlow in terms of African market focus. The platform specializes in remittances to '
    'developing countries, with Africa representing a significant portion of its transfer volume and revenue. '
    'WorldRemit supports delivery to mobile money wallets, bank accounts, cash pickup locations, and mobile airtime '
    'top-up across most African countries, and its pricing and delivery options are specifically calibrated for '
    'African corridor characteristics. This makes WorldRemit the most important single competitor for TradeFlow '
    'to study, as it has already solved many of the last-mile delivery challenges that TradeFlow Phase 1 only '
    'addresses at the comparison level.',
    body_style
))
story.append(Spacer(1, 6))
story.append(Paragraph(
    'WorldRemit mobile-first strategy for African markets offers critical insights. The platform has invested '
    'heavily in optimizing for low-bandwidth environments, USSD-based interfaces for feature phones, and '
    'offline-capable mobile applications that can queue transactions when connectivity is poor and automatically '
    'submit when the connection is restored. These technical adaptations are essential for reaching users in '
    'African markets where smartphone penetration is growing but connectivity remains inconsistent. TradeFlow '
    'PWA support provides a foundation for offline capability, but specifically optimizing for low-bandwidth '
    'scenarios and developing USSD fallback interfaces would significantly expand the addressable user base. '
    'WorldRemit also partners with local agents for cash pickup and mobile money registration, creating a physical '
    'distribution network that digital-only platforms cannot replicate. As TradeFlow scales, building partnerships '
    'with local financial service agents across African trade hubs would strengthen the platform value proposition '
    'for users who need both digital comparison and physical last-mile delivery.',
    body_style
))

story.append(add_heading('<b>5.4 UK Gap Analysis</b>', h2_style, 1))
story.extend(safe_keep([
    Spacer(1, 10),
    make_table(
        ['Feature', 'Wise UK', 'OFX', 'WorldRemit', 'TradeFlow'],
        [
            ['Cost % Display', 'Yes', 'On request', 'No', 'No'],
            ['Volume Pricing', 'Standard', 'Negotiated', 'Standard', 'Auto-discount'],
            ['Dedicated Account Mgr', 'No', 'Yes (high-value)', 'No', 'Not yet'],
            ['Low-bandwidth Optimized', 'No', 'No', 'Yes (USSD)', 'No'],
            ['Agent Network', 'No', 'No', 'Yes (extensive)', 'Not yet'],
            ['African Corridor Depth', 'Moderate', 'Limited', 'Extensive', 'PAPSS-focused'],
            ['Trust Signals (FSCS etc.)', 'FSCS + FCA', 'FCA', 'FCA', 'Emerging'],
        ],
        [0.22, 0.18, 0.18, 0.20, 0.22]
    ),
    Paragraph('<b>Table 4.</b> United Kingdom Competitive Feature Matrix', caption_style),
]))
story.append(Spacer(1, 18))

# ═══════════════════════════════════════════════════════════════
# CHAPTER 6: Cross-Regional Themes & Patterns
# ═══════════════════════════════════════════════════════════════
story.append(add_heading('<b>6. Cross-Regional Themes and Strategic Patterns</b>', h1_style, 0))

story.append(add_heading('<b>6.1 The Transparency Imperative</b>', h2_style, 1))
story.append(Paragraph(
    'Across all four regions analyzed, the single most consistent competitive pattern is the absolute priority '
    'placed on fee and rate transparency. Every major competitor has converged on displaying the mid-market '
    'rate (or as close to it as their business model allows) and breaking down all costs before requiring user '
    'commitment. Wise pioneered this approach, but it has now become table stakes: Remitly shows all fees '
    'upfront, Revolut displays the rate and fee in the conversion flow, Airwallex provides detailed FX cost '
    'analysis in its treasury dashboard, and even OFX provides clear fee schedules for standard transfers. '
    'TradeFlow Phase 1 already implements this pattern well, but the next level of transparency demonstrated by '
    'leading platforms includes showing the total cost as a percentage of the transfer amount, comparing the '
    'total cost against the user current bank or MTO, and providing historical fee trend data that shows users '
    'whether they are getting a good deal relative to recent averages.',
    body_style
))

story.append(add_heading('<b>6.2 The API-First Transformation</b>', h2_style, 1))
story.append(Paragraph(
    'The second dominant pattern is the shift from consumer-facing comparison tools to API-first infrastructure '
    'platforms. Wise, Airwallex, and Revolut Business all derive a significant and growing portion of their revenue '
    'from API-based integrations that allow other businesses to embed cross-border payment capabilities into '
    'their own products. Wise Platform (the API product) processes billions of dollars annually for partners '
    'ranging from e-commerce platforms to accounting software providers. Airwallex entire business model is '
    'built around embedded finance, and the company has positioned itself as the infrastructure layer that '
    'other fintechs and platforms build upon. This pattern validates TradeFlow planned Phase 3 payment '
    'facilitation API but also suggests that the API should be designed not just as a technical interface but as '
    'a complete developer platform with sandboxes, SDKs, webhooks, interactive documentation, and dedicated '
    'developer support. The window of opportunity for establishing an API platform in the African cross-border '
    'payment space is still open, but it is narrowing as global players like Wise and Airwallex expand their '
    'African corridor coverage.',
    body_style
))

story.append(add_heading('<b>6.3 Mobile as Primary Interface</b>', h2_style, 1))
story.append(Paragraph(
    'The third consistent pattern is the dominance of mobile as the primary user interface for cross-border '
    'payments. In every region analyzed, mobile transaction volumes significantly exceed desktop volumes. In '
    'emerging markets (the segment most relevant to TradeFlow), mobile often accounts for 80-90% of transaction '
    'origin. Remitly reports over 80% mobile transactions. WorldRemit has built its African strategy around '
    'mobile money delivery. Wise has invested heavily in its mobile app experience with biometric authentication '
    'and one-tap repeat transfers. For TradeFlow, this pattern reinforces the importance of PWA support '
    '(already implemented) but also highlights the need to invest in native mobile applications for iOS and '
    'Android that can leverage device-level capabilities like biometric authentication, push notifications, '
    'camera-based document scanning for KYC, and deep OS integration for seamless payment flows. The PWA '
    'foundation is valuable for rapid deployment, but the long-term mobile strategy should target native app '
    'development with offline-first architecture optimized for the connectivity conditions prevalent in African '
    'markets.',
    body_style
))

story.append(add_heading('<b>6.4 Regulatory Licensing as Competitive Moat</b>', h2_style, 1))
story.append(Paragraph(
    'Perhaps the most significant structural finding from this audit is the role of regulatory licensing as a '
    'competitive moat. Wise holds over 50 regulatory licenses globally, Revolut holds over 40, and Airwallex '
    'holds licenses in every major market it operates in. These licenses are not merely compliance checkboxes; '
    'they enable capabilities that unlicensed competitors cannot match: direct access to payment rails, ability to '
    'hold customer funds, issuance of local account details, and most importantly, the trust that comes from '
    'being regulated by reputable financial authorities. For TradeFlow, this finding has profound implications for '
    'the product roadmap. The current Phase 1 model of comparing rates without actually processing payments does '
    'not require regulatory licensing, which is an advantage for rapid market entry. However, as the product '
    'evolves toward Phase 3 (payment facilitation) and Phase 4 (trade marketplace), obtaining regulatory licenses '
    'in key African jurisdictions (starting with Ghana, Nigeria, Kenya, and South Africa) will become essential. '
    'The licensing process should be initiated early in Phase 2 to avoid delays when payment processing capabilities '
    'are needed.',
    body_style
))

story.append(Spacer(1, 18))

# ═══════════════════════════════════════════════════════════════
# CHAPTER 7: Prioritized Recommendations
# ═══════════════════════════════════════════════════════════════
story.append(add_heading('<b>7. Prioritized Recommendations for TradeFlow Roadmap</b>', h1_style, 0))
story.append(Paragraph(
    'Based on the comprehensive analysis across all four regions, the following recommendations are organized by '
    'priority level and mapped to TradeFlow four-phase product strategy. Each recommendation includes the '
    'specific competitor or pattern that inspired it, the expected impact on user acquisition and retention, and '
    'the implementation complexity relative to the current codebase.',
    body_style
))
story.append(Spacer(1, 10))

story.append(add_heading('<b>7.1 Critical Priority (Phase 1 Enhancement)</b>', h2_style, 1))
story.append(Paragraph(
    '<b>Cost Percentage Display:</b> Following Wise UK practice, display the total cost of each payment method '
    'as a percentage of the transfer amount alongside the absolute fee. This enables users to quickly assess value '
    'and provides a shareable metric that drives organic referrals. Implementation is straightforward: calculate '
    'the percentage cost and display it in the comparison results card. This small '
    'UX addition has outsized impact on user confidence and conversion. Estimated effort: 2-4 hours of frontend '
    'development.',
    body_style
))
story.append(Spacer(1, 6))
story.append(Paragraph(
    '<b>Rate Lock Window:</b> Following InstaReM practice, implement a 60-second rate lock after a comparison is '
    'generated. During this window, the displayed rates and fees are guaranteed, giving users confidence to '
    'proceed. If rates change after the window expires, a subtle notification should inform the user that rates '
    'have been refreshed. This feature requires caching the comparison result with a timestamp and comparing '
    'subsequent rate fetches against the cached baseline. Estimated effort: 4-8 hours.',
    body_style
))
story.append(Spacer(1, 6))
story.append(Paragraph(
    '<b>Real Historical Charts:</b> The current 30-day simulated rate history should be replaced with actual '
    'historical rate data from the ExchangeRate-API historical endpoint or a dedicated FX data provider. Wise '
    'provides 1-year historical charts, and even a 90-day real history would significantly increase credibility '
    'over simulated data. Integration with a free historical data source (e.g., Alpha Vantage free tier or '
    'ExchangeRate-API historical endpoint) would provide authentic trend data that businesses can use for '
    'treasury planning. Estimated effort: 6-12 hours including API integration and error handling.',
    body_style
))

story.append(add_heading('<b>7.2 High Priority (Phase 2 Requirements)</b>', h2_style, 1))
story.append(Paragraph(
    '<b>Regulatory License Initiation:</b> Begin the process of obtaining payment institution licenses in Ghana '
    '(Bank of Ghana), Nigeria (CBN), and Kenya (CBK). This is a long-lead-time activity (6-18 months per '
    'jurisdiction) that should start immediately to avoid blocking Phase 3 payment facilitation capabilities. '
    'The cost of licensing varies by jurisdiction but typically ranges from USD 10,000 to USD 100,000 per license '
    'including legal fees. This is the single most important strategic investment for TradeFlow long-term '
    'competitive position, as regulatory licenses create barriers to entry that pure technology plays cannot '
    'replicate.',
    body_style
))
story.append(Spacer(1, 6))
story.append(Paragraph(
    '<b>Automated Rate Alert Execution:</b> Extend the current rate alert notification system to support automated '
    'execution, following CurrencyFair model. When a target rate is hit, the system should notify the user AND '
    'offer a one-click option to execute the transfer at the locked rate. This converts passive rate monitoring into '
    'active payment flow, increasing platform engagement and conversion. The automated execution capability requires '
    'payment processing integration (Phase 3), but the UX framework can be designed in Phase 2.',
    body_style
))
story.append(Spacer(1, 6))
story.append(Paragraph(
    '<b>Low-Bandwidth and Offline Optimization:</b> Following WorldRemit practice for African markets, implement '
    'aggressive caching of rate data and comparison results for offline access, service worker background sync for '
    'queued transactions, and a lightweight version of the comparison tool that loads under 100KB for users on '
    'slow connections. Consider developing a USSD interface for feature phone users who cannot access the web app, '
    'partnering with mobile network operators to provide a star-code-based comparison service.',
    body_style
))

story.append(add_heading('<b>7.3 Medium Priority (Phase 3-4 Considerations)</b>', h2_style, 1))
story.append(Paragraph(
    '<b>Developer Platform:</b> Following Airwallex example, design the Phase 3 API not just as an endpoint but as a '
    'complete developer platform. This includes interactive API documentation (Swagger/OpenAPI), sandbox environment '
    'with test credentials, SDKs for Python and Node.js, webhook infrastructure for payment status notifications, '
    'rate-limit management, and a developer dashboard with usage analytics. The developer experience should be on '
    'par with what Stripe has achieved for payment APIs: clear documentation, responsive support, and tools that '
    'make integration as painless as possible.',
    body_style
))
story.append(Spacer(1, 6))
story.append(Paragraph(
    '<b>Team Management and Approval Workflows:</b> Following Revolut Business model, implement role-based access '
    'controls, multi-level approval workflows for large transfers, spending limits by user and department, and an '
    'audit trail of all payment activities. These features are essential for the B2B segment that TradeFlow '
    'increasingly serves, as businesses typically require multiple stakeholders to authorize cross-border payments '
    'and need detailed records for accounting and compliance purposes.',
    body_style
))
story.append(Spacer(1, 6))
story.append(Paragraph(
    '<b>Agent Network Partnerships:</b> Following WorldRemit physical distribution model, establish partnerships with '
    'local financial service agents in key African trade hubs (Lagos, Accra, Nairobi, Johannesburg, Addis Ababa, '
    'Cairo) to provide cash pickup, mobile money registration assistance, and in-person customer support. These '
    'partnerships extend TradeFlow digital reach into the physical realm, addressing the trust barrier that exists '
    'for users who are unfamiliar with or skeptical of purely digital financial services.',
    body_style
))

# ── Build ──
doc.multiBuild(story, onLaterPages=page_footer, onFirstPage=page_footer)
print(f'Body PDF generated: {OUTPUT}')
