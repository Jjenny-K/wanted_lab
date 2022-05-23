from django.db import models
from django.contrib.postgres.fields import ArrayField


class Company(models.Model):
    number = models.AutoField(verbose_name='회사번호', primary_key=True)

    def __str__(self):
        return f'company_number({self.number})'


class Tag(models.Model):
    number = models.AutoField(verbose_name='태그번호', primary_key=True)
    company_num = models.ForeignKey('companies.Company', on_delete=models.CASCADE)

    def __str__(self):
        return f'tag_number({self.company_num}, {self.number})'


class Language(models.Model):
    name = models.CharField(verbose_name='언어', max_length=20)
    description = models.CharField(verbose_name='언어설명', max_length=127)

    def __str__(self):
        return self.name


class CompanyKeyVal(models.Model):
    number = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
    language = models.ForeignKey('companies.Language', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='회사명', max_length=255, blank=True, default='')

    def __str__(self):
        return self.name


class TagKeyVal(models.Model):
    number = models.ForeignKey('companies.Tag', on_delete=models.CASCADE)
    language = models.ForeignKey('companies.Language', on_delete=models.CASCADE)
    name = ArrayField(models.CharField(verbose_name='태그명', max_length=127))

    def has_tag(self, name: str):
        return name in self.name

    def add_tag(self, name: str):
        if self.has_tag(name):
            return
        self.name.append(name)
        self.save(update_fields=['name'])
        return self.name

    def remove_tag(self, name: str):
        if not self.has_tag(name):
            return
        self.name.remove(name)
        self.save(update_fields=['name'])
        return self.name

    def __str__(self):
        return f'tag_name({self.language}, {self.name})'
