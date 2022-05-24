from django.contrib import admin
from companies.models import Company, Tag, Language, CompanyName

admin.site.register([Company, Tag, Language, CompanyName])
