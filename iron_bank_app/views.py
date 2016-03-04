from datetime import timedelta, date
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render

from django.views.generic import CreateView, TemplateView, ListView, DetailView

from iron_bank_app.models import AccountNumber, Transaction


class LimitedAccessMixin:

   def get_queryset(self):
       return AccountNumber.objects.filter(user=self.request.user)


class IndexTemplate(TemplateView):
    template_name = 'index.html'


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse("login")


class AccountCreateView(CreateView):
    model = AccountNumber
    fields = ('nickname', 'balance')

    def form_valid(self, form):
        acct_object = form.save(commit=False)
        acct_object.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("account_number_list")


class AccountNumberList(LimitedAccessMixin, ListView):
    model = AccountNumber


class AccountDetailView(LimitedAccessMixin, DetailView):
    model = AccountNumber


class TransCreateView(CreateView):
    model = Transaction
    fields = ('trans_type', 'amount', 'description')

    def form_valid(self, form):
        trans_object = form.save(commit=False)
        acct_num = AccountNumber.objects.get(user=self.request.user)
        trans_object.account = acct_num
        if trans_object.trans_type == 'd':
            new_balance = acct_num.balance + trans_object.amount
            AccountNumber.objects.filter(user=self.request.user).update(balance=new_balance)
        elif trans_object.trans_type == 'w':
            if trans_object.amount > acct_num.balance:
                return "Insufficient Funds"
            else:
                new_balance = acct_num.balance - trans_object.amount
                AccountNumber.objects.filter(user=self.request.user).update(balance=new_balance)
        trans_object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("trans_list_view")


class TransactionListView(ListView):
    model = Transaction

    """def get_queryset(self):
        startdate = date.today()
        enddate = startdate + timedelta(days=30)
        return Transaction.objects.filter(date__range=[startdate, enddate])"""