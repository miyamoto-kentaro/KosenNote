from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from templated_mail.mail import BaseEmailMessage


from djoser import utils
from djoser.conf import settings as djoser_setting


# class ActivationEmail(BaseEmailMessage):
#     template_name = "email/activation.html"

#     def get_context_data(self):
#         # ActivationEmail can be deleted
#         context = super().get_context_data()

#         user = context.get("user")
#         context["uid"] = utils.encode_uid(user.pk)
#         context["token"] = default_token_generator.make_token(user)
#         context["url"] = settings.ACTIVATION_URL.format(**context)
#         return context


# class ConfirmationEmail(BaseEmailMessage):
#     template_name = "email/confirmation.html"
class ConfirmationEmail(BaseEmailMessage):
    template_name = "email/confirmation_email.html"

    def get_context_data(self):
        # PasswordResetEmail can be deleted
        context = super().get_context_data()

        pre_register = context.get("pre_register")
        frontend_host = settings.EMAIL_FRONTEND_HOST
        context["frontend_host"] = frontend_host
        context["email"] = pre_register.email
        context["code"] = pre_register.authentication_code
        return context


class PasswordResetEmail(BaseEmailMessage):
    template_name = "email/custom_password_reset.html"

    def get_context_data(self):
        # PasswordResetEmail can be deleted
        context = super().get_context_data()

        frontend_host = settings.EMAIL_FRONTEND_HOST
        user = context.get("user")
        context["frontend_host"] = frontend_host
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = djoser_setting.PASSWORD_RESET_CONFIRM_URL.format(**context)
        return context

# class PasswordResetEmail(BaseEmailMessage):
#     template_name = "email/custom_password_reset.html"

#     def get_context_data(self):
#         # PasswordResetEmail can be deleted
#         context = super().get_context_data()

#         frontend_host = settings.EMAIL_FRONTEND_HOST
#         user = context.get("user")
#         context["frontend_host"] = frontend_host
#         context["uid"] = utils.encode_uid(user.pk)
#         context["token"] = default_token_generator.make_token(user)
#         context["url"] = djoser_setting.PASSWORD_RESET_CONFIRM_URL.format(**context)
        # return context


# class PasswordChangedConfirmationEmail(BaseEmailMessage):
#     template_name = "email/password_changed_confirmation.html"


# class UsernameChangedConfirmationEmail(BaseEmailMessage):
#     template_name = "email/username_changed_confirmation.html"


# class UsernameResetEmail(BaseEmailMessage):
#     template_name = "email/username_reset.html"

#     def get_context_data(self):
#         context = super().get_context_data()

#         user = context.get("user")
#         context["uid"] = utils.encode_uid(user.pk)
#         context["token"] = default_token_generator.make_token(user)
#         context["url"] = settings.USERNAME_RESET_CONFIRM_URL.format(**context)
#         return context