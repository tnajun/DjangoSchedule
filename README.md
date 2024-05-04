

# README
A friend wanted to use the reservation system, so this is a portion of our counseling reservation service currently under development. It can be used for both commercial and personal purposes. However, if you make any modifications, please submit a pull request.

## Setup Instructions
Install the necessary dependencies:

```
pip install -r requirements.txt
```
Create a local_settings.py file with the following configuration:

python
Copy code
```
# Configuration for sending emails through Gmail

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'your@gmail.com'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = 'your@gmail.com'

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'  # or 'email'
# ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_REQUIRED = True
LOGIN_REDIRECT_URL = 'accounts:userlist'
ACCOUNT_LOGOUT_REDIRECT_URL = 'account_login'
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
ACCOUNT_UNIQUE_EMAIL = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # or 'django.core.mail.backends.console.EmailBackend'
# Email address verification is mandatory
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
```

Run the following Django management commands:

```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Note: The pip freeze > requirements.txt was used to generate the dependencies file. If you encounter any dependency errors during installation, please make the necessary adjustments.

## Usage:

To properly understand the service operation, ensure that there are at least two users, one counselor and one general user. After registering, users will receive a verification email which they need to click to verify their account.

## Under Development:

/schedule/edit_schedule/
This page allows counselors to change their schedules but the link is not yet connected.

## Areas Needing Revision:

/accounts/userlist/
The slide for page navigation does not function correctly when there are more than ten counselors. JavaScript improvements are needed for efficient page transitions within each category.
The home page should be easily editable through flat pages or similar methods.
The entire application should be editable for international use. Please rewrite all content in English and adjust the scheduling to not be fixed to Japan Standard Time (JST), making it usable worldwide.






