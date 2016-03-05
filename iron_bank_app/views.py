from datetime import timedelta, date
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, TemplateView, ListView, DetailView
from iron_bank_app.models import AccountNumber, Transaction, Transfer


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
        acct_num = AccountNumber.objects.get(pk=self.kwargs['pk'])
        trans_object.account = acct_num
        if trans_object.amount > 0:
            if trans_object.trans_type == 'd':
                new_balance = acct_num.balance + trans_object.amount
                AccountNumber.objects.filter(user=self.request.user).update(balance=new_balance)
            elif trans_object.trans_type == 'w':
                if trans_object.amount > acct_num.balance:
                    return HttpResponseRedirect('/overdraft')
                else:
                    new_balance = acct_num.balance - trans_object.amount
                    AccountNumber.objects.filter(user=self.request.user).update(balance=new_balance)
        else:
            return HttpResponseRedirect('/overdraft')
        trans_object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("trans_list_view")


class OverdraftView(TemplateView):
    template_name = 'overdraft.html'


class TransactionListView(ListView):
    model = Transaction


class TransactionDetailView(DetailView):
    model = Transaction


class TransferCreateView(CreateView):
    model = Transfer
    fields = ('account', 'amount')

    def form_valid(self, form):
        form_object = form.save(commit=False)
        acct_num_from = AccountNumber.objects.get(pk=self.kwargs['pk'])
        if acct_num_from == AccountNumber:
            new_balance_from = acct_num_from.balance - form_object.amount
            new_balance_to = form_object.account.balance + form_object.amount
            if new_balance_from < 0:
                return HttpResponseRedirect('/overdraft')
            elif new_balance_to < 0:
                return HttpResponseRedirect('/overdraft')
            elif acct_num_from == Transfer.account:
                return HttpResponseRedirect('/overdraft')
            else:
                AccountNumber.objects.filter(pk=self.kwargs['pk']).update(balance=new_balance_from)
                AccountNumber.objects.filter(pk=form_object.account.id).update(balance=new_balance_to)
                form_object.save()
                return super().form_valid(form)
        else:
            return HttpResponseRedirect('/overdraft')

    def get_success_url(self):
        return reverse("account_number_list")


class TransferListView(ListView):
    model = Transfer

    def get_queryset(self):
       return Transfer.objects.filter(account__user=self.request.user)


class TransferDetailView(DetailView):
    model = Transfer
