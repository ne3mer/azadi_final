from django.contrib import admin
from .models import Wallet, WithdrawalRequest
from .views import process_withdrawal_request
from django.urls import reverse
from django.utils.html import format_html


class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')


@admin.register(WithdrawalRequest)
class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'amount', 'is_processed', 'created_at', 'process_withdrawal_link')
    list_filter = ('is_processed',)
    search_fields = ('wallet__user__username',)

    def process_withdrawal_link(self, obj):
        if not obj.is_processed:
            url = reverse('process_withdrawal_request', args=[str(obj.id)])
            return format_html('<a href="{}">Process Withdrawal</a>', url)
        else:
            return "Processed"

    process_withdrawal_link.short_description = 'Process Withdrawal'


admin.site.register(Wallet, WalletAdmin)
