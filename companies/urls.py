from django.urls import path
from companies.views import CompanyListView, CompanyRetrieveView, CompanyAutoCompleteView


urlpatterns = [
    path('companies', CompanyListView.as_view(), name='companies_list'),
    path('companies/<str:name>', CompanyRetrieveView.as_view(), name='companies_retrieve'),
    path('search', CompanyAutoCompleteView.as_view(), name='companies_search'),
]