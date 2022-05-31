import sys
import os
import django
import csv

# system setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath((__file__))))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'config.settings.develop')
django.setup()

from django.conf import settings
from companies.models import Company, Tag, Language, CompanyName
from companies.utils import get_tag_list

# db upload path
base_path = settings.DATA_ROOT
csv_path = base_path + 'wanted_temp_data.csv'


def insert_language():
    """
        # companies.Language
        csv 파일 내 language 'ko', 'en', 'ja' insert
    """
    data = {
        'name': [
            'ko', 'en', 'ja'
        ],
        'description': [
            '한국어', '영어', '일본어'
        ]
    }

    Language.objects.all().delete()

    for idx in range(len(data['name'])):
        Language.objects.get_or_create(
            name=data['name'][idx],
            description=data['description'][idx]
        )

    print("Language UPLOADED SUCCESS!")


def get_language():
    """ language object """
    language_ko = Language.objects.get(name='ko')
    language_en = Language.objects.get(name='en')
    language_jp = Language.objects.get(name='ja')

    return language_ko, language_en, language_jp


def insert_tags():
    """
        # companies.Tag
        csv 파일 내 tag list 0 - 30 '태그_', 'tag_', 'タグ_' insert
    """
    Tag.objects.all().delete()

    language_ko, language_en, language_ja = get_language()

    for idx in range(1, 31):
        str_idx = str(idx)

        Tag.objects.get_or_create(
            language=language_ko,
            name='태그_' + str_idx
        )
        Tag.objects.get_or_create(
            language=language_en,
            name='tag_' + str_idx
        )
        Tag.objects.get_or_create(
            language=language_ja,
            name='タグ_' + str_idx
        )

    print("Tag UPLOADED SUCCESS!")


def insert_company():
    """
        # companies.Company + CompanyName
    """
    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        data_reader = csv.DictReader(csvfile)

        Company.objects.all().delete()
        CompanyName.objects.all().delete()

        language_ko, language_en, language_ja = get_language()

        for idx, row in enumerate(data_reader):
            if row['company_ko'] or row['company_en'] or row['company_ja']:
                Company.objects.get_or_create(
                    id=idx + 1
                )

                company_id = Company.objects.latest('id')
                CompanyName.objects.get_or_create(
                    company=company_id,
                    language=language_ko,
                    name=row['company_ko']
                )
                CompanyName.objects.get_or_create(
                    company=company_id,
                    language=language_en,
                    name=row['company_en']
                )
                CompanyName.objects.get_or_create(
                    company=company_id,
                    language=language_ja,
                    name=row['company_ja']
                )

                # ManyToManyField 'tags' insert
                # CompanyName, Tag 사이의 중간테이블에 .add()로 tag data 추가
                CompanyName.objects.filter(language=language_ko).latest('company')\
                    .tags.add(*get_tag_list(row['tag_ko'].split('|')))
                CompanyName.objects.filter(language=language_en).latest('company')\
                    .tags.add(*get_tag_list(row['tag_en'].split('|')))
                CompanyName.objects.filter(language=language_ja).latest('company')\
                    .tags.add(*get_tag_list(row['tag_ja'].split('|')))

    print("Company Info UPLOADED SUCCESS!")


insert_language()
insert_tags()
insert_company()
