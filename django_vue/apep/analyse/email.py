from django.core.mail import EmailMessage
import os

class email():
    def __init__(self):
        self.directory = os.path.dirname(os.path.dirname(__file__))

    def sendMail(self,data):
        text = "Borderaux taxe d'apprentissage et OPCO "+ data['nomSociete']+'_'+data['siren']+data['siret']
        # lienPdf = os.path.join(self.directory,".\pdfGenerate","A2J_488084005.pdf")
        docName = str(data["nomSociete"]+'_'+data["siren"]).replace("'",'').replace(" ","")
        lienPdf = "/home/SDABOU/SILAE/django_vue/apep/pdfGenerate/"+docName+".pdf"
        msg = EmailMessage('Borderaux',text, to=[data['email']])
        msg.attach_file(lienPdf)
        msg.send()
        return 'lasa'