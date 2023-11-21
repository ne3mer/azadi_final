import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import FloatField, ExpressionWrapper, F
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView
from jalali_date import date2jalali

from shop.models import UserProduct, PriceChange, Product
from utils import send_otp_code
from .forms import UserRegistrationForm, VerifyCodeForm, UserLoginForm, UserEditForm
from .models import OtpCode, User


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(form.cleaned_data['phone_number'], random_code)
            OtpCode.objects.create(
                phone_number=form.cleaned_data['phone_number'], code=random_code)
            request.session['user_registration_info'] = {
                'phone_number': form.cleaned_data['phone_number'],
                'email': form.cleaned_data['email'],
                'name': form.cleaned_data['name'],
                'family': form.cleaned_data['family'],
                'password': form.cleaned_data['password']
            }
            messages.success(request, 'کد تایید برای شما ارسال شد', 'success')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form': form})


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/verify.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(
            phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                User.objects.create_user(user_session['phone_number'], user_session['email'], user_session['name'],
                                         user_session['password'])
                code_instance.delete()
                messages.success(
                    request, 'ثبت نام با موفقیت انجام شد', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'کد وارد شده اشتباه است', 'danger')
                return redirect('accounts:verify_code')
        return render(request)


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, phone_number=cd['phone_number'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'با موفقیت وارد شدید', 'success')
                return redirect('home:home')
            messages.error(
                request, 'شماره موبایل یا رمز عبور اشتباه است', 'danger')
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'با موفقیت خارج شدید', 'info')
        return redirect("home:home")


class UserPriceChangesView(LoginRequiredMixin, ListView):
    model = UserProduct
    template_name = 'accounts/user_price_changes.html'
    context_object_name = 'user_products'

    def get_queryset(self):
        return UserProduct.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_products = context['user_products']

        # Fetch all related price changes and products in a single query
        price_changes_queryset = PriceChange.objects.filter(
            product__userproduct__in=user_products
        ).select_related('product')

        price_changes_dict = {}
        product_price_data = {}
        all_dates = set()
        for price_change in price_changes_queryset:
            product = price_change.product
            if product not in price_changes_dict:
                price_changes_dict[product] = []

            price_changes_dict[product].append(price_change)
            date = price_change.created_at.date()
            all_dates.add(date)
            if product.name not in product_price_data:
                product_price_data[product.name] = []
            product_price_data[product.name].append(
                (date, price_change.new_price))

        # ... (Process the fetched data as before)

        return context
    model = UserProduct
    template_name = 'accounts/user_price_changes.html'
    context_object_name = 'user_products'

    def get_queryset(self):
        return UserProduct.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_products = context['user_products']
        price_changes = []
        sum_benefit = 0
        product_benefit = {}
        product_price_data = {}
        all_dates = set()
        User = get_user_model()
        user = get_object_or_404(User, pk=self.request.user.pk)
        for user_product in user_products:
            product = user_product.product
            product_price_changes = PriceChange.objects.filter(
                product=product).order_by('created_at')
            if product_price_changes:
                price_data = []
                initial_price = product_price_changes.first().new_price
                for price_change in product_price_changes:
                    date = price_change.created_at.date()
                    all_dates.add(date)
                    price_data.append((date, price_change.new_price))
                product_price_data[product.name] = price_data

                first_price = product_price_changes.first().new_price
                benefit = (product_price_changes.last().new_price -
                           user_product.initial_price) * user_product.quantity
                sum_benefit += benefit
                percentage_change = ((
                    product_price_changes.last().new_price - user_product.initial_price) / user_product.initial_price) * 100
                price_changes.append({
                    'product': product,
                    'current_price': product_price_changes.last().new_price,
                    'price_change': product_price_changes.last(),
                    'quantity': user_product.quantity,
                    'benefit': benefit,
                    'percentage_change': percentage_change,
                    'first_price': first_price,
                    'user_product': user_product
                })
                product_benefit[product.name] = {
                    'product': product, 'benefit': benefit}

        context['price_changes'] = price_changes
        context['num_products'] = sum([p['quantity'] for p in price_changes])
        context['sum_benefit'] = sum_benefit
        context['product_benefit'] = product_benefit
        context['wallet'] = user.wallet.balance

        # Prepare data for the line chart
        line_data = []
        for product_name, price_data in product_price_data.items():
            line_data.append({
                'label': product_name,
                'data': [(date.strftime('%Y-%m-%d'), price) for date, price in price_data],
                'fill': False
            })
        line_data = sorted(line_data, key=lambda x: x['label'])

        context['line_data'] = line_data
        context['all_dates'] = sorted(list(all_dates))

        # Prepare data for the bar chart
        bar_data = []
        for user_product in user_products:
            product_name = user_product.product.name
            initial_price = user_product.initial_price
            current_price = PriceChange.objects.filter(
                product=user_product.product).latest('created_at').new_price
            price_change = current_price - initial_price
            bar_data.append({
                'product_name': product_name,
                'initial_price': initial_price,
                'current_price': current_price,
                'price_change': price_change
            })
        bar_data = sorted(bar_data, key=lambda x: x['product_name'])

        context['bar_data'] = bar_data
        return context


class PriceChangesListView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        price_changes = PriceChange.objects.filter(
            product=product).order_by('created_at')

        # Create lists for the chart data
        labels = []
        old_prices = []
        new_prices = []

        # Add data to the lists
        for price_change in price_changes:
            labels.append(date2jalali(
                price_change.created_at).strftime("%Y-%m-%d"))
            old_prices.append(price_change.old_price)
            new_prices.append(price_change.new_price)

        # Calculate the percent change for each price change
        percent_changes = ExpressionWrapper(
            ((F('new_price') - F('old_price')) / F('old_price')) * 100,
            output_field=FloatField()
        )
        price_changes = price_changes.annotate(
            percentage_change=percent_changes)

        context = {
            'product': product,
            'price_changes': price_changes,
            'labels': labels,
            'old_prices': old_prices,
            'new_prices': new_prices,
        }
        return render(request, 'accounts/price_changes_list.html', context)


class UserEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'accounts/edit_user.html'
    success_url = reverse_lazy('home:home')

    def get_object(self, queryset=None):
        return self.request.user
