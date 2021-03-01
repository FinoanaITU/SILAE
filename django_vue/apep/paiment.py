import stripe
from django.conf import settings

class paiment():
        def __init__(self):
            stripe.api_key = settings.STRIPE_SECRET

        def validerPaiment(self,data):
            try:
                payment = stripe.Charge.create(
                    amount = data['amount']*100,
                    currency = 'eur',
                    description = 'Payement par carte bancaire de la societe ' + data['societeName'],
                    receipt_email = data['receipt_email'],
                    card = data['token'],
                    # card = 'tok_1IOiHmA2z2hXdnDHB6R0zrZU',
                    # metadata={'client': 'DFC'},
                )
                return payment
            except Exception as e:
                print('ato erreur ----------------------')
                print(e)
                return {'errormessage':str(e)}
            