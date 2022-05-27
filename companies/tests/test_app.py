import pytest

from django.urls import reverse

pytestmark = pytest.mark.django_db


class Test_CompanyNameAPI:
    header_ko = {"HTTP_x-wanted-language": "ko"}
    post_data_tw = {
        "company_name": {
            "ko": "라인 프레쉬",
            "tw": "LINE FRESH",
            "en": "LINE FRESH",
        },
        "tags": [
            {
                "tag_name": {
                    "ko": "태그_1",
                    "tw": "tag_1",
                    "en": "tag_1",
                }
            },
            {
                "tag_name": {
                    "ko": "태그_8",
                    "tw": "tag_8",
                    "en": "tag_8",
                }
            },
            {
                "tag_name": {
                    "ko": "태그_15",
                    "tw": "tag_15",
                    "en": "tag_15",
                }
            }
        ]
    }
    post_data = {
        "company_name": {
            "ko": "라인 프레쉬",
            "ja": "LINE FRESH",
            "en": "LINE FRESH",
        },
        "tags": [
            {
                "tag_name": {
                    "ko": "태그_1",
                    "ja": "tag_1",
                    "en": "tag_1",
                }
            },
            {
                "tag_name": {
                    "ko": "태그_8",
                    "ja": "tag_8",
                    "en": "tag_8",
                }
            },
            {
                "tag_name": {
                    "ko": "태그_15",
                    "ja": "tag_15",
                    "en": "tag_15",
                }
            }
        ]
    }

    def test_company_name_autocomplete(self, client):
        """
        1. 회사명 자동완성
        회사명의 일부만 들어가도 검색이 되어야 합니다.
        header의 x-wanted-language 언어값에 따라 해당 언어로 출력되어야 합니다.
        """
        search_url = reverse('companies_search') + '?query=링크'

        response = client.get(search_url, **self.header_ko)
        searched_companies = response.data

        assert response.status_code == 200
        assert searched_companies == [
            {"company_name": "주식회사 링크드코리아"},
            {"company_name": "스피링크"},
        ]

    def test_company_search(self, client):
        """
        2. 회사 이름으로 회사 검색
        header의 x-wanted-language 언어값에 따라 해당 언어로 출력되어야 합니다.
        """
        retrieve_url = reverse('companies_retrieve', kwargs={'name': 'Wantedlab'})

        response = client.get(retrieve_url, **self.header_ko)
        company = response.data

        assert response.status_code == 200
        assert company == {
            "company_name": "원티드랩",
            "tags": [
                "태그_4",
                "태그_16",
                "태그_20",
            ],
        }

        # 검색된 회사가 없는 경우 404를 리턴합니다.
        retrieve_url_none = reverse('companies_retrieve', kwargs={'name': '없는회사'})

        response_none = client.get(retrieve_url_none, **self.header_ko)

        assert response_none.status_code == 404

    def test_new_company(self, client):
        """
        3.  새로운 회사 추가
        새로운 언어(tw)도 같이 추가 될 수 있습니다.
        저장 완료후 header의 x-wanted-language 언어값에 따라 해당 언어로 출력되어야 합니다.
        """
        list_url = reverse('companies_list')

        # 새로운 언어를 따로 등록한 후, 새로운 회사를 추가할 때 해당 언어를 사용할 수 있습니다.
        # 해당 언어가 없을 경우, '지원하지 않는 언어입니다.' 400 error를 반환합니다.
        response_header_tw = client.post(list_url, json=self.post_data_tw, **{"HTTP_x-wanted-language": "tw"})

        assert response_header_tw.status_code == 400

        # 언어가 모두 등록된 경우
        headers_post = {
            'CONTENT_TYPE': 'application/json;charset=UTF-8',
            'HTTP_x-wanted-language': 'en'
        }

        response_header_en = client.post(list_url, data=self.post_data, **headers_post, format='json')
        company = response_header_en.data

        assert response_header_en.status_code == 201
        assert company == {
            "company_name": "LINE FRESH",
            "tags": [
                "tag_1",
                "tag_8",
                "tag_15",
            ],
        }
