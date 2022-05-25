from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import views, status
from rest_framework.response import Response

from companies.models import CompanyName
from companies.serializers import CompanyNameSerializers
from companies.utils import *


class CompanyRetrieveView(views.APIView):
    serializer_class = CompanyNameSerializers

    def get_object(self, name):
        return get_object_or_404(CompanyName, name=name)

    def get(self, request, name):
        """
            api/companies/<str:name>
            회사 이름으로 회사 검색
        """

        # request.headers 'x-wanted-language' 값과 맞는 language object 검색 후 예외처리
        language, language_obj, error, has_error = get_headers_language(request)

        if has_error:
            return error

        # name 값과 맞는 company name object 검색 후 없다면 404 error 반환
        company = self.get_object(name)

        # request.headers로 넘어온 언어에 맞는 company 검색
        company_obj = company.company
        search_company = CompanyName.objects.filter(company=company_obj, language=language_obj).first()
        serializer = self.serializer_class(search_company)

        return Response(serializer.data, status=status.HTTP_200_OK)
