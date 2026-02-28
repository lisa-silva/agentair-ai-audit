from fpdf import FPDF
import datetime

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "AgentAir AI Visibility Audit", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_pdf(business_name, url, score, recommendations, filename="audit_report.pdf"):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, f"Business: {business_name}", ln=True)
    pdf.cell(0, 10, f"Website: {url}", ln=True)
    pdf.cell(0, 10, f"Audit Date: {datetime.date.today()}", ln=True)
    pdf.ln(10)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"AI Visibility Score: {score}/100", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Recommendations:", ln=True)
    pdf.set_font("Arial", size=11)
    for rec in recommendations:
        pdf.multi_cell(0, 8, f"• {rec}")
    
    pdf.output(filename)
    return filename
