import json
from collections import defaultdict

from django.shortcuts import get_list_or_404, get_object_or_404
from django.db import transaction
from django.db.models import Q
from rest_framework import views, status
from rest_framework.response import Response

from companies.models import Company, Language, Tag, CompanyName
from companies.serializers import CompanyNameListSerializers, CompanyNameAutoCompleteSerializers
from companies.utils import *


class CompanyListView(views.APIView):
    def get_list(self, language):
        return get_list_or_404(CompanyName, language=language)

    def get_tag_list(self, data):
        tag_list = []
        for idx, value in enumerate(data):
            tag_list.append(Tag.objects.get(name=value))

        return tag_list

    def get(self, request):
        """
            GET api/companies
            회사 리스트 검색
        """
        # request.headers 'x-wanted-language' 값과 맞는 language object 검색 후 예외처리
        language, language_obj, error, has_error = get_headers_language(request)

        if has_error:
            return error

        companies = self.get_list(language_obj)
        serializer = CompanyNameListSerializers(companies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic(using='default')
    def post(self, request):
        """
            POST api/companies
            새로운 회사 등록
        """
        # request.headers 'x-wanted-language' 값과 맞는 language object 검색 후 예외처리
        language, language_obj, error, has_error = get_headers_language(request)

        if has_error:
            return error

        try:
            # request.body type == json
            if request.META['CONTENT_TYPE'] == 'application/json':
                request = json.loads(request.body)

                # request['tags'] 정보 '언어' - '태그 list' 형태의 dictionary list 변환
                tag_dict = defaultdict(list)
                for data in request['tags']:
                    for key, val in data['tag_name'].items():
                        tag_dict[key].append(val)

                # request에 선언된 언어 중 language에 없는 값이 입력되었을 경우 rollback
                try:
                    with transaction.atomic():
                        # 1. 새로운 company 등록
                        company_id = Company.objects.latest('id').id
                        print('company_id:', company_id)

                        company = Company(id=company_id + 1)
                        company.save()

                        # 2. 새로 생성된 company와 연관된 company_name 정보 등록
                        latest_company = Company.objects.latest('id')
                        for key, val in request['company_name'].items():
                            language = Language.objects.get(name=key)
                            company_name = CompanyName(company=latest_company, language=language, name=val)
                            company_name.save()

                            CompanyName.objects.filter(language=language).latest('company')\
                                .tags.add(*self.get_tag_list(tag_dict[key]))

                        company = CompanyName.objects.filter(company=latest_company, language=language_obj).first()
                        serializer = CompanyNameListSerializers(company)

                        return Response(serializer.data, status=status.HTTP_201_CREATED)

                except Exception as e:
                    return Response({'error message': '지원하지 않는 언어가 입력되었습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error message': '형식에 맞지않는 요청이 입력되었습니다.'}, status=status.HTTP_400_BAD_REQUEST)


class CompanyRetrieveView(views.APIView):
    serializer_class = CompanyNameListSerializers

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


class CompanyAutoCompleteView(views.APIView):
    serializer_class = CompanyNameAutoCompleteSerializers

    def get(self, request):
        """
            GET api/search?query=...
            회사 이름으로 회사 검색
        """

        # request.headers 'x-wanted-language' 값과 맞는 language object 검색 후 예외처리
        language, language_obj, error, has_error = get_headers_language(request)

        if has_error:
            return error

        request_query = request.query_params.get('query', None)
        query = Q(language=language_obj)

        if request_query:
            query &= Q(name__icontains=request_query)

        companies = CompanyName.objects.filter(query)
        serializer = self.serializer_class(companies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
