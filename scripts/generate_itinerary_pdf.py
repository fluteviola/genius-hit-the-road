from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "France_Italy_Travel_Itinerary_English_Updated.pdf"

NAVY = colors.HexColor("#17324D")
BLUE = colors.HexColor("#3F6B8A")
PALE = colors.HexColor("#EAF1F6")
CREAM = colors.HexColor("#F8F5EE")
GOLD = colors.HexColor("#C69C5B")
TEXT = colors.HexColor("#1F2933")
MUTED = colors.HexColor("#5B6770")
LINE = colors.HexColor("#CCD6DD")
WHITE = colors.white

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="TitleCustom", parent=styles["Title"], fontName="Helvetica-Bold",
    fontSize=24, leading=28, textColor=NAVY, spaceAfter=4 * mm,
))
styles.add(ParagraphStyle(
    name="SubTitle", parent=styles["Normal"], fontName="Helvetica",
    fontSize=10, leading=14, textColor=MUTED, spaceAfter=5 * mm,
))
styles.add(ParagraphStyle(
    name="Section", parent=styles["Heading2"], fontName="Helvetica-Bold",
    fontSize=12, leading=15, textColor=NAVY, spaceBefore=3 * mm, spaceAfter=2 * mm,
))
styles.add(ParagraphStyle(
    name="BodySmall", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=7.4, leading=10, textColor=TEXT,
))
styles.add(ParagraphStyle(
    name="BodyTiny", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=6.8, leading=9, textColor=TEXT,
))
styles.add(ParagraphStyle(
    name="CellHead", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=7.2, leading=9, textColor=WHITE,
))
styles.add(ParagraphStyle(
    name="Callout", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=8, leading=11, textColor=NAVY, borderColor=GOLD,
    borderWidth=0.7, borderPadding=7, backColor=CREAM,
))
styles.add(ParagraphStyle(
    name="DayTitle", parent=styles["Heading3"], fontName="Helvetica-Bold",
    fontSize=10.3, leading=13, textColor=NAVY, spaceAfter=1 * mm,
))


def p(text, style="BodySmall"):
    return Paragraph(text, styles[style])


def clean(text):
    return (text.replace("–", "-").replace("—", "-").replace("→", " to ")
                .replace("’", "'").replace("“", '"').replace("”", '"'))


def table(data, widths, header=True, font_size=7.2, row_bgs=True):
    rows = [[p(clean(str(v)), "CellHead" if header and r == 0 else "BodyTiny") for v in row]
            for r, row in enumerate(data)]
    t = Table(rows, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.35, LINE),
    ]
    if header:
        commands.append(("BACKGROUND", (0, 0), (-1, 0), NAVY))
    if row_bgs:
        for idx in range(1 if header else 0, len(rows)):
            commands.append(("BACKGROUND", (0, idx), (-1, idx), PALE if idx % 2 else WHITE))
    t.setStyle(TableStyle(commands))
    return t


class ItineraryDoc(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(
            filename,
            pagesize=A4,
            leftMargin=15 * mm,
            rightMargin=15 * mm,
            topMargin=20 * mm,
            bottomMargin=16 * mm,
            title="France and Italy Travel Itinerary - Final English Version",
            subject="Final tourism itinerary for border entry reference, 23 September to 5 October 2026",
            author="Genius Hit The Road",
        )
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="normal")
        self.addPageTemplates(PageTemplate(id="main", frames=[frame], onPage=self._decorate))

    def _decorate(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(NAVY)
        canvas.rect(0, A4[1] - 12 * mm, A4[0], 12 * mm, fill=1, stroke=0)
        canvas.setFillColor(WHITE)
        canvas.setFont("Helvetica-Bold", 8.5)
        canvas.drawString(15 * mm, A4[1] - 7.5 * mm, "FRANCE + ITALY | FINAL TRAVEL ITINERARY")
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(A4[0] - 15 * mm, A4[1] - 7.5 * mm, "23 September - 5 October 2026")
        canvas.setStrokeColor(LINE)
        canvas.line(15 * mm, 12 * mm, A4[0] - 15 * mm, 12 * mm)
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 7.2)
        canvas.drawString(15 * mm, 8 * mm, "For border entry reference | Booking documents carried separately")
        canvas.drawRightString(A4[0] - 15 * mm, 8 * mm, f"Page {doc.page}")
        canvas.restoreState()


