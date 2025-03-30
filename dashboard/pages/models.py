from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def validate_email_list(value):
    emails = value.split(',')
    for email in emails:
        try:
            validate_email(email.strip())
        except ValidationError:
            raise ValidationError(f'Invalid email address: {email}')

class CustomUser(AbstractUser):
    # Override username field to use group_name
    username = models.CharField(max_length=100, unique=True, help_text="Group name")
    # Store member emails as comma-separated values
    member_emails = models.TextField(
        validators=[validate_email_list],
        help_text="Comma-separated list of member email addresses"
    )
    
    
    def __str__(self):
        return self.username  # username is now the group name
    
    def get_member_emails(self):
        """Returns a list of member email addresses"""
        return [email.strip() for email in self.member_emails.split(',')]

