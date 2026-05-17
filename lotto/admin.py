from django.contrib import admin
from .models import Draw, Ticket

# 관리자 페이지에서 볼 수 있도록 등록
admin.site.register(Draw)
admin.site.register(Ticket)

# Register your models here.
