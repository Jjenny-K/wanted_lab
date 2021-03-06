import json
from collections import defaultdict

from django.shortcuts import get_list_or_404, get_object_or_404
from django.db import transaction
from django.db.models import Q
from rest_framework import views, status
from rest_framework.response import Response

from companies.models import Company, Language, CompanyName
from companies.serializers import CompanyNameListSerializers, CompanyNameAutoCompleteSerializers
from companies.utils import get_headers_language, get_tag_list


class CompanyListView(views.APIView):
    def get_list(self, language):
        return get_list_or_404(CompanyName, language=language)

    def get(self, request):
        """
            GET api/companies
            회사 리스트 검색
        """
        # request.headers 'x-wanted-language' 값과 맞는 language object 검색 후 예외처리
        language_header, error = get_headers_language(request)

        if language_header is None:
            return error

        companies = self.get_list(language_header)
        serializer = CompanyNameListSerializers(companies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
            POST api/companies
            새로운 회사 등록
        """
        # request.headers 'x-wanted-language' 값과 맞는 language object 검색 후 예외처리
        language_header, error = get_headers_language(request)

        if language_header is None:
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
                        latest_company = Company.objects.latest('id')
                        Company(id=latest_company.id + 1).save()

                        # 2. 새로 생성된 company와 연관된 company_name 정보 등록
                        latest_company = Company.objects.latest('id')
                        for key, val in request['company_name'].items():
                            language = Language.objects.get(name=key)
                            CompanyName(company=latest_company, language=language, name=val).save()

                            CompanyName.objects.filter(language=language).latest('company') \
                                .tags.add(*get_tag_list(tag_dict[key]))

                    # 3. 저장된 company 정보 중 header에 입력된 언어에 해당하는 정보 반환
                    result_company = CompanyName.objects\
                        .filter(company=latest_company, language=language_header).first()
                    serializer = CompanyNameListSerializers(result_company)

                    return Response(serializer.data, status=status.HTTP_201_CREATED)

                except Exception as e:
                    return Response({'error message': '지원하지 않는 언어가 입력되었습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error message': '%s, 형식에 맞지않는 요청이 입력되었습니다.' % e}, status=status.HTTP_400_BAD_REQUEST)


class CompanyRetrieveView(views.APIView):
    serializer_class = CompanyNameListSerializers

    def get_object(self, name):
        return get_object_or_404(CompanyName, name=name)

    def get(self, request, name):
        """
            GET api/companies/<str:name>
            회사 이름으로 회사 검색
        """

        # request.headers 'x-wanted-language' 값과 맞는 language object 검색 후 예외처리
        language_header, error = get_headers_language(request)

        if language_header is None:
            return error

        # name 값과 맞는 company name object 검색 후 없다면 404 error 반환
        company = self.get_object(name)

        # request.headers로 넘어온 언어에 맞는 company 검색
        company_obj = company.company
        search_company = CompanyName.objects.filter(company=company_obj, language=language_header).first()
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
        language_header, error = get_headers_language(request)

        if language_header is None:
            return error

        request_query = request.query_params.get('query', None)
        query = Q(language=language_header)

        if request_query:
            query &= Q(name__icontains=request_query)

        companies = CompanyName.objects.filter(query)
        serializer = self.serializer_class(companies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
