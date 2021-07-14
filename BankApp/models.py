from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.
class UserDetails(models.Model):
    FirstName=models.CharField(max_length=250)
    LastName=models.CharField(max_length=250)
    FatherName=models.CharField(max_length=250)
    MotherName=models.CharField(max_length=250)
    PhoneNumber=models.CharField(max_length=10,unique=True)
    Email=models.EmailField(unique=True)
    District=models.CharField(max_length=250)
    State=models.CharField(max_length=250)
    moneyAvailable=models.DecimalField(max_digits=10, decimal_places=3,null=True,default=0)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,default=None,null=True)
    def __str__(self):
        return self.FirstName


class Transactions(models.Model):
    UserName=models.CharField(max_length=250)
    ReceiptantName=models.CharField(max_length=250)
    Money=models.DecimalField(max_digits=10, decimal_places=3,null=False)
    Time=models.DateTimeField(default=datetime.now())
    UserId=models.ForeignKey(User,on_delete=models.CASCADE,default=None,null=True)

    def __str__(self):
        return self.UserName + " to "+ self.ReceiptantName
