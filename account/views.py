import jwt
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializer, SignUpSerializer, LoginSerializer
from django_rest_framework_17th.settings import SECRET_KEY, REFRESH_TOKEN_SECRET_KEY


class SignupView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid(raise_exception=False):
            user = serializer.save(request)
            response = Response(
                {
                    "id": user.id,
                    "message": "회원가입 성공",
                },
                status=status.HTTP_200_OK,
            )
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            #유효성 검사를 통과한 경우 토큰 확인
            #serializer.validated_data는 프론트에서 전송한 request.data에서 추출됨
            id=serializer.validated_data.get("id")

            access_token = serializer.validated_data['access_token']
            refresh_token = serializer.validated_data['refresh_token']

            response = Response({
                "id": id,
                "message": "로그인 성공",
                "token":{
                "access_token": access_token.__str__(),
                "refresh_token": refresh_token.__str__(),
                 }},
                status=status.HTTP_200_OK, )

            response.set_cookie("access_token", access_token.__str__(), httponly=True, secure=True,
                                max_age=60 * 60 * 1)  # 쿠키 만료 시간을 1시간으로 설정
            response.set_cookie("refresh_token", access_token.__str__(), httponly=True, secure=True,
                                max_age=60 * 60 * 24)  # 쿠키 만료 시간을 24시간으로 설정
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response



class AuthView(APIView):
    def get(self, request):
        # "Bearer <access_token>" 형식으로 반환되기 때문에, 분리한 후 access_token만 추출
        access_token = request.META['HTTP_AUTHORIZATION'].split()[1]

        if not access_token:
             return Response({"message": "access token 없음"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # payload에서 user_id(고유한 식별자)를 추출
            # payload={'user_id:1'}
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256']) # accesstoken 번호
            id = payload.get('user_id')
            #해당 유저 아이디를 가지는 객체 user을 가져와
            user = get_object_or_404(User, id=id)
            #UserSerializer로 JSON화 시켜준 뒤,
            serializer = UserSerializer(instance=user)
            #프론트로 200과 함께 재전송
            return Response(serializer.data, status=status.HTTP_200_OK)

         #Access token 예외 처리
        except jwt.exceptions.InvalidSignatureError:
            #access_token 유효하지 않음
            return Response({"message": "유효하지 않은 access token"}, status=status.HTTP_401_UNAUTHORIZED)

        except jwt.exceptions.ExpiredSignatureError:
            # access_token 만료 기간 다 됨
            refresh_token = request.COOKIES.get('refresh_token')

            #refresh_token이 없다면 에러 발생
            if not refresh_token:
                return Response({"message": "refresh token 없음"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                #refresh_token 디코딩
                payload = jwt.decode(refresh_token, REFRESH_TOKEN_SECRET_KEY, algorithms=['HS256'])
                id = payload.get('id')
                user = get_object_or_404(pk=id)

                #새로운 access_token 발급
                access_token = jwt.encode({"id": user.pk}, SECRET_KEY, algorithm='HS256')

                #access_token을 쿠키에 저장하여 프론트로 전송
                response = Response(UserSerializer(instance=user).data, status=status.HTTP_200_OK)
                response.set_cookie(key='access_token', value=access_token, httponly=True, samesite='None', secure=True)

                return response

            # refresh_token 예외 처리
            except jwt.exceptions.InvalidSignatureError:
                # refresh_token 유효하지 않음
                return Response({"message": "유효하지 않은 refresh token"}, status=status.HTTP_401_UNAUTHORIZED)

            except jwt.exceptions.ExpiredSignatureError:
                # refresh_token 만료 기간 다 됨 => 이경우에는, 사용자가 로그아웃 후 재로그인하도록 유인 => 리다이렉트
                return Response({"message": "refresh token 기간 만료"}, status=status.HTTP_401_UNAUTHORIZED)
