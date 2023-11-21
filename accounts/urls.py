from django.urls import path

from . import views
from .views import UserEditView

app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('verify/', views.UserRegisterVerifyCodeView.as_view(), name='verify_code'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('UserPriceChanges/', views.UserPriceChangesView.as_view(), name='user_price'),
    path('changes/<slug:slug>/', views.PriceChangesListView.as_view(), name='price_change'),
    path('edit-user/', UserEditView.as_view(), name='edit_user'),

]
