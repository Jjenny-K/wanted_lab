from django.db import models


class Company(models.Model):

    def __str__(self):
        return f'company_({self.id})'


class Language(models.Model):
    name = models.CharField(verbose_name='언어', max_length=20)
    description = models.CharField(verbose_name='언어설명', max_length=127)

    def __str__(self):
        return self.name


class Tag(models.Model):
    language = models.ForeignKey('companies.Language', verbose_name='언어', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='태그', max_length=20, unique=True)
    description = models.CharField(verbose_name='태그설명', max_length=127, blank=True, default='')

    def __str__(self):
        return self.name


class CompanyName(models.Model):
    company = models.ForeignKey('companies.Company', verbose_name='회사', on_delete=models.CASCADE)
    language = models.ForeignKey('companies.Language', verbose_name='언어', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='회사명', max_length=255, blank=True, default='')
    tags = models.ManyToManyField('Tag', verbose_name='태그', blank=True, default='')

    def __str__(self):
        return f'company_name({self.company}, {self.name})'
