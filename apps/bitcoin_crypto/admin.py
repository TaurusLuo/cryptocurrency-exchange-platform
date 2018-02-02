from django.contrib import admin
from apps.bitcoin_crypto.models import Transaction, ExchangeRate, TransactionPaidUser, TransactionPaidSystem
from apps.authentication.models import Wallet,User

class WalletAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(WalletAdmin, self).get_queryset(request)
        return User.objects.get(username="admin").wallets.all()


# Register your models here.
admin.site.register(ExchangeRate)
admin.site.register(Transaction)
admin.site.register(TransactionPaidSystem)
admin.site.register(TransactionPaidUser)
admin.site.register(Wallet,WalletAdmin)