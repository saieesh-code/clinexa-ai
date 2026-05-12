from fpdf import FPDF

def create_pdf(summary, notes, priority):

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=14)

    pdf.cell(200, 10, txt="Medical AI Report", ln=True)

    pdf.ln(10)

    pdf.set_font("Arial", size=12)

    pdf.multi_cell(0, 10, f"Priority Level: {priority}")

    pdf.ln(5)

    pdf.multi_cell(0, 10, f"AI Summary:\n{summary}")

    pdf.ln(5)

    pdf.multi_cell(0, 10, f"Doctor Notes:\n{notes}")

    output_path = "medical_summary.pdf"

    pdf.output(output_path)

    return output_path