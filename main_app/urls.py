from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('companies/search/', views.company_search, name='search'),
    path('companies/add/', views.company_add, name='add_company'),
    path('companies/<str:ticker>/', views.company_detail, name='detail'),
    path('mystocks/', views.my_stocks, name='my_stocks'),
    path('user/performance/add/', views.add_performance, name='add_performance'),
]