def first_page():
    story = [
        Spacer(1, 3 * mm),
        p("FRANCE + ITALY", "TitleCustom"),
        p("Final English itinerary for border entry | Tourism | Group of 6 adults", "SubTitle"),
    ]
    summary = [
        ["SCHENGEN STAY", "ENTRY", "ROUTE", "EXIT"],
        ["23 Sep - 5 Oct 2026<br/>13 days / 12 nights",
         "Paris Charles de Gaulle Airport (CDG), France",
         "Paris - Nice - Menton - Florence - Capri - Positano - Rome",
         "Rome Fiumicino Airport (FCO), Italy"],
    ]
    story += [table(summary, [39 * mm, 46 * mm, 59 * mm, 36 * mm]), Spacer(1, 3 * mm)]
    story.append(p("The 28 September Nice-Menton-Florence route and the 2 October Capri-Positano-Rome route are final. Personal names, passport data, booking references, storage PINs and QR codes are intentionally omitted.", "Callout"))

    story += [p("1. INTERNATIONAL FLIGHTS", "Section")]
    flights = [
        ["Date", "Flight", "Departure", "Arrival", "Notes"],
        ["23 Sep", "TK197", "Beijing Capital T3<br/>06:45", "Istanbul<br/>12:10", "40 kg checked baggage"],
        ["23 Sep", "TK1829", "Istanbul<br/>19:45", "Paris CDG T1<br/>22:30", "Entry into France"],
        ["5 Oct", "TK1864", "Rome FCO T3<br/>20:00", "Istanbul<br/>23:35", "Exit from Schengen"],
        ["6 Oct", "TK088", "Istanbul<br/>01:40", "Beijing Capital T3<br/>15:35", "40 kg checked baggage"],
    ]
    story += [table(flights, [18 * mm, 18 * mm, 45 * mm, 45 * mm, 54 * mm])]

    story += [p("2. ACCOMMODATION", "Section")]
    hotels = [
        ["Stay", "Hotel and telephone", "Address", "Meals"],
        ["23-26 Sep<br/>3 nights", "Best Western Hotel Le Montparnasse<br/>+33 1 45 44 85 37", "37 Boulevard du Montparnasse, 75006 Paris, France", "Not included"],
        ["26-28 Sep<br/>2 nights", "Le Riviera Collection, BW Signature Collection<br/>+33 4 22 13 50 21", "36 Rue Rossini, 06000 Nice, France", "Breakfast included"],
        ["28-30 Sep<br/>2 nights", "Hotel Bonifacio<br/>+39 055 462 7133", "Via Bonifacio Lupi 21, 50129 Florence, Italy", "Breakfast included"],
        ["30 Sep-2 Oct<br/>2 nights", "Hotel Della Piccola Marina<br/>+39 081 837 9642", "Via Mulo 14-16, 80073 Capri, Italy", "Breakfast included"],
        ["2-5 Oct<br/>3 nights", "Hotel Santa Prisca<br/>+39 06 574 1917", "Largo Manlio Gelsomini 25, 00153 Rome, Italy", "Breakfast included"],
    ]
    story += [table(hotels, [26 * mm, 57 * mm, 66 * mm, 31 * mm])]

    story += [p("3. INTERCITY TRANSPORTATION", "Section")]
    transport = [
        ["Date", "Mode", "Route / time", "Verified status"],
        ["23 Sep", "Reserved car", "Paris CDG to Paris hotel | 23:45", "Booked for 6; EUR 120 payable on site"],
        ["26 Sep", "TGV INOUI 6165", "Paris Gare de Lyon to Nice-Ville | 11:22-17:05", "Ticketed; second class"],
        ["28 Sep", "Reserved car", "Nice to Menton to Florence | morning", "Final plan; 50% deposit paid"],
        ["30 Sep", "Frecciarossa 9409", "Firenze S. M. Novella to Napoli Centrale | 10:48-14:03", "Ticketed; second class"],
        ["30 Sep", "NLG JET", "Napoli Beverello to Capri | 16:30", "Ticketed for 6 + luggage; arrive 20 min early"],
        ["2 Oct", "Positano Jet 2", "Capri to Positano | 11:15", "Ticketed for 6 + 6 XL bags; arrive 30 min early"],
        ["2 Oct", "Reserved car", "Positano to Rome | afternoon", "Confirmed; 50% deposit paid"],
        ["5 Oct", "Reserved car", "Rome hotel to FCO | about 15:30", "Final confirmation pending"],
    ]
    story += [table(transport, [18 * mm, 34 * mm, 71 * mm, 57 * mm])]
    return story


