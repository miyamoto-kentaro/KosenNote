import imp
from django.db.models import Q
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils import tree
from django.utils.translation import ugettext_lazy as _
from requests import delete

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

from .models import Following, PreRegister, ChangeEmailTicket
from .serializers import UserSerializer, PreRegisterSerializer, ChangeEmailTicketSerializer, FollowingSerializer
from .error import AlreadyExists
from .email import ConfirmationEmail, ChangeEmailConfirmationEmail


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
                serializer = UserSerializer(data=data)
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
    def put(self, request, format=None):
        try:
            user = User.objects.get(username = request.user)
            serializer = UserSerializer(user, data=request.data,partial=True)
            print(request.data)
            if serializer.is_valid():
                serializer.update(user, serializer.validated_data)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            data = {
                "error":"DoseNotExist",
                "error_message": "このユーザーは存在していません",
            }
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)



class CreateChangeEmailTicket(APIView):
    def exist_user(self,email):
        try:
            user = User.objects.get(email=email)
            raise AlreadyExists
        except User.DoesNotExist:
            pass
    def exist_preuser(self,email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise User.DoesNotExist

    
    def exist_change_email_ticket(self, email):
        try:
            change_email_ticket = ChangeEmailTicket.objects.get(email=email)
            change_email_ticket.delete()
        except ChangeEmailTicket.DoesNotExist:
            pass
    


    def post(self, request):
        # print(request)
        try:
            self.exist_user(request.data['email'])
            self.exist_preuser(request.data['previous_email'])
            self.exist_change_email_ticket(request.data['email'])
            serializer = ChangeEmailTicketSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                # from_mail = settings.EMAIL_HOST_USER
                # # raise ValidationError(from_mail)
                # send_mail('Subject here', 'Here is the message.', from_mail, ['kentaro.miyamoto1001@gmail.com'], fail_silently=False)
                change_email_ticket = ChangeEmailTicket.objects.get(email=request.data['email'])

                if change_email_ticket:
                    context = {"change_email_ticket": change_email_ticket}
                    to = [change_email_ticket.email]
                    ChangeEmailConfirmationEmail(self.request, context).send(to)

                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.data}, status=status.HTTP_400_BAD_REQUEST)
        except AlreadyExists:
            data = {
                "error":"AlreadyExists",
                "error_message": "そのメールアドレスは既に登録されています",
            }
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            data = {
                "error":"AlreadyExists",
                "error_message": "そのメールアドレスで登録されているユーザーが存在しません",
            }
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)


class CertificationChangeEmailTicket(APIView):
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        try:
            email = request.data['email']
            authentication_code = request.data['code']
            change_email_ticket = ChangeEmailTicket.objects.get(email=email)
            print("auth_code",authentication_code)
            confirm = change_email_ticket.confirm_code(authentication_code)
            if confirm=='Success':
                data = {
                    "email": change_email_ticket.email,
                }
                user = User.objects.get(email=change_email_ticket.previous_email)
                serializer = UserSerializer(user, data=data,partial=True)
                if serializer.is_valid():
                    serializer.update(user, serializer.validated_data)
                    return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

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

        except ChangeEmailTicket.DoesNotExist:
            # print('acount dose not exist')
            data = {
                "error":"DoesNotExist",
                "error_message": "このメールアドレスに確認コードを発送していません。",
            }
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)


class FollowingView(APIView):
    authentication_classes = [TokenAuthentication]
    
    def get(self, request, username ,format=None):
        try:
            # user = User.objects.get(username = request.user)
            user = User.objects.get(username = username)
            following = Following.objects.filter(follower = user.id)
            serializer = FollowingSerializer(following, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            data = {
                "error":"DoseNotExist",
                "error_message": "このユーザーは存在していません",
            }
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)
        except Following.DoesNotExist:
            data = {
                "error":"DoseNotExist",
                "error_message": "このユーザーは存在していません",
            }
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, username ,format=None):
        try:
            follower = User.objects.get(username = request.user)
            followed_user = User.objects.get(username = username)
            data = {
                'follower': follower.id,
                'followed_user': followed_user.id
            }
            serializer = FollowingSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            data = {
                "error":"DoseNotExist",
                "error_message": "このユーザーは存在していません",
            }
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)
        except Following.DoesNotExist:
            data = {
                "error":"DoseNotExist",
                "error_message": "このユーザーは存在していません",
            }
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,username, format=None):
        try:
            follower = User.objects.get(username = request.user)
            followed_user = User.objects.get(username = username)
            following = Following.objects.filter(follower=follower.id, followed_user=followed_user.id)
            following.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            data = {
                "error":"DoseNotExist",
                "error_message": "このユーザーは存在していません",
            }
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)
        except Following.DoesNotExist:
            data = {
                "error":"DoseNotExist",
                "error_message": "このユーザーは存在していません",
            }
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)








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