import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
import time
import random
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import UserSerializer
from .models import Account
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'status': 'error', 'message': '用户名和密码是必填项'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is not None:
            user.token = uuid.uuid4()
            user.save()
            logger.info(f"用户 {user.username} 登录成功")
            return Response({'status': 'success', 'token': str(user.token)})
        else:
            logger.error(f"用户 {username} 登录失败: 用户名或密码错误")
            return Response({'status': 'error', 'message': '用户名或密码错误'},
                            status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        auth_logout(request)
        return Response({'status': 'success', 'message': '登出成功'})

class SendCodeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        email = request.GET.get('email')
        if not email:
            return Response({'status': 'error', 'message': '邮箱是必填项'},
                            status=status.HTTP_400_BAD_REQUEST)

        last_request_time = cache.get(f'last_request_time_{email}')
        if last_request_time and time.time() - last_request_time < 60:
            return Response({'status': 'error', 'message': '请在一分钟后再次请求验证码'},
                            status=status.HTTP_429_TOO_MANY_REQUESTS)

        code = ''.join(random.choices('0123456789', k=6))
        cache.set(f'verification_code_{email}', code, timeout=300)
        cache.set(f'last_request_time_{email}', time.time(), timeout=60)

        send_mail(
            '验证码',
            f'您的验证码是: {code}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        logger.info(f"验证码 {code} 已发送到邮箱 {email}")
        return Response({'status': 'success', 'message': '验证码已发送'})

class VerifyCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        if not email or not code:
            return Response({'status': 'error', 'message': '邮箱和验证码是必填项'},
                            status=status.HTTP_400_BAD_REQUEST)

        cached_code = cache.get(f'verification_code_{email}')
        if not cached_code or cached_code != code:
            return Response({'status': 'error', 'message': '验证码无效'},
                            status=status.HTTP_400_BAD_REQUEST)

        cache.delete(f'verification_code_{email}')
        return Response({'status': 'success', 'message': '验证码有效'})

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'status': 'error', 'message': '邮箱和密码是必填项'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Account.objects.get(email=email)
            user.password = make_password(password)
            user.save()
            logger.info(f"用户 {user.username} 密码重置成功")
            return Response({'status': 'success', 'message': '密码重置成功'})
        except Account.DoesNotExist:
            logger.error(f"用户 {email} 不存在")
            return Response({'status': 'error', 'message': '无效的邮箱'},
                            status=status.HTTP_400_BAD_REQUEST)

class AskCodeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        email = request.GET.get('email')
        type = request.GET.get('type')

        if not email or not type:
            return Response({'status': 'error', 'message': '邮箱和类型是必填项'},
                            status=status.HTTP_400_BAD_REQUEST)

        if type not in ['register', 'reset']:
            return Response({'status': 'error', 'message': '无效的类型'},
                            status=status.HTTP_400_BAD_REQUEST)

        code = ''.join(random.choices('0123456789', k=6))
        cache.set(f'verification_code_{email}', code, timeout=300)

        send_mail(
            '验证码',
            f'您的验证码是: {code}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return Response({'status': 'success', 'message': '验证码已发送'})

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        code = request.data.get('code')
        role = request.data.get('role', 'user')  # 默认角色为 'user'

        if not username or not password or not email or not code:
            return Response({'status': 'error', 'message': '用户名、密码、邮箱和验证码是必填项'},
                            status=status.HTTP_400_BAD_REQUEST)

        cached_code = cache.get(f'verification_code_{email}')
        if not cached_code:
            logger.warning(f"注册失败：验证码已过期，邮箱={email}")
            return Response({'status': 'error', 'message': '验证码已过期'},
                            status=status.HTTP_400_BAD_REQUEST)
        if cached_code != code:
            logger.warning(f"注册失败：验证码无效，邮箱={email}")
            return Response({'status': 'error', 'message': '验证码无效'},
                            status=status.HTTP_400_BAD_REQUEST)

        if Account.objects.filter(email=email).exists():
            logger.warning(f"注册失败：邮箱已存在，邮箱={email}")
            return Response({'status': 'error', 'message': '使用这个邮箱的用户已经存在'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Account.objects.create(
                username=username,
                email=email,
                role=role,
                register_time=timezone.now()
            )
            user.password = make_password(password)
            user.save()
            logger.info(f"用户 {user.username} 注册成功")
            return Response({'status': 'success', 'message': '用户注册成功'},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"注册失败: {str(e)}")
            return Response({'status': 'error', 'message': f'注册失败，具体原因：{str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)