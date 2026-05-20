from django.contrib import admin
from django.shortcuts import redirect
from .models import Draw, Ticket

def admin_login_view(request):
    return redirect('/accounts/login/')

admin.site.login = admin_login_view

# 관리자 페이지에서 볼 수 있도록 등록
admin.site.register(Draw)
admin.site.register(Ticket)

# Register your models here.
