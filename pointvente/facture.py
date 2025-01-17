# import datetime
# import logging, re, os, shutil, sys
# import locale
#
# from reportlab.lib.pagesizes import landscape, letter
# from reportlab.lib import colors
# from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.units import inch, cm
# from reportlab.platypus import SimpleDocTemplate, Image as img, Spacer, Paragraph, Table, TableStyle
# from reportlab.graphics.barcode import code39
# # from invoice.conf import settings
# import importlib
#
#
# Titretyle = ParagraphStyle(
#         name='titre',
#         fontName='Helvetica-Bold',
#         fontSize=8,
#         textColor='DarkGray',
#         borderPadding=(2, 2, 7, 2),
#         borderWidth=0,
#         alignment=TA_CENTER
#     )
#
# Headerstyle = ParagraphStyle(
#         name='headesr',
#         fontName='Helvetica-Bold',
#         fontSize=8,
#         # borderPadding=(2, 2, 7, 2),
#         # borderWidth=0,
#         # borderColor='Gray',
#         alignment=TA_CENTER
#     )
#
#
#
# styles = getSampleStyleSheet()
# styleN = styles["BodyText"]
# styleN.alignment = TA_LEFT
# styleN.fontSize=8
#
# styleNN = styles["BodyText"]
# styleNN.alignment = TA_RIGHT
# styleNN.fontSize=8
#
# styleB = styles["Normal"]
# styleB.alignment = TA_RIGHT
#
# elements = []
#
# header = Table([[Paragraph('TAKE AWAY<br/>LEON HOTEL<br/>41,Luambo Makiadi C/Gombe Kinshasa<br/>RCCM 14-B-2299 ID NAT. N397108<br/>NIF A0705328A Tél:+243 81 219 90 09', style=Titretyle)]])
# elements.append(header)
#
# header = Table([[Paragraph('CDE:0012', style=Headerstyle)]])
# elements.append(header)
#
# header = Table([[Paragraph(f'<u>Date: {datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")} Client:Cash</u>', style=Titretyle)]])
# elements.append(header)
#
# # Items
# data = [['Article', 'Qte', 'Pu', 'Total'], ]
# for item in [1]:
#     data.append([
#
#         Paragraph("totonnvvhgchgccgvchgchgfh", styleN),
#         Paragraph("1", styleN),
#         Paragraph("12",styleNN),
#         Paragraph("120",styleNN)
#     ])
#
# table = Table(data, colWidths=[ 3 * cm,0.8 * cm, 1.5 * cm, 1.5 * cm])
# table.setStyle([
#     ('FONT', (0, 0), (-1, -1), 'Helvetica'),
#     ('FONTSIZE', (0, 0), (-1, -1), 7),
#     ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
#     ('GRID', (0, 0), (-1, 0), 0, (0.7, 0.7, 0.7)),
#     #('GRID', (-2, -1), (-1, -1), 0, (0.7, 0.7, 0.7)),
#     ('ALIGN', (-2, 0), (-1, -1), 'RIGHT'),
#     ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
# ])
# elements.append(table)
#
#
# header = Table([[Paragraph("--------------------------------", style=styleNN)]])
# elements.append(header)
#
# header = Table([[Paragraph("Total CDF {:,.2f}".format(1223), style=styleNN)]])
# elements.append(header)
#
# header = Table([[Paragraph("--------------------------------", style=styleNN)]])
# elements.append(header)
#
# header = Table([[Paragraph("Merci de votre visite. A la prochaine.<br/>Les marchandises vendues ne sont ni Reprises ni echangees", style=Titretyle)]])
# elements.append(header)
#
# barcode=code39.Extended39("1202110021111", barWidth= 0.01 * inch, barHeight= .5 * inch)
# elements.append(barcode)
#
#
#
# # elements.append(Spacer(1, 40))
#
# pagesize = (7.1967 * cm, 29.6686 * cm)
#
# doc = SimpleDocTemplate('output.pdf', pagesize=pagesize,rightMargin=1, leftMargin=1,
#                                 topMargin=1, bottomMargin=1,)
# # doc.build(elements,onFirstPage=drawPageFrame)
# doc.multiBuild(elements)
#
#
#
#
#
# consultant_logo_filename = None
# business_details = (
#     'Scott Stafford',
#     '1212 Mockingbird Lane',
#     'City, ST  11111',
#     '',
#     'Email: scott.stafford@example.com',
# )
#
# note = (
#     'PAYMENT TERMS: 30 DAYS FROM INVOICE DATE.',
#     'Please make all cheques payable to Your Name.',
# )
#
# # locale.setlocale( locale.LC_ALL, '' )
# #
# # def format_currency(value, currency):
# #     return locale.currency(value, grouping=True) #"{0:C0}".format(value)
# #
# # def draw_header(canvas):
# #     """ Draws the invoice header """
# #     canvas.setStrokeColorRGB(176/255., 196/255., 222/255.)
# #     # canvas.setStrokeColorRGB(0.9, 0.5, 0.2)
# #     canvas.setFillColorRGB(0.2, 0.2, 0.2)
# #     canvas.setFont('Helvetica', 16)
# #     canvas.drawString(10 * cm, -1 * cm, 'TAKE AWAY')
# #     if consultant_logo_filename:
# #         canvas.drawInlineImage(consultant_logo_filename, 1 * cm, -1 * cm, 250, 16)
# #     canvas.setLineWidth(4)
# #     canvas.line(0, -1.25 * cm, 21.7 * cm, -1.25 * cm)
# #
# #
# # def draw_address(canvas, text=None):
# #     """ Draws the business address """
# #
# #     canvas.setFont('Helvetica', 9)
# #     textobject = canvas.beginText(13 * cm, -2.5 * cm)
# #
# #     if text is None:
# #         text = business_details
# #
# #     for line in text:
# #         textobject.textLine(line)
# #     canvas.drawText(textobject)
# #
# #
# # def draw_footer(canvas, text=None):
# #     """ Draws the invoice footer """
# #     note = (
# #         'Bank Details: Street address, Town, County, POSTCODE',
# #         'Sort Code: 00-00-00 Account No: 00000000 (Quote invoice number).',
# #         'Please pay via bank transfer or cheque. All payments should be made in CURRENCY.',
# #         'Make cheques payable to Company Name Ltd.',
# #     )
# #     if text is None:
# #         text = note
# #     textobject = canvas.beginText(1 * cm, -27 * cm)
# #     for line in text:
# #         textobject.textLine(line)
# #     canvas.drawText(textobject)
# #
# #
# # # inv_module = importlib.import_module(settings.INV_MODULE)
# # # header_func = inv_module.draw_header
# # # address_func = inv_module.draw_address
# # # footer_func = inv_module.draw_footer
# # header_func = draw_header
# # address_func = draw_address
# # footer_func = draw_footer
# #
# #
# # def draw_pdf(buffer, invoice):
# #     """ Draws the invoice """
# #     pagesize = (7.1967 * cm, 29.6686 * cm)
# #     #canvas = Canvas(buffer, pagesize=A4)
# #     canvas = Canvas(buffer, pagesize=pagesize)
# #
# #     #canvas.setPageSize((204, 841))
# #     canvas.translate(0, 29.7 * cm)
# #     canvas.setFont('Helvetica', 10)
# #
# #     canvas.saveState()
# #     header_func(canvas)
# #     canvas.restoreState()
# #
# #     canvas.saveState()
# #     footer_func(canvas, invoice.footer)
# #     canvas.restoreState()
# #     #
# #     # canvas.saveState()
# #     # address_func(canvas, invoice.address)
# #     # canvas.restoreState()
# #     #
# #     # # Client address
# #     # textobject = canvas.beginText(1.5 * cm, -2.5 * cm)
# #     #
# #     # for line in invoice.client_business_details:
# #     #     textobject.textLine(line)
# #     #
# #     # # if invoice.address.contact_name:
# #     # #     textobject.textLine(invoice.address.contact_name)
# #     # # textobject.textLine(invoice.address.address_one)
# #     # # if invoice.address.address_two:
# #     # #     textobject.textLine(invoice.address.address_two)
# #     # # textobject.textLine(invoice.address.town)
# #     # # if invoice.address.county:
# #     # #     textobject.textLine(invoice.address.county)
# #     # # textobject.textLine(invoice.address.postcode)
# #     # # textobject.textLine(invoice.address.country.name)
# #     # canvas.drawText(textobject)
# #     #
# #     # # Info
# #     # textobject = canvas.beginText(1.5 * cm, -6.75 * cm)
# #     # textobject.textLine('Invoice ID: %s' % invoice.invoice_id)
# #     # textobject.textLine('Invoice Date: %s' % invoice.invoice_date.strftime('%d %b %Y'))
# #     # textobject.textLine('Client: %s' % invoice.client)
# #     #
# #     # #for line in invoice.body_text:
# #     # for line in ["bobo","toto"]:
# #     #     textobject.textLine(line)
# #     #
# #     # canvas.drawText(textobject)
# #
# #     # Items
# #     data = [['Quantity', 'Description', 'Amount', 'Total'], ]
# #     for item in invoice.items:
# #         data.append([
# #             item.quantity,
# #             item.description,
# #             format_currency(item.unit_price, invoice.currency),
# #             format_currency(item.total(), invoice.currency)
# #         ])
# #     data.append(['', '', 'Total:', format_currency(invoice.total(), invoice.currency)])
# #     table = Table(data, colWidths=[2 * cm, 11 * cm, 3 * cm, 3 * cm])
# #     table.setStyle([
# #         ('FONT', (0, 0), (-1, -1), 'Helvetica'),
# #         ('FONTSIZE', (0, 0), (-1, -1), 10),
# #         ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
# #         ('GRID', (0, 0), (-1, -2), 1, (0.7, 0.7, 0.7)),
# #         ('GRID', (-2, -1), (-1, -1), 1, (0.7, 0.7, 0.7)),
# #         ('ALIGN', (-2, 0), (-1, -1), 'RIGHT'),
# #         ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
# #     ])
# #     tw, th, = table.wrapOn(canvas, 15 * cm, 19 * cm)
# #     table.drawOn(canvas, 1 * cm, -10 * cm - th)
# #
# #     canvas.showPage()
# #     canvas.save()
# #
# # class Invoice():
# #     def __init__(self, id, client_business_details, client_name,
# #         invoice_date=datetime.datetime.now(),
# #         currency='USD', body=None, footer=None, address=None):
# #         self.invoice_id = id
# #         self.invoice_date = invoice_date
# #         self.client = client_name
# #         self.currency = currency
# #         self.items = []
# #         self.client_business_details = client_business_details
# #         self.footer = footer
# #         self.body_text = body
# #         self.address = address
# #
# #     def total(self):
# #         return sum([i.total() for i in self.items])
# #
# #     def add_item(self,item):
# #         self.items.append(item)
# #
# #     # def add_item(self, *args, **kwargs):
# #     #     self.items.append(Item(*args, **kwargs))
# #
# #     def save(self, out_filepath):
# #         if out_filepath.lower().endswith('.pdf'):
# #             draw_pdf(out_filepath, self)
# #         else:
# #             raise NotImplementedError("only .pdf")
# #
# #
# # class Item(object):
# #     def __init__(self, name, qty, unit_price, description = ''):
# #         self.name = name
# #         self.description = description
# #         self.quantity = qty
# #         self.unit_price = unit_price
# #
# #     def total(self):
# #         return self.unit_price * self.quantity
# #
# # class Country():
# #     def __init__(self, name):
# #         self.name = name
# #
# #
# # client_business_details = [
# #     'Company One',
# #     'NYC',
# # ]
# #
# # if __name__=='__main__':
# #     invoice = Invoice("VES001", client_business_details, "Company")
# #     #print(type(Item('august hours',50.25,125.0, 'Hours for august')))
# #     invoice.add_item(Item('august hours',50.25,125.0, 'Hours for august'))
# #     draw_pdf('out.pdf', invoice)


from reportlab.graphics.barcode import code39, code128, code93
from reportlab.graphics.barcode import eanbc, qr, usps
from reportlab.graphics.shapes import Drawing
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF


# ----------------------------------------------------------------------
def createBarCodes():
    """
    Create barcode examples and embed in a PDF
    """
    c = canvas.Canvas("barcodes.pdf", pagesize=letter)

    barcode_value = "1234567898888"

    # barcode39 = code39.Extended39(barcode_value)
    # barcode39Std = code39.Standard39(barcode_value, barHeight=20, stop=1)
    #
    # # code93 also has an Extended and MultiWidth version
    # barcode93 = code93.Standard93(barcode_value)
    #
    # barcode128 = code128.Code128(barcode_value)
    # # the multiwidth barcode appears to be broken
    # # barcode128Multi = code128.MultiWidthBarcode(barcode_value)
    #
    # barcode_usps = usps.POSTNET("50158-9999")
    #
    # codes = [barcode39, barcode39Std, barcode93, barcode128, barcode_usps]

    # x = 1 * mm
    # y = 285 * mm
    # x1 = 6.4 * mm
    #
    # for code in codes:
    #     code.drawOn(c, x, y)
    #     y = y - 15 * mm

    # draw the eanbc8 code
    # barcode_eanbc8 = eanbc.Ean8BarcodeWidget(barcode_value)
    # bounds = barcode_eanbc8.getBounds()
    # width = bounds[2] - bounds[0]
    # height = bounds[3] - bounds[1]
    # d = Drawing(50, 10)
    # d.add(barcode_eanbc8)
    # renderPDF.draw(d, c, 15, 555)

    # draw the eanbc13 code

    barcode_eanbc13 = eanbc.Ean13BarcodeWidget(barcode_value)
    bounds = barcode_eanbc13.getBounds()
    #print(dir(barcode_eanbc13.getProperties))
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    d = Drawing(50, 10)
    d.add(barcode_eanbc13)
    renderPDF.draw(d, c, 15, 465)

    # draw a QR code
    # qr_code = qr.QrCodeWidget('www.mousevspython.com')
    # bounds = qr_code.getBounds()
    # width = bounds[2] - bounds[0]
    # height = bounds[3] - bounds[1]
    # d = Drawing(45, 45, transform=[45. / width, 0, 0, 45. / height, 0, 0])
    # d.add(qr_code)
    # renderPDF.draw(d, c, 15, 405)

    c.save()


if __name__ == "__main__":
    createBarCodes()