from django.contrib import admin
from django.urls import path, include
from lotto import views as lotto_views  # lotto 앱의 회원가입 뷰를 가져옴.

urlpatterns = [
    # 1. 관리자 전용 숨겨진 주소
    path('secret-admin-access/', admin.site.urls),
    
    # 2. 일반 사용자 회원가입
    path('accounts/signup/', lotto_views.signup, name='signup'),
    
    # 3. 장고 기본 로그인/로그아웃 제공 주소록
    path('accounts/', include('django.contrib.auth.urls')),
    
    # 4. 로또 앱 메인 페이지 주소록
    path('', include('lotto.urls')),
]
