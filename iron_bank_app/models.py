from django.contrib.auth.models import User
from django.db import models

TYPE_CHOICES = [('d', 'deposit'),('w', 'withdraw')]

class AccountNumber(models.Model):
    balance = models.IntegerField()
    user = models.ForeignKey(User)
    nickname = models.CharField(max_length=30)
    created_time = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    account = models.ForeignKey(AccountNumber)
    trans_type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    amount = models.IntegerField()
    description = models.CharField(max_length=50)
    time_created = models.DateTimeField(auto_now_add=True)


class Transfer(models.Model):
    account = models.ForeignKey(AccountNumber)
    amount = models.IntegerField()
    transfer_time = models.DateTimeField(auto_now_add=True)