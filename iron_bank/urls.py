
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from iron_bank_app.views import UserCreateView, IndexTemplate, AccountNumberList, AccountCreateView, AccountDetailView, \
    TransactionListView, TransCreateView, OverdraftView, TransferCreateView, TransferListView, TransactionDetailView, \
    TransferDetailView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexTemplate.as_view(), name='index'),
    url(r'^signup', UserCreateView.as_view(), name='signup'),
    url(r'^login', auth_views.login, name='login'),
    url(r'^logout', auth_views.logout_then_login, name='logout'),
    url(r'^accountlist/$', AccountNumberList.as_view(), name='account_number_list'),
    url(r'^createaccount', AccountCreateView.as_view(), name='create_account'),
    url(r'^accountdetail/(?P<pk>\d+)/$', AccountDetailView.as_view(), name="account_detail_view"),
    url(r'^transactions/$', TransactionListView.as_view(), name="trans_list_view"),
    url(r'^transactiondetail/(?P<pk>\d+)/$', TransactionDetailView.as_view(), name="transaction_detail_view"),
    url(r'^createtransaction/(?P<pk>\d+)/$', TransCreateView.as_view(), name="trans_create_view"),
    url(r'^overdraft', OverdraftView.as_view(), name='overdraft_view'),
    url(r'^transfercreate/(?P<pk>\d+)', TransferCreateView.as_view(), name='transfer_view'),
    url(r'^transferlist', TransferListView.as_view(), name='transfer_list'),
    url(r'^transferdetail/(?P<pk>\d+)/$', TransferDetailView.as_view(), name="transfer_detail")
]
