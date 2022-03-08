from django.db.models import Q
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils import tree
from django.utils.translation import ugettext_lazy as _

from rest_framework import status
from rest_framework import authentication
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication

from .models import PreRegister
from .serializers import UserSerializer, PreRegisterSerializer
from .error import AlreadyExists
from .email import ConfirmationEmail

User = get_user_model()


class CreatePreRegister(APIView):
    def exist_user(self,email):
        try:
            user = User.objects.get(email=email)
            raise AlreadyExists
        except User.DoesNotExist:
            pass

    
    def exist_pre_register(self, email):
        try:
            preregister = PreRegister.objects.get(email=email)
            preregister.delete()
        except PreRegister.DoesNotExist:
            pass
    


    def post(self, request):
        # print(request)
        try:
            self.exist_user(request.data['email'])
            self.exist_pre_register(request.data['email'])
            serializer = PreRegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                # from_mail = settings.EMAIL_HOST_USER
                # # print(from_mail)
                # # raise ValidationError(from_mail)
                # send_mail('Subject here', 'Here is the message.', from_mail, ['kentaro.miyamoto1001@gmail.com'], fail_silently=False)
                pre_register = PreRegister.objects.get(email=request.data['email'])

                if pre_register:
                    context = {"pre_register": pre_register}
                    to = [pre_register.email]
                    ConfirmationEmail(self.request, context).send(to)

                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.data}, status=status.HTTP_400_BAD_REQUEST)
        except AlreadyExists:
            data = {
                "error":"AlreadyExists",
                "error_message": "そのメールアドレスは既に登録されています",
            }
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)

        # except Exception:
        #     data = {
        #         "error":"DoesNotExist",
        #         "error_message": "PreRegister DoesNotExist",
        #     }
        #     return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)

class CertificationPreRegister(APIView):
    def post(self, request):
        try:
            email = request.data['email']
            authentication_code = request.data['code']
            preregister = PreRegister.objects.get(email=email)
            print("auth_code",authentication_code)
            confirm = preregister.confirm_code(authentication_code)
            if confirm=='Success':
                data = {
                    "email": email,
                    "username": request.data['username'],
                    "password": request.data['password']
                }
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                # create_user = preregister.create_user(data,authentication_code)
                # if create_user == 'Success':
                #     return Response({"status": "success", "data": data}, status=status.HTTP_200_OK)

                # elif create_user == 'AlreadyExists':
                #     data = {
                #         "error":"AlreadyExists",
                #         "error_message": "このアカウント名は既に存在しています。",
                #     }
                #     return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)

                # elif create_user == 'FailureAuthentication':
                #     data = {
                #         "error":"FailureAuthentication",
                #         "error_message": "認証コードが違います。もう一度、メールを確認してください。",
                #     }
                #     return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)

                # else:
                #     data = {
                #         "error":"SomethingWrong",
                #         "error_message": "不明のエラーが発生しました。",
                #     }
                #     return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)

            elif confirm=='FailureAuthentication':
                data = {
                    "error":"FailureAuthentication",
                    "error_message": "認証コードが違います。もう一度、メールを確認してください。",
                }
                return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)
            elif confirm=='Expired':
                data = {
                    "error":"Expired",
                    "error_message": "認証コードの有効期限が切れました。再発行してください。",
                }
                return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)

        except PreRegister.DoesNotExist:
            # print('acount dose not exist')
            data = {
                "error":"DoesNotExist",
                "error_message": "このメールアドレスに確認コードを発送していません。",
            }
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)
        # except Exception:
        #     data = {
        #         "error_message": "something wrong",
        #     }
        #     return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)


class UpdateUser(APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, format=None):
        content = {'user': str(request.user), 'auth': str(request.auth)}
        return Response(content)

# class CheckView(APIView):
#     authentication_classes = [TokenAuthentication, ]

#     def get(self, request, *args, **kwargs):
#         return Response({"data": "中身です"})
#     # def post(self, request, format=None):
#     #     user = User.objects.get()



class UserEmailAlreadyExists(APIView):
    def post(self, request):
        try:
            user = User.objects.get(email=request.data["email"])
            data = {
                "error":"AlreadyExists",
                "error_message": "このメールアドレスは既に存在しています。",
            }
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            data = {
                "email":request.data['email'],
            }
            return Response({"status": "success", "data": data}, status=status.HTTP_200_OK)

class UserNameAlreadyExists(APIView):
    def post(self, request):
        try:
            user = User.objects.get(username=request.data["username"])
            data = {
                "error":"AlreadyExists",
                "error_message": "このユーザーネームは既に存在しています。",
            }
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            data = {
                "username":request.data['username'],
            }
            return Response({"status": "success", "data": data}, status=status.HTTP_200_OK)

class UserEmailDoesNotExist(APIView):
    def post(self, request):
        try:
            user = User.objects.get(email=request.data["email"])
            data = {
                "email":request.data['email'],
            }
            return Response({"status": "success", "data": data}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            data = {
                "error":"DoseNotExist",
                "error_message": "このユーザーは存在していません",
            }
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)

class UserNameDoesNotExist(APIView):
    def post(self, request):
        try:
            user = User.objects.get(username=request.data["username"])
            data = {
                "username":request.data['username'],
            }
            return Response({"status": "success", "data": data}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            data = {
                "error":"DoseNotExist",
                "error_message": "このユーザーは存在していません",
            }
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)