days = [
    ("23 Sep | Wed", "Beijing to Paris", "Depart Beijing Capital Airport T3 on TK197 at 06:45 and arrive in Istanbul at 12:10. Take TK1829 at 19:45 and arrive at Paris CDG T1 at 22:30. After immigration and baggage collection, take the pre-booked vehicle to the hotel and rest.", "Flights; reserved car", "Best Western Le Montparnasse"),
    ("24 Sep | Thu", "Paris", "Breakfast near the hotel (not included). Enter the Louvre at 11:30 with reserved tickets. After lunch, continue to Ile de la Cite and view Notre-Dame from outside. Shakespeare and Company is optional, followed by Le Marais. Reserved dinner at 20:00.", "Metro; taxi; walking", "Best Western Le Montparnasse"),
    ("25 Sep | Fri", "Paris", "Trocadero for Eiffel Tower viewpoints and brunch. Continue to the Arc de Triomphe and Champs-Elysees. Reserved vintage football-shirt shop at 16:00-16:15, then Galeries Lafayette, Printemps or Le Marais. Optional Seine cruise. Reserved Les Ombres dinner at 20:30.", "Metro; taxi; walking", "Best Western Le Montparnasse"),
    ("26 Sep | Sat", "Paris to Nice", "Breakfast near the hotel, check out and transfer to Gare de Lyon. Take TGV INOUI 6165 at 11:22 and arrive at Nice-Ville at 17:05. Walk about 10 minutes to the hotel and check in.", "Taxi; TGV; walking", "Le Riviera Collection"),
    ("27 Sep | Sun", "Nice", "After breakfast, visit Cours Saleya, Place Massena, Avenue Jean Medecin and Vieux Nice. Take the free lift to Castle Hill, then walk along the Promenade des Anglais and see the I Love Nice sign. Reserved Le Galet dinner at 19:00.", "Walking; local transit", "Le Riviera Collection"),
    ("28 Sep | Mon", "Nice to Menton to Florence", "After breakfast, check out and leave Nice by reserved vehicle. Reach Menton in about 40 minutes. Spend 2-3 hours on this route: Plage des Sablettes, yellow stairs, Saint-Michel Basilica, old streets, Tutti Frutti gelato and the viewpoint. Lunch at La Trattoria near the station. Continue about 5 hours to Florence, check in, then reserved T-bone steak dinner at Trattoria Dall'Oste Chianineria at 20:00. Gucci Giardino is optional afterwards (about 200 m walk).", "Reserved car; walking", "Hotel Bonifacio"),
    ("29 Sep | Tue", "Florence", "After breakfast, visit the Cathedral of Santa Maria del Fiore at 11:00, including the dome climb and museum. Enter the Uffizi Gallery at 15:00 with reserved tickets. Continue to Piazzale Michelangelo for sunset.", "Walking; taxi", "Hotel Bonifacio"),
    ("30 Sep | Wed", "Florence to Capri", "Check out and take Frecciarossa 9409 at 10:48, arriving Napoli Centrale at 14:03. Transfer directly to Molo Beverello and board NLG JET at 16:30, arriving at least 20 minutes early. Continue from Marina Grande to the hotel.", "Taxi; train; ferry", "Hotel Della Piccola Marina"),
    ("1 Oct | Thu", "Capri", "Visit the Gardens of Augustus and the Via Krupp viewing area. Continue by open-top taxi to Anacapri and take the Monte Solaro chairlift. The Blue Grotto or a beach club is optional and depends on weather and sea conditions.", "Taxi; chairlift; walking", "Hotel Della Piccola Marina"),
    ("2 Oct | Fri", "Capri to Positano to Rome", "After breakfast, check out and proceed to Marina Grande with all luggage. Board Positano Jet 2 at 11:15; arrive 30 minutes early. Store 6 bags at Via Rampa Teglia 23. Walk via Ceramica Assunta, the Santa Maria Assunta Church direction, Delicatessen fruit shop, the viewpoint at Via Cristoforo Colombo 175 and the fruit stand at SS163.53. Food options: Terrazza Cele, Saraceno d'Oro, Mediterraneo, Posides, Il Fornillo, or Angelo Cafe Dolce Salato. Collect luggage, meet the reserved driver, continue to Rome and check in at Hotel Santa Prisca.", "Ferry; walking; reserved car", "Hotel Santa Prisca"),
    ("3 Oct | Sat", "Rome / Vatican City", "View Castel Sant'Angelo from outside and walk along the Tiber. Visit St. Peter's Square and Basilica in the afternoon, allowing time for security. Enter the Vatican Museums at 17:00 with reserved tickets and visit the galleries and Sistine Chapel.", "Taxi; metro; walking", "Hotel Santa Prisca"),
    ("4 Oct | Sun", "Rome", "Start early for the Colosseum free-entry day, subject to official rules. Continue to Palatine Hill and the Roman Forum. After lunch, visit Piazza Venezia, the Pantheon, Piazza Navona and Trevi Fountain. Spanish Steps are optional. Reserved dinner at 19:45.", "Metro; taxi; walking", "Hotel Santa Prisca"),
    ("5 Oct | Mon", "Rome to Beijing", "Keep activities close to the hotel and collect luggage. Leave by private transfer at about 15:30 and arrive at FCO at about 16:30 for tax refund, check-in, security and exit formalities. Take TK1864 to Istanbul at 20:00.", "Reserved car; flight", "In flight / transit"),
    ("6 Oct | Tue", "Istanbul to Beijing", "Depart Istanbul on TK088 at 01:40 and arrive at Beijing Capital Airport T3 at 15:35. This date is outside the Schengen stay period.", "International flight", "None"),
]


