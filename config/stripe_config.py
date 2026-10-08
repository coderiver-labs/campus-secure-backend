from decouple import config


STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = config("STRIPE_WEBHOOK_SECRET", default="")
