from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Business(models.Model):
    """
        Model for a business account
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=50)
    logo = models.ImageField(default='default.jpg',  
                                     upload_to='business_logos')
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    date_founded = models.DateTimeField(null=True)