def day_table(subset):
    data = [["Date", "City", "Daily itinerary", "Transport", "Accommodation"]]
    data.extend(subset)
    return table(data, [24 * mm, 28 * mm, 86 * mm, 22 * mm, 30 * mm])


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    story = first_page()
    story += [PageBreak(), p("4. DAILY ITINERARY", "Section"), day_table(days[:7])]
    story += [PageBreak(), p("4. DAILY ITINERARY - CONTINUED", "Section"), day_table(days[7:])]
    story += [Spacer(1, 4 * mm)]
    story.append(p("DOCUMENTS CARRIED", "Section"))
    story.append(p("Passports and valid Schengen visas; return flight tickets; hotel confirmations; rail, ferry and chauffeur bookings."))
    story.append(p("TRAVEL PURPOSE", "Section"))
    story.append(p("Tourism in France, Italy and Vatican City. No employment, study or commercial activity is planned."))
    story.append(p("PRIVACY NOTE", "Section"))
    story.append(p("This summary contains no traveler names, passport numbers, personal contact details, booking references, luggage-storage PINs or QR codes."))
    story.append(Spacer(1, 3 * mm))
    story.append(p("Updated from the final shared itinerary on 19 September 2026. Daily sightseeing may be adjusted for weather, local opening conditions and transportation operations; booked accommodation, ticketed transport and international flights follow the supporting booking documents.", "Callout"))

    doc = ItineraryDoc(str(OUTPUT))
    doc.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    build()
