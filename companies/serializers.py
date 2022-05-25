from rest_framework import serializers
from companies.models import CompanyName


class CompanyNameSerializers(serializers.ModelSerializer):
    company_name = serializers.CharField(source='name')
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = CompanyName
        fields = (
            'company_name', 'tags'
        )
