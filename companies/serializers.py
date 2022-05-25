from rest_framework import serializers
from companies.models import CompanyName


class CompanyNameSerializers(serializers.ModelSerializer):
    class Meta:
        model = CompanyName
        fields = '__all__'


class CompanyNameListSerializers(serializers.ModelSerializer):
    company_name = serializers.CharField(source='name')
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = CompanyName
        fields = (
            'company_name', 'tags'
        )
        read_only_fields = (
            'company_name', 'tags'
        )
