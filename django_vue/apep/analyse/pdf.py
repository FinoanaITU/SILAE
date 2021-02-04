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
        #locals
        # path_to_pdf_origin = os.path.join(self.directory,".\data",'OriginVide3_1.pdf')
        #prod
        path_to_pdf_origin = os.path.join(self.directory,"./data",'OriginVide3_1.pdf')
        # create a new PDF with Reportlab
        page_1 = self.createPage1(data)
        pageTA = self.createPageTA(data)
        pageOPCO = self.createOPCO(data)
        # read your existing PDF
        existing_pdf = PdfFileReader(open(path_to_pdf_origin, "rb"))
        output = PdfFileWriter()
        # add the "watermark" (which is the new pdf) on the existing page

        #page 1
        page = existing_pdf.getPage(0)
        page.mergePage(page_1.getPage(0))
        output.addPage(page)

        #page TA
        page = existing_pdf.getPage(1)
        page.mergePage(pageTA.getPage(0))
        output.addPage(page)

        #page OPCO
        page = existing_pdf.getPage(2)
        page.mergePage(pageOPCO.getPage(0))
        output.addPage(page)

        # finally, write "output" to a real file
        docName = str(data["nom"]+'_'+data["siren"]).replace("'",'').replace(" ","")
        # outputStream = open('apep/pdfGenerate/'+docName+".pdf", "wb")
        outputStream = open('/home/SDABOU/SILAE/django_vue/apep/pdfGenerate/'+docName+".pdf", "wb")
        output.write(outputStream)
        outputStream.close()
        # lienPdf = os.path.join(self.directory,".\pdfGenerate",docName+".pdf")
        #lien prod
        lienPdf = 'http://sdabou.pythonanywhere.com/pdf/'+docName+".pdf"
        # return os.path.join(self.directory,".\pdfGenerate",docName+".pdf")
        return lienPdf

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
        can.drawString(363,518, str(data["solde_ecole"])+' €')
        #ecole
        can.drawString(120,483,'APEP SUP')
        #contribution
        can.drawString(332,458, str(data["totalContribution"])+' €')
        #nom OPCO
        opcoAddress = data['addressOPCO'].split(';')
        infoOPCO = str('OPCO '+data['nomOPCO']+', '+opcoAddress[0]+' ,'+opcoAddress[1])
        addressPlus = opcoAddress[2] if len(opcoAddress)>2 else ''
        can.drawString(120,414, infoOPCO+' '+addressPlus)
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
        # can.setFontSize(10)
        can.setFont('Helvetica-Bold', 17)
        nowDate = datetime.datetime.now()
        can.drawString(472,800,str(nowDate.year))

        #siren/siret
        can.setFont('Helvetica', 13)
        can.drawString(100, 608, data["siren"]+' '+data["siret"])

        #info beneficiaire
        can.setFont('Helvetica', 13)
        can.drawString(318, 685, 'APEP SUP')
        can.drawString(318, 672, '7 RUE DE LA VEGA')
        can.drawString(318, 660, '75012 PARIS')
        can.setFont('Helvetica', 12)
        can.drawString(318, 640, 'Au service des entreprises et des apprenants')

        #code UAI
        can.setFont('Helvetica', 13)
        can.drawString(472, 395, '0755775V')

        #Masse salariale TA
        can.setFont('Helvetica', 13)
        can.drawString(180,515, str(data["masse_salariale"])+' €')
        #0.68%
        can.setFont('Helvetica', 13)
        can.drawString(180,496, str(data["tA_68"])+' €')
        #solde ecole de 13%
        can.setFont('Helvetica', 13)
        can.drawString(180,470, str(data["solde_ecole"])+' €')
        #Montant versement
        can.setFont('Helvetica', 19)
        can.drawString(210,395, str(data["solde_ecole"])+' €')
        #nom ecole
        can.setFont('Helvetica-Bold', 12)
        can.drawString(124, 373, "APEP SUP ")
        
        #IBAN
        can.setFont('Helvetica-Bold', 10)
        can.drawString(180, 265, data['iban'])

        can.save()
        #move to the beginning of the StringIO buffer
        page.seek(0)
        new_pdf = PdfFileReader(page)
        return new_pdf

    def createOPCO(self,data):
        page = io.BytesIO()
        can = canvas.Canvas(page, pagesize=letter)
        # 
        # nom
        can.drawString(32, 695, data["nom"])
        # address
        can.drawString(32, 680, data["address"])
        # rue? - ex : Paris 20e Arrondissement
        # can.drawString(32, 665, 'Paris 20e Arrondissement')
        # codePostal
        can.drawString(32, 665, data["codePostal"]+' '+data["ville"])
        
        can.setFont('Helvetica', 10)
        opcoAddress = data['addressOPCO'].split(';')
        addressPlus = opcoAddress[2] if len(opcoAddress)>2 else ''
        #date limite versement
        can.drawString(307, 779, '28/02/2021')
        # nom_organisme
        can.drawString(307, 710, 'OPCO')
        # activite_organisme? - ex : SERVICE COLLECTE - TSA 49876
        can.drawString(307, 691, data['nomOPCO'])
        # adresse_organisme
        can.drawString(307, 671, opcoAddress[0])
        # codePostal_organisme
        can.drawString(307, 650, opcoAddress[1])
        # ville_organisme? - ex : MEUDON CEDEX
        can.drawString(400, 650, addressPlus)

        # siren
        can.drawString(92, 631, data["siren"])
        # siret
        can.drawString(160, 631, data["siret"])
        # codeNAF
        can.drawString(295, 631, data["codeNAF"])
        # convention - ex :
        can.drawString(450, 631, data['convention'])
        # activite_principale - ex : Transports collectifs de voyageurs
        can.drawString(120, 614, data['activite'])
        # effectif_annuel_moyen - ex : 35
        can.drawString(135, 598, data['nbrSalarie'])
        # effectif_annuel_moyen_CDD
        # can.drawString(365, 598, '16')
        # a_f_s = annee_franchissement_seuil
        # can.drawString(185, 581, '{{a_f_s}}')
        # a_c = annee_creation
        # can.drawString(325, 581, '{{a_c}}')
        # tva
        can.drawString(475, 581, data["tva"].upper())
        
        #formation continue
        # can.setFont('Helvetica', 10)
        # can.drawString(490, 548, str(data['masse_salariale'])+ ' €')
        #masse salariale taxe apprentissage
        # can.setFont('Helvetica', 10)
        # can.drawString(485, 528, str(data['masse_salariale'])+ ' €')
        #Alsace moselle
        # can.setFont('Helvetica', 10)
        # can.drawString(500, 508, '0 €')

        #masse cdd 
        if 'masseCDD' in data:
            can.drawString(32, 466, 'Masse salarieale CDD:')
            can.drawString(485, 466, str(data['masseCDD'])+ ' €')
        else:
            can.drawString(500, 360, '0 €')
        #lister la contribution
        valueurAcompte = 0
        compteurAutre = 20
        for contribution in data['listeContribution']:
            if contribution['nom_contribution'] == 'Contribution legale':
                #formation continue
                can.drawString(32, 548, 'Formation Continue')
                can.drawString(320, 548, str(data['masse_salariale']))
                can.drawString(365, 548, 'x')
                can.drawString(380, 548, str(contribution['pourcentage'])+' %')
                can.drawString(485, 548, str(contribution['valeur'])+ ' €')
                valueurAcompte = str(contribution['valeur'])

            elif contribution['nom_contribution'] == 'Votre Contribution CPF-CDD':
                can.drawString(32, 446, 'Votre Contribution CPF-CDD')
                can.drawString(320, 446, str(data['masseCDD']))
                can.drawString(365, 446, 'x')
                can.drawString(380, 446, str(contribution['pourcentage'])+' %')
                can.drawString(485, 446, str(contribution['valeur'])+ ' €')

            elif contribution['nom_contribution'] == '1er ACOMPTE CUFPA':
                can.drawString(32, 526, contribution['nom_contribution']+' à payer avant le 28/02/2021')
                can.drawString(320, 526, str(valueurAcompte))
                can.drawString(365, 526, 'x')
                can.drawString(380, 526, str(contribution['pourcentage'])+' %')
                can.drawString(485, 526, str(contribution['valeur'])+ ' €')

            elif contribution['nom_contribution'] == '2er ACOMPTE CUFPA':
                can.drawString(32, 230, contribution['nom_contribution']+'(HT) à payer avant le 15/09/2021')
                can.drawString(320, 230, str(valueurAcompte))
                can.drawString(365, 230, 'x')
                can.drawString(380, 230, str(contribution['pourcentage'])+ ' %')
                can.drawString(485, 230, str(contribution['valeur'])+ ' €')
            
            #autre contribution    
            else:
                if contribution['nom_contribution'] != 'TVA':
                    print(compteurAutre)
                    can.drawString(32, 406 - compteurAutre , contribution['nom_contribution'])
                    can.drawString(320, 406 - compteurAutre, str(data['masse_salariale']))
                    can.drawString(365, 406 - compteurAutre, 'x')
                    can.drawString(380, 406 - compteurAutre, str(contribution['pourcentage']))
                    can.drawString(485, 406 - compteurAutre, str(contribution['valeur'])+ ' €')
                    compteurAutre = compteurAutre + 20 
            #TVA
            if data['tva'] == 'oui' and contribution['nom_contribution'] == 'TVA' :
                can.drawString(32, 506, "TVA applicable")
                can.drawString(485, 506, str(contribution['valeur'])+ ' €')
            
        #-------------------------------
        #TAXE d'apprentissage
        can.setFont('Helvetica', 10)
        can.drawString(32, 406, "Taxe d'apprentissage") 
        can.drawString(260, 406, str(valueurAcompte))
        can.drawString(310, 406, 'x')
        can.drawString(320, 406, '0.68%')
        can.drawString(365, 406, 'x')
        can.drawString(380, 406, '87%')
        # ta87 = str(data['tA_68']).replace(' ','')
        can.drawString(485, 406, str(data['opco87']) +'€')

        #deja verser
        can.drawString(485, 190, '0 €')
        #formule calcule
        can.setFont('Helvetica-Bold', 10)
        can.drawString(32, 150, 'Formule calcule:')
        can.drawString(132, 150, "1er ACOMPTE + TVA + Contribution CPF-CDD + Taxe d'apprentissage")
        #ordre opco
        can.drawString(135, 113, 'OPCO '+data['nomOPCO'])
        #totale
        can.setFont('Helvetica-Bold', 13)
        can.drawString(485, 113, data['totalContribution']+' €')

        can.save()
        page.seek(0)
        new_pdf = PdfFileReader(page)
        return new_pdf

def main():
    pdf().createPDF()

if __name__ == "__main__":
    main()