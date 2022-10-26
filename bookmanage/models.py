from django.db import models

class UserManage(models.Model):
    user_id = models.IntegerField()
    mail_adress = models.EmailField()
    password = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    regist_date = models.DateField()
    class Meta:
        db_table = 'user_manage'

class BookManage(models.Model):
    user_id = models.IntegerField()
    book_name = models.CharField(max_length=100)
    book_author = models.CharField(max_length=100)
    status = models.IntegerField()
    book_start_date = models.DateField()
    book_end_date = models.DateField()
    class Meta:
        db_table = 'book_manage'