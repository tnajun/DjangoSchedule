
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from .models import TherapistGoogleCalendar




from django.dispatch import receiver
from allauth.socialaccount.models import SocialLogin, SocialToken
from allauth.account.signals import user_logged_in


@receiver(user_logged_in, sender=SocialLogin)
def save_google_credentials(request, sociallogin, **kwargs):
    """
    Save Google credentials when a user logs in with Google.
    """
    # Ensure the provider is Google
    if sociallogin.account.provider == 'google':
        # Retrieve the token and user
        token = SocialToken.objects.get(account=sociallogin.account, app__provider='google')
        user = sociallogin.user

        # Convert the token to Credentials
        creds = Credentials(
            token=token.token,
            refresh_token=token.token_secret,
            client_id=token.app.client_id,
            client_secret=token.app.secret,
            token_uri='https://accounts.google.com/o/oauth2/token',
        )

        # Use the credentials to retrieve the user's primary Google Calendar ID
        service = build('calendar', 'v3', credentials=creds)
        calendar_list_entry = service.calendarList().get(calendarId='primary').execute()
        calendar_id = calendar_list_entry['id']

        # Save or update the credentials in the database
        TherapistGoogleCalendar.objects.update_or_create(
            user=user,
            defaults={
                'google_calendar_id': calendar_id,
                'google_access_token': creds.token,
                'google_refresh_token': creds.refresh_token,
                'google_token_expiry': creds.expiry,
            }
        )

