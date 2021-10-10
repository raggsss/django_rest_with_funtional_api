from django.core.validators import MaxValueValidator, RegexValidator
from django.db import models


# Create your models here.
class DUser(models.Model):
    first_name = models.CharField(max_length=100, blank=False,
                                  help_text='A first name of user')
    last_name = models.CharField(max_length=100, blank=False,
                                 help_text='A last name of user')
    address = models.CharField(max_length=600,
                               help_text='Address of the user')

    contact_regex = RegexValidator(regex=r'^\+?1?\d{10,10}$',
                                   message="Phone number must be entered in the format: '9999999999'. "
                                           "Up to 10 digits allowed.")
    contact = models.CharField(validators=[contact_regex], max_length=10, blank=False)  # validators should be a list

    email_id = models.EmailField(max_length=200, blank=False)
    website = models.CharField(max_length=200)
    is_active = models.BooleanField(null=False, default=True)
