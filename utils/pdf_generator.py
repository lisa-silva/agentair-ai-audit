from fpdf import FPDF
import datetime

class PDF(FPDF):
    def header(self):
        # Add a Unicode-compatible font (DejaVu is a good choice)
        self.add_font('DejaVu', '', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', uni=True) # Path for Linux/Streamlit Cloud
        self.add_font('DejaVu', 'B', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', uni=True)
        self.set_font('DejaVu', 'B', 16)
        self.cell(0, 10, "AgentAir AI Visibility Audit", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', '', 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_pdf(business_name, url, score, recommendations, filename="audit_report.pdf"):
    pdf = PDF()
    pdf.add_page()

    # Use the Unicode font for all text
    pdf.set_font('DejaVu', '', 12)
    pdf.cell(0, 10, f"Business: {business_name}", ln=True)
    pdf.cell(0, 10, f"Website: {url}", ln=True)
    pdf.cell(0, 10, f"Audit Date: {datetime.date.today()}", ln=True)
    pdf.ln(10)

    pdf.set_font('DejaVu', 'B', 14)
    pdf.cell(0, 10, f"AI Visibility Score: {score}/100", ln=True)
    pdf.ln(5)

    pdf.set_font('DejaVu', 'B', 12)
    pdf.cell(0, 10, "Recommendations:", ln=True)
    pdf.set_font('DejaVu', '', 11)
    for rec in recommendations:
        # Handle any potential special characters in the recommendations
        try:
            pdf.multi_cell(0, 8, f"• {rec}")
        except:
            # If it still fails, try to encode it safely
            safe_rec = rec.encode('ascii', 'replace').decode('ascii')
            pdf.multi_cell(0, 8, f"• {safe_rec}")

    pdf.output(filename)
    return filename