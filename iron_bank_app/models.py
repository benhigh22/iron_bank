from django.contrib.auth.models import User
from django.db import models

TYPE_CHOICES = [('d', 'deposit'),('w', 'withdrawal')]

class AccountNumber(models.Model):
    balance = models.FloatField()
    user = models.ForeignKey(User)
    nickname = models.CharField(max_length=30)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_time']

class Transaction(models.Model):
    account = models.ForeignKey(AccountNumber)
    trans_type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    amount = models.FloatField()
    description = models.CharField(max_length=50)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time_created']

class Transfer(models.Model):
    account = models.ForeignKey(AccountNumber)
    amount = models.FloatField()
    transfer_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-transfer_time']