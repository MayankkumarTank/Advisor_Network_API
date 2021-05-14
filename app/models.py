from django.db import models
from django.conf import settings
import jwt
from django.utils import timezone
from datetime import datetime

# Create your models here.
class Advisor(models.Model):
    name = models.CharField(max_length=100)
    profile_url = models.URLField(max_length = 2000)

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['name']

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now()
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%S'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

class Booking(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    advisor_id = models.ForeignKey(Advisor,on_delete=models.CASCADE)
    booking_date = models.DateTimeField()