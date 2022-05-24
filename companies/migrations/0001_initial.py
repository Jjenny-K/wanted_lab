# Generated by Django 4.0.4 on 2022-05-24 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='언어')),
                ('description', models.CharField(max_length=127, verbose_name='언어설명')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='태그')),
                ('description', models.CharField(blank=True, default='', max_length=127, verbose_name='태그설명')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=255, verbose_name='회사명')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.company', verbose_name='회사')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.language', verbose_name='언어')),
                ('tags', models.ManyToManyField(to='companies.tag', verbose_name='태그')),
            ],
        ),
    ]
