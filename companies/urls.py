from django.urls import path
from companies.views import CompanyListView, CompanyRetrieveView, CompanyAutoCompleteView


urlpatterns = [
    path('companies', CompanyListView.as_view()),
    path('companies/<str:name>', CompanyRetrieveView.as_view()),
    path('search', CompanyAutoCompleteView.as_view()),
]