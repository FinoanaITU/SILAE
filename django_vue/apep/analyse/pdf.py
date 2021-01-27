from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
import os
import datetime
class pdf:
    def __init__(self):
        self.directory = os.path.dirname(os.path.dirname(__file__))

    def createPDF(self, data):
        path_to_pdf_origin = os.path.join(self.directory,".\data",'originVide.pdf')
        # create a new PDF with Reportlab
        page_1 = self.createPage1(data)
        pageTA = self.createPageTA(data)

        # read your existing PDF
        existing_pdf = PdfFileReader(open(path_to_pdf_origin, "rb"))
        output = PdfFileWriter()
        # add the "watermark" (which is the new pdf) on the existing page

        # #page 1
        # page = existing_pdf.getPage(0)
        # page.mergePage(page_1.getPage(0))
        # output.addPage(page)

        #page TA
        page = existing_pdf.getPage(1)
        page.mergePage(pageTA.getPage(0))
        output.addPage(page)

        # finally, write "output" to a real file
        outputStream = open("destination2.pdf", "wb")
        output.write(outputStream)
        outputStream.close()

    def createPage1(self,data):
        page_1 = io.BytesIO()
        can = canvas.Canvas(page_1, pagesize=letter)
        #Nom entreprise
        can.drawString(318, 685, data["nom"])
        #addresse entreprise
        can.drawString(318, 670, data["address"])
        #code postal et ville entreprise
        can.drawString(318, 653, data["codePostal"]+' '+data["ville"])
        #anne en cours
        can.setFont('Helvetica-Bold', 10)
        # can.setFontSize(10)
        nowDate = datetime.datetime.now()
        can.drawString(417,538,str(nowDate.year))

        #Taxe d'apprentissage
        can.drawString(363,518, str(data["tA_68"])+' €')
        #ecole
        can.drawString(120,483,'ecole citée')
        #contribution
        can.drawString(332,458, str(data["totalContribution"])+' €')
        #nom OPCO
        can.drawString(120,414, "OPCO")
        can.save()

        #move to the beginning of the StringIO buffer
        page_1.seek(0)
        new_pdf = PdfFileReader(page_1)
        return new_pdf

    def createPageTA(self, data):
        page = io.BytesIO()
        can = canvas.Canvas(page, pagesize=letter)
        #Nom entreprise
        can.drawString(40, 685, data["nom"])
        #addresse entreprise
        can.drawString(40, 670, data["address"])
        #code postal et ville entreprise
        can.drawString(40, 653, data["codePostal"]+' '+data["ville"])
        #anne en cours
        can.setFont('Helvetica-Bold', 10)
        # can.setFontSize(10)
        nowDate = datetime.datetime.now()
        can.drawString(417,538,str(nowDate.year))

        #Masse salariale TA
        can.setFont('Helvetica', 13)
        can.drawString(180,515, str(data["masse_salariale"])+' €')
        #0.68%
        can.setFont('Helvetica', 13)
        can.drawString(180,496, str(data["tA_68"])+' €')
        #solde ecole de 13%
        can.setFont('Helvetica', 13)
        can.drawString(180,474, str(data["solde_ecole"])+' €')
        #Montant versement
        can.setFont('Helvetica', 19)
        can.drawString(210,400, str(data["solde_ecole"])+' €')
        #nom ecole
        can.setFont('Helvetica-Bold', 12)
        can.drawString(124, 378, "NOM DE L'ECOLE ")
        can.save()

        #move to the beginning of the StringIO buffer
        page.seek(0)
        new_pdf = PdfFileReader(page)
        return new_pdf

def main():
    pdf().createPDF()

if __name__ == "__main__":
    main()