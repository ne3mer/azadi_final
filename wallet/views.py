from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import WithdrawalRequestForm
from .models import WithdrawalRequest


@login_required
def request_withdrawal(request):
    wallet = request.user.wallet
    if request.method == 'POST':
        form = WithdrawalRequestForm(request.POST)
        if form.is_valid():
            withdrawal_request = form.save(commit=False)
            withdrawal_request.wallet = wallet
            if withdrawal_request.amount > wallet.balance:
                messages.error(request, "درخواست شما از میزان کیف پول شما بیشتر است")
            else:
                wallet.balance -= withdrawal_request.amount
                wallet.save()
                withdrawal_request.save()
                messages.success(request, "درخواست برداشت شما با موفقیت ثبت شد.")
                return redirect('accounts:user_price')
    else:
        form = WithdrawalRequestForm()

    return render(request, 'wallet/request_withdrawal.html', {'form': form})


@staff_member_required
def process_withdrawal_request(request, request_id):
    withdrawal_request = get_object_or_404(WithdrawalRequest, pk=request_id)
    if not withdrawal_request.is_processed:
        withdrawal_request.is_processed = True
        withdrawal_request.save()
        messages.success(request, f"Withdrawal request {withdrawal_request} processed successfully.")
    else:
        messages.error(request, f"Withdrawal request {withdrawal_request} has already been processed.")

    return redirect('admin:wallet_withdrawalrequest_changelist')
