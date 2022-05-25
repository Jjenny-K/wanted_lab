from rest_framework import status
from rest_framework.response import Response

from companies.models import Language, Tag


def get_headers_language(request):
    """ request headers 'x-wanted-language' 예외 처리 """
    language_header = error = None
    has_error = False

    try:
        language = request.headers['x-wanted-language'].lower()

        try:
            language_header = Language.objects.get(name=language)
        except Exception as e:
            has_error = True
            error = Response({'error message': '지원하지 않는 언어입니다.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        has_error = True
        error = Response({'error message': '검색할 언어를 체크하세요.'}, status=status.HTTP_400_BAD_REQUEST)

    return language_header, error, has_error


def get_tag_list(data):
    """ data에 담긴 tag list에 맞는 tag object list 반환 """
    tag_list = []
    for idx, value in enumerate(data):
        tag_list.append(Tag.objects.get(name=value))

    return tag_list
