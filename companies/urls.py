from django.urls import path
from companies.views import CompanyListView, CompanyRetrieveView


urlpatterns = [
    path('companies', CompanyListView.as_view()),
    path('companies/<str:name>', CompanyRetrieveView.as_view()),
    # path('companies/search'),
]