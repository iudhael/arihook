import os 

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER_ARIHOOK')  # variable d'environnement email_user
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS_ARIHOOK')

DB_PASS = os.environ.get('DB_PASS')
