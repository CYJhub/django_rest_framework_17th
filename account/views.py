import jwt
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer,SchoolSerializer,SignUpSerializer,LoginSerializer
from django_rest_framework_17th.settings import SECRET_KEY, REFRESH_TOKEN_SECRET_KEY


# cotroller 작업

#회원가입
class SignupView(APIView):
    def post(self, request): #프론트에서 올린 데이터(request)
        serializer = SignUpSerializer(data=request.data)
        #입력된 데이터가 유효하다면,에러발생X
        if serializer.is_valid(raise_exception=False):
            user = serializer.save()
            response = Response(
                {
                    "user_id": user.user_id,
                    "message": "회원가입 성공",
                },
                status=status.HTTP_200_OK,
            )
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#로그인
#post요청을 받으면 LoginSerializer를 이용해 데이터를 검증하고, 유효한 데이터의 경우
#유저 인증 후 access token을 LoginSerializer에서 가져와 response를 반환


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            #유효성 검사를 통과한 경우 토큰 확인
            #serializer.validated_data는 프론트에서 전송한 request.data에서 추출됨
            user_id=serializer.validated_data.get("user_id")

            # jwt token(refresh(장기), access(단기) 발급한걸 가져옴
            access_token = serializer.validated_data['access_token']
            refresh_token = serializer.validated_data['refresh_token']


            response = Response({
                "user_id": user_id,
                "message": "로그인 성공",
                "token":{
                "access_token": access_token.__str__(),
                "refresh_token": refresh_token.__str__(),
                 }},
                status=status.HTTP_200_OK, )

            #쿠키에 삽입 후 프론트로 전달
            response.set_cookie("access_token", access_token.__str__(), httponly=True, secure=True,
                                max_age=60 * 60 * 1)  # 쿠키 만료 시간을 1시간으로 설정
            response.set_cookie("refresh_token", access_token.__str__(), httponly=True, secure=True,
                                max_age=60 * 60 * 24)  # 쿠키 만료 시간을 24시간으로 설정
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 로그 아웃
class LogoutView(APIView):

    #로그아웃시 jwt토큰 삭제
    def post(self, request):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response

#jwt의 구조
# 1.header: 토큰 타입(JWT)와 알고리즘(HS256) 저장
# 2.payload: 사용자 또는 토큰 속성 정보(생성,만료,대상자) 저장
# 3.signature: 비밀키

#토큰인가
#프론트에서 axios-get header에 access_token을 담아 보낸 경우
#이를 인코딩하여 해당 유저의 정보를 반환

#고객정보
class AuthView(APIView):
    def get(self, request):
        #access token을 프론트가 보낸 request에서 추출
        access_token = request.COOKIES.get('access_token')

        #access token이 없다면 에러 발생
        if not access_token:
            return Response({"message": "access token 없음"}, status=status.HTTP_401_UNAUTHORIZED)

        #access token이 있다면
        #토큰 디코딩(유저 식별)
        try:
            #payload에서 user_id(고유한 식별자)를 추출
            #payload={'user_id:1'}
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256']) #accesstoken 번호
            user_id = payload.get('user_id')
            #해당 유저 아이디를 가지는 객체 user을 가져와
            user = get_object_or_404(pk=user_id)
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
                user_id = payload.get('user_id')
                user = get_object_or_404(pk=user_id)

                #새로운 access_token 발급
                access_token = jwt.encode({"user_id": user.pk}, SECRET_KEY, algorithm='HS256')

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
