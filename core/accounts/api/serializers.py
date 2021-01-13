from core.helpers import Compare, Error
from django.utils import timezone
import random

from django.core.validators import MaxLengthValidator, RegexValidator
from accounts.models import Account, Verify
from rest_framework import fields, serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from core.exceptions import DoesNotMatch, DoesNotVerify


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[
        RegexValidator(regex=r"^(09)[0-9]{9}$", message="phone is not valid.")
    ])
    email = serializers.EmailField(validators=[
        UniqueValidator(queryset=User.objects.all())
    ], required=False)
    password = serializers.CharField(write_only=True)
    confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm']

    def create(self):
        """ ...........................
            create new user and account
            ...........................
        """
        username = self.validated_data.get('username')
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        confirm = self.validated_data.get('confirm')
        type = "employer"

        try:
            verify = Verify.objects.get(phone=username)

            if not verify.isVerified or verify.type != "register" or not Compare.verifyTime(verify.created, 30):
                raise DoesNotVerify

            if password != confirm:
                raise DoesNotMatch

            user = User(email=email, username=username)
            user.set_password(password)
            user.save()
            Account.objects.create(user=user, type=type)
            verify.delete()

            return user

        except Verify.DoesNotExist:
            raise serializers.ValidationError(
                {'phone': 'phone does not exists.'}
            )
        except DoesNotVerify:
            raise serializers.ValidationError(
                {'phone': 'phone does not verified.'}
            )
        except DoesNotMatch:
            raise serializers.ValidationError(
                {'password': 'passwords must match.'}
            )

    def changePassword(self):
        """ ..........................
            change the user's password
            ..........................
        """
        phone = self.validated_data.get("username")
        password = self.validated_data.get("password")
        confirm = self.validated_data.get("confirm")

        try:
            verify = Verify.objects.get(phone=phone)

            if not verify.isVerified or verify.type != "resetpass" or not Compare.verifyTime(verify.created, 30):
                raise DoesNotVerify

            if password != confirm:
                raise DoesNotMatch

            user = User.objects.get(username=phone)
            user.set_password(password)
            user.save()
            verify.delete()

            return user

        except User.DoesNotExist:
            raise serializers.ValidationError(
                {'user': 'user does not exists.'}
            )

        except Verify.DoesNotExist or DoesNotVerify:
            raise serializers.ValidationError(
                {'phone': 'phone does not verified.'}
            )

        except DoesNotMatch:
            raise serializers.ValidationError(
                {'password': 'passwords must match.'}
            )


class VerifySerializer(serializers.ModelSerializer):
    phone = serializers.CharField(validators=[
        RegexValidator(regex=r"^(09)[0-9]{9}$", message="phone is not valid.")
    ])

    class Meta:
        model = Verify
        fields = ['type', 'phone', 'code']

    def validate_type(self, value):
        if value == "register" or value == "resetpass":
            return value
        raise serializers.ValidationError({"type": "type is not valid."})

    def verified(self):
        """ .................................................................
            check the code when if it's true then assign as a verified number
            .................................................................
        """
        phone = self.validated_data.get('phone')
        code = self.validated_data.get('code')
        type = self.validated_data.get('type')

        verify = Verify.objects.filter(phone=phone).first()

        if verify and verify.code == code and verify.type == type and Compare.verifyTime(verify.created):
            verify.isVerified = True
            verify.save()

        return verify
