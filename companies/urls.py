from django.urls import path
from companies.views import CompanyRetrieveView


urlpatterns = [
    # path('companies'),
    path('companies/<str:name>', CompanyRetrieveView.as_view()),
    # path('companies/search'),
]