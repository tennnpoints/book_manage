# Generated by Django 4.1 on 2022-09-24 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BookManage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_id", models.IntegerField()),
                ("book_name", models.CharField(max_length=100)),
                ("book_author", models.CharField(max_length=100)),
                ("status", models.IntegerField()),
                ("book_start_date", models.DateField()),
                ("book_end_date", models.DateField()),
            ],
            options={"db_table": "book_manage",},
        ),
        migrations.CreateModel(
            name="UserManage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_id", models.IntegerField()),
                ("mail_adress", models.EmailField(max_length=254)),
                ("password", models.CharField(max_length=100)),
                ("user_name", models.CharField(max_length=100)),
                ("regist_date", models.DateField()),
            ],
            options={"db_table": "user_manage",},
        ),
    ]
