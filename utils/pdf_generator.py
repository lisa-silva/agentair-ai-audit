from fpdf import FPDF
import datetime
import unicodedata
import os

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        # Set better default margins
        self.set_left_margin(15)
        self.set_right_margin(15)
        self.set_top_margin(20)
        self.set_auto_page_break(auto=True, margin=25)
    
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "AgentAir AI Visibility Audit", ln=True, align="C")
        self.ln(15)  # More space after header

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def clean_text(text):
    """Remove or replace characters that cause Unicode errors."""
    if not isinstance(text, str):
        text = str(text)
    # Normalize unicode characters to closest ASCII equivalent
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return text.strip()

def generate_pdf(business_name, url, score, recommendations, filename="audit_report.pdf"):
    pdf = PDF()
    pdf.add_page()
    
    # Clean all text inputs
    clean_business = clean_text(business_name)
    clean_url = clean_text(url)
    
    pdf.set_font("Helvetica", size=12)
    pdf.cell(0, 10, f"Business: {clean_business}", ln=True)
    pdf.cell(0, 10, f"Website: {clean_url}", ln=True)
    pdf.cell(0, 10, f"Audit Date: {datetime.date.today()}", ln=True)
    pdf.ln(10)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, f"AI Visibility Score: {score}/100", ln=True)
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Recommendations:", ln=True)
    pdf.set_font("Helvetica", size=11)
    pdf.ln(2)  # Small gap before recommendations
    
    for rec in recommendations:
        clean_rec = clean_text(rec)
        # Ensure text fits by using multi_cell with full width minus margins
        pdf.multi_cell(0, 8, f"- {clean_rec}")
        pdf.ln(2)  # Space between recommendations
    
    # Save to temp path
    temp_filename = f"/tmp/{clean_text(filename)}"
    pdf.output(temp_filename)
    return temp_filename