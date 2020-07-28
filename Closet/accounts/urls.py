from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup), #회원가입
    path('login/', login), # 로그인
    path('social_login/kakao', kakao_login), # kakao login
    path('activate/<str:uidb64>/<str:token>', Activate.as_view()), # email 인증
    path('email-verify/', email_verify),
    path('clothes_info/', ClothesInfo.as_view()), # 옷 정보 받기
]