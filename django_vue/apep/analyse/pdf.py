from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

class pdf:
    def __init__(self):
        self.directory = os.path.dirname(os.path.dirname(__file__))

    def createPDF(self):
        path_to_pdf_origin = os.path.join(self.directory,"../data",'origin.pdf')
    
        # create a new PDF with Reportlab
        #page 1
        page_1 = io.BytesIO()
        can = canvas.Canvas(page_1, pagesize=letter)
        #Nom entreprise
        can.drawString(318, 685, "Nom entreprise")
        #addresse entreprise
        can.drawString(318, 670, "addresse entreprise")
        #code postal et ville entreprise
        can.drawString(318, 653, "code postal et ville entreprise")
        #
        can.save()

        #move to the beginning of the StringIO buffer
        page_1.seek(0)
        new_pdf = PdfFileReader(page_1)
        # read your existing PDF
        existing_pdf = PdfFileReader(open(path_to_pdf_origin, "rb"))
        output = PdfFileWriter()
        # add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        # finally, write "output" to a real file
        outputStream = open("destination.pdf", "wb")
        output.write(outputStream)
        outputStream.close()

def main():
    pdf().createPDF()

if __name__ == "__main__":
    main()