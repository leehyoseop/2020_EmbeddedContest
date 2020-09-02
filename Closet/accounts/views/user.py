import json
import bcrypt
import jwt
from ..models import *
from ..serializers import *
from ..my_settings import SECRET_KEY, EMAIL
from ..token import account_activation_token
from ..text import message
from ..tokenCheck import *
from ..social_login import *

from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from datetime import datetime
now = datetime.now()

def signup(request, format=None):
    if request.method == 'GET':
        try :
            queryset = Account.objects.all()
            serializer = AccountSerializer(queryset, many=True)
            return JsonResponse(serializer.data, safe=False)

        except Exception as e :
            print('signup get e : ', e)
            return JsonResponse(e, safe=False)

    if request.method == 'POST': # email, username이 null일 때도 확인(프론트 측에서), email form이 맞는지 확인
        try:           
            email = request.POST.get('email', '')
            pw = request.POST.get('password', '')
            password = bcrypt.hashpw(pw.encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')
            username = request.POST.get('username', '')
   
            print("email = " + email+" username = " + username)
            myuser = Account.objects.filter(email=email)

            if myuser: # 이미 등록된 email이라면 회원가입 불가
                print("duplicated email")
                return JsonResponse({'code':400, 'msg':'duplicated email'}, status=201)
            else : 
                user = Account.objects.create(
                    email = email,
                    password=password,
                    username=username,
                    is_active=False,
                    platform=0
                )

                current_site = get_current_site(request)
                domain = current_site.domain
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = account_activation_token.make_token(user)

                mail_title = "ICE CLOSET 이메일 인증"
                message_data = message(domain, uidb64, token)
                mail_to = email
                email = EmailMessage(mail_title, message_data, to=[mail_to])
                email.send()

                print("signup success and send email")
                return JsonResponse({'code':201, 'msg':'signup success'}, status=201)

        except KeyError:
            return JsonResponse({'code':400, 'msg':'INVALID KEY'}, status=201)
        except TypeError:
            return JsonResponse({"code":400, 'msg':'INVALID_TYPE'}, status=201)
        except ValidationError:
            return JsonResponse({'code':400, 'msg':'VALIDATION ERROR'}, status=201)
        except Exception as e:
            print('signup post e : ', e)
            return JsonResponse({'code':400, 'msg':e}, status=201)

def login(request, format=None): 
    try :
        if request.method == "POST":
            email = request.POST.get('email', '')
            print('login email = ' , email)
            myuser = Account.objects.filter(email=email)
            if myuser: # email이 db에 저장되어있으면
                print("email exits")
                user = Account.objects.get(email=email)
                password = request.POST.get('password', '')
                if bcrypt.checkpw(password.encode('UTF-8'), user.password.encode('UTF-8')):
                    print("password correct, my user!")
                    if user.is_active == True: # email 인증까지 완료한 회원이면 로그인 성공
                        print("user is_active turns True")
                        token = jwt.encode({'user':user.id}, SECRET_KEY['secret'], SECRET_KEY['algorithm']).decode('UTF-8')
                        print("token = ", token)
                        return JsonResponse({'code':201, 'msg':'login success', 'token':token}, status=201) # login 시 token 발급
                    return JsonResponse({'code':0, 'msg':'not activated account'}, status=201) # email 활성화 되지 않음
                return JsonResponse({'code':1, 'msg':'password incorrect'}, status=201) # email에 매칭된 pw가 틀림
            return JsonResponse({'code':2, 'msg':'not my user'}, status=201) # 해당 email이 db에 없음
    except Exception as e :
        print('login e : ', e)
        return JsonResponse({'code':400, 'msg':e}, status=400)

def kakao_login(request, format=None): # 앱연동 테스트 해보기, get 넣어주기
    try :
        if request.method == "POST":
            platform = 1
            uid = request.POST.get('uid', '')
            email = request.POST.get('email', '')
            result = social_login(platform=platform, uid=uid, email=email) # social_login 파일에서 처리
            if(result == False): # uid or email 길이가 0 일 때
                return JsonResponse({'code':503, 'msg':'login fail', 'token':''}, status=201) # 소셜로그인 실패(정보가 안넘어왔을 경우)
            print("token : ", result['token'])
            return JsonResponse({'code':201, 'msg':'login success', 'token':result['token']}, status=201) # 소셜로그인 성공
    except Exception as e :
        print('kakao_login e :', e)
        return JsonResponse({'code':400, 'msg':e}, status=400)

def google_login(request, format=None):
    try :
        if request.method == "POST":
            platform = 2
            uid = request.POST.get('uid', '')
            email = request.POST.get('email', '')
            result = social_login(platform=platform, uid=uid, email=email)
            if(result == False):
                return JsonResponse({'code':503, 'msg':'login fail', 'token':'token fail'}, status=201) # 소셜로그인 실패(정보가 안넘어왔을 경우)
            return JsonResponse({'code':201, 'msg':'login success', 'token':result['token']}, status=201) # 소셜로그인 성공
    except Exception as e :
        print('google_login e : ', e)
        return JsonResponse({'code':400, 'msg':e}, status=400)


# logout 시에는 android 앱에서 토큰을 더이상 넘겨주지 않으면 됨.
class Activate(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)
            print("uid = ", uid, " user = ", user)

            if account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                return redirect(EMAIL['REDIRECT_PAGE'])
            return JsonResponse({'code':401, 'msg':'auth fail'}, status=201)

        except ValidationError:
            return JsonResponse({'code':400, 'msg':'TYPE ERROR'}, status=201)
        except KeyError:
            print("class Activate key error")
            return JsonResponse({'code':400, 'msg':'KEY ERROR'}, status=201)

def email_verify(request):
    try :
        return render(request, 'accounts/verify.html')
    except Exception as e :
        print('email_verify e : ', e)
        return render(request, e)