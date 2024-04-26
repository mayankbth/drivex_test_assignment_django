# Generated by Django 4.2.11 on 2024-04-26 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('birth_year', models.IntegerField(blank=True, null=True)),
                ('death_year', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('copyright', models.BooleanField(blank=True, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('rent_fee', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BooksAuthorsMappers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authors', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.authors')),
                ('books', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.books')),
            ],
        ),
    ]
