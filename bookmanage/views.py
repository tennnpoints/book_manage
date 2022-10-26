from re import template
from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.http import JsonResponse
from .log import Logging
import bookmanage.const as const
import datetime
import logging

from .models import UserManage,BookManage

class LoginView(View):
    def get(self, request):
        params = {}
        return render(request, 'bookmanage/login.html', params)
    
    def post(self, request):
        params = {}
        form_uid = request.POST.get('userid')
        form_pw = request.POST.get('password')
        u = UserManage.objects.filter(mail_adress__iexact=form_uid).filter(password__exact=form_pw)
        if len(u) == 1 :
            # 合致した処理
            request.session['userid'] = u[0].user_id
            request.session['username'] = u[0].user_name
            return redirect('bookmanage:mypage')
        else: 
            params = {'mail': form_uid, 'error': const.ERROR}
            return render(request, 'bookmanage/login.html', params)

class RegisterView(View):
    def get(self, request):
        params = {'error': const.CLEAR, 'errormsg': ''}
        return render(request, 'bookmanage/register.html', params)

    def post(self,request):
        req = request.POST
        uname = req.get('uname')
        uid = req.get('uid')
        uidconf = req.get('uidconf')
        pwd = req.get('pwd')
        pwdconf = req.get('pwdconf')
        params = { 'error': const.CLEAR, 'uiderror': const.CLEAR, 'pwderror': const.CLEAR }
        if uname == '' :
            errormsg = 'ユーザー名が空欄です'
            params['error'] = const.ERROR
            params['nameerror'] = const.ERROR
            params['nameerrormsg'] = errormsg
            
        if uid == '' and uidconf == '' :
            errormsg = 'メールアドレスが空欄です'
            params['error'] = const.ERROR
            params['uiderror'] = const.ERROR
            params['uiderrormsg'] = errormsg

        if uid != uidconf :
            errormsg = '確認用のメールアドレスが異なります'
            params['error'] = const.ERROR
            params['uiderror'] = const.ERROR
            params['uiderrormsg'] = errormsg
            
        if pwd == '' and pwdconf == '' :
            errormsg = 'パスワードが空欄です'
            params['error'] = const.ERROR
            params['pwderror'] = const.ERROR
            params['pwderrormsg'] = errormsg

        if pwd != pwdconf :
            errormsg = '確認用のパスワードが異なります'
            params['error'] = const.ERROR
            params['pwderror'] = const.ERROR
            params['pwderrormsg'] = errormsg

        # if 登録済みのメールアドレスかどうか
        u = UserManage.objects.filter(mail_adress__iexact=uid)
        if len(u) != 0 :
            errormsg = '既に登録されているメールアドレスです'
            params['error'] = const.ERROR
            params['uiderror'] = const.ERROR
            params['uiderrormsg'] = errormsg

        print(params)
        if params['error'] == const.CLEAR :
            #ここに新規登録の処理
            print('hoge')
            # user_id mail_adress password user_name regist_date
            tdy = datetime.datetime.today()
            idcount = UserManage.objects.all().count()
            um = UserManage.objects.create(user_id=idcount, mail_adress=uid, password=pwd, user_name=uname, regist_date=tdy)
            print('model',um)
            #ここにセッション書き込み
            request.session['userid'] = idcount
            request.session['username'] = uname

        return JsonResponse(params)

class MypageView(View):
    def get(self,request):
        params = {}
        uid = request.session['userid']
        unreadlist = BookManage.objects.filter(user_id=uid).filter(status=0)
        readinglist = BookManage.objects.filter(user_id=uid).filter(status=1)
        readlist = BookManage.objects.filter(user_id=uid).filter(status=2)
        params = { 'unreadlist': unreadlist, 'readinglist': readinglist, 'readlist': readlist}
        return render(request, 'bookmanage/mypage.html', params)
    
class MypageRenewView(View):
    def post(self,request):
        log = Logging()
        book_id = request.POST.get('book_id')
        proc_status = int(request.POST.get('proc_status'))
        bookupdate = BookManage.objects.get(id=book_id)
        log.info('Renew :'+str(proc_status))
        tdy = datetime.datetime.today()
        if proc_status == const.DELETE :
            bookupdate.delete()
        else :
            if bookupdate.status == const.UNREAD :
                if proc_status == const.END :
                    bookupdate.status = const.END
                    bookupdate.book_start_date = tdy
                    bookupdate.book_end_date = tdy
                else :
                    bookupdate.status = const.READING
                    bookupdate.book_start_date = tdy


            elif bookupdate.status == const.READING :
                bookupdate.status = proc_status
                if proc_status != const.UNREAD :
                    bookupdate.book_end_date = tdy
                    
            elif bookupdate.status == const.END :
                bookupdate.status = proc_status
                if proc_status != const.UNREAD :
                    bookupdate.book_start_date = tdy
            bookupdate.save()

        params = { 'msg': 'asd'}
        return JsonResponse(params)

class BookRegistView(View):
    def post(self,request):
        logger = logging.getLogger('bookmanage')
        book_name = request.POST.get('book_name')
        book_author = request.POST.get('book_author')
        logger.info('Book Name :'+str(book_name))
        logger.info('Author Name :'+str(book_author))
        params = { 'error': const.CLEAR, 'errormsg': ''}
        errormsg = []
        if book_name == '' :
            params['error'] = const.ERROR
            errormsg.append('書籍名が空欄です')
        if book_author == '' :
            params['error'] = const.ERROR
            errormsg.append('著者名が空欄です')

        if params['error'] == const.ERROR : 
            params['errormsg'] = '<br>'.join(errormsg)
        else :
            uid = request.session['userid']
            tdy = datetime.datetime.today()
            bm = BookManage.objects.create(user_id=uid, book_name=book_name, book_author=book_author, status=const.UNREAD, book_start_date=tdy , book_end_date=tdy)
        
        return JsonResponse(params)