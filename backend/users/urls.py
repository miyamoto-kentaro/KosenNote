from django.conf import settings
from django.urls import path, include

from . import views

urlpatterns = [
    # emailでユーザーを作成するAPI
    # 仮登録をするAPI
    path('email/pre_register/create', views.CreatePreRegister.as_view()),
    # 仮登録を認証してユーザーを作るAPI
    path('email/pre_register/certification', views.CertificationPreRegister.as_view()),

    # メールアドレスの仮変更
    path('email/change_email_ticket/create', views.CreateChangeEmailTicket.as_view()),
    # メルアドの変更認証
    path('email/update/certification', views.CertificationChangeEmailTicket.as_view()),

    # User情報を取得
    path('me', views.UpdateUser.as_view()),
    path('update/', views.UpdateUser.as_view()),

    # emailとusernameでUserを検索して、重複を確認するAPI
    path('already_exists/email', views.UserEmailAlreadyExists.as_view()),
    path('already_exists/username', views.UserNameAlreadyExists.as_view()),
    path('dosenot_exists/email', views.UserEmailDoesNotExist.as_view()),
    path('dosenot_exists/username', views.UserNameDoesNotExist.as_view()),
]
