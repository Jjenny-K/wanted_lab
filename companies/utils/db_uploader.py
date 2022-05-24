import sys
import os
import django
import csv

# system setup
sys.path.append((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'config.settings')
django.setup()

from django.conf import settings
from companies.models import Company, Tag, Language, CompanyKeyVal, TagKeyVal

# db upload path
base_path = settings.DATA_ROOT
csv_path = base_path + 'wanted_temp_data.csv'

# companies.Language
def insert_language():
    data = {
        'name': [
            'ko', 'en', 'ja'
        ],
        'description': [
            '한국어', '영어', '일본어'
        ]
    }

    Language.objects.all().delete()
    length = len(data['name'])

    for idx in range(length):
        Language.objects.get_or_create(
            name=data['name'][idx],
            description=data['description'][idx]
        )

    print("Language UPLOADED SUCCESS!")


# tag_name split to list
def set_list(data):
    return data.split('|')


# companies.Company + CompanyKeyVal + Tag + TagKeyVal
def insert_company():
    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        data_reader = csv.DictReader(csvfile)

        Company.objects.all().delete()
        CompanyKeyVal.objects.all().delete()

        language_id_ko = Language.objects.get(name='ko')
        language_id_en = Language.objects.get(name='en')
        language_id_jp = Language.objects.get(name='ja')

        for row in data_reader:
            if row['company_ko'] or row['company_en'] or row['company_ja']:
                Company.objects.get_or_create()

                company_number = Company.objects.latest('number')
                print(company_number)
                CompanyKeyVal.objects.get_or_create(
                    number=company_number,
                    language=language_id_ko,
                    name=row['company_ko']
                )
                CompanyKeyVal.objects.get_or_create(
                    number=company_number,
                    language=language_id_en,
                    name=row['company_en']
                )
                CompanyKeyVal.objects.get_or_create(
                    number=company_number,
                    language=language_id_jp,
                    name=row['company_ja']
                )

                Tag.objects.get_or_create(company_num=company_number)
                tag_number = Tag.objects.latest('number')

                TagKeyVal.objects.get_or_create(
                    number=tag_number,
                    language=language_id_ko,
                    name=set_list(row['tag_ko'])
                )
                TagKeyVal.objects.get_or_create(
                    number=tag_number,
                    language=language_id_en,
                    name=set_list(row['tag_en'])
                )
                TagKeyVal.objects.get_or_create(
                    number=tag_number,
                    language=language_id_jp,
                    name=set_list(row['tag_ja'])
                )

    print("Company Info UPLOADED SUCCESS!")


# insert_language()
insert_company()
