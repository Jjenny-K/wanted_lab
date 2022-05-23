from django.contrib import admin
from companies.models import Company, Tag, Language, CompanyKeyVal, TagKeyVal

admin.site.register([Company, Tag, Language, CompanyKeyVal, TagKeyVal])
