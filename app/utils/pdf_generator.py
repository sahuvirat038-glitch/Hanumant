from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
from app.models.invoices import Invoices

def generate_invoice_pdf(invoice: Invoices) -> str:
    # create invoices folder if it doesn't exist
    os.makedirs("invoices", exist_ok=True)

    file_path = f"invoices/{invoice.invoice_number}.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # title
    elements.append(Paragraph("INVOICE", styles["Title"]))
    elements.append(Spacer(1, 20))

    # invoice details
    details = [
        ["Invoice Number", str(invoice.invoice_number)],
        ["Order ID", str(invoice.order_id)],
        ["Date", str(invoice.created_at.strftime("%Y-%m-%d"))],
    ]
    details_table = Table(details, colWidths=[200, 300])
    details_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.grey),
    ]))
    elements.append(details_table)
    elements.append(Spacer(1, 30))

    # amounts
    amounts = [
        ["", ""],
        ["Subtotal", f"Rs. {invoice.subtotal}"],
        ["GST", f"Rs. {invoice.gst_amount}"],
        ["Total", f"Rs. {invoice.total}"],
    ]
    amounts_table = Table(amounts, colWidths=[400, 100])
    amounts_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LINEABOVE", (0, 3), (-1, 3), 1, colors.black),
        ("FONTNAME", (0, 3), (-1, 3), "Helvetica-Bold"),
        ("TEXTCOLOR", (0, 1), (0, -1), colors.grey),
    ]))
    elements.append(amounts_table)

    doc.build(elements)
    return file_path