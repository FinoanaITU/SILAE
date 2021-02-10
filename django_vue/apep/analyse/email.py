from django.core.mail import EmailMessage
import os

class email():
    def __init__(self):
        self.directory = os.path.dirname(os.path.dirname(__file__))

    def sendMail(self):
        text = "Les étoiles vous permettent d'attribuer un statut spécial aux messages afin de faciliter leur recherche. Pour activer le suivi d'un message, cliquez sur l'icône en forme d'étoile à côté d'un message ou d'une conversation"
        lienPdf = os.path.join(self.directory,".\pdfGenerate","A2J_488084005.pdf")
        msg = EmailMessage('apep dsn pdf',text, to=['finoanaandriatsilavoo@gmail.com'])
        msg.attach_file(lienPdf)
        msg.send()
        print('lasa')

def main():
    email.sendMail()

if __name__ == "__main__":
    main()