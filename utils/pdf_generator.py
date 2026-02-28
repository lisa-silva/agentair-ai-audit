from fpdf import FPDF
import datetime
import unicodedata
import os

class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "AgentAir AI Visibility Audit", ln=True, align="C")
        self.ln(10)

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
    # Replace any remaining problematic characters
    return text

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
    
    for rec in recommendations:
        clean_rec = clean_text(rec)
        pdf.multi_cell(0, 8, f"• {clean_rec}")
    
    # Save to a temporary path that Streamlit can read
    temp_filename = f"/tmp/{clean_text(filename)}"
    pdf.output(temp_filename)
    return temp_filename