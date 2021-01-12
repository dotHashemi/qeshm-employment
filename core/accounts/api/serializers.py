from enum import unique
import random

from django.core.validators import MaxLengthValidator, RegexValidator
from accounts.models import Account, Verify
from rest_framework import fields, serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator


class RegistrationSerializer(serializers.ModelSerializer):
    # this field will use to store phone
    username = serializers.CharField(validators=[
        RegexValidator(regex=r"^(09)[0-9]{9}$", message="phone is not valid.")
    ])
    email = serializers.EmailField(validators=[
        UniqueValidator(queryset=User.objects.all())
    ])
    password = serializers.CharField(write_only=True)
    confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm']

    def create(self):
        thisPassword = self.validated_data.get('password')
        thisConfirm = self.validated_data.get('confirm')
        thisEmail = self.validated_data.get('email')
        thisUsername = self.validated_data.get('username')
        thisType = "employer"

        if thisPassword != thisConfirm:
            raise serializers.ValidationError(
                {'password': 'passwords must match.'})

        user = User(email=thisEmail, username=thisUsername)
        user.set_password(thisPassword)
        user.save()

        Account.objects.create(user=user, type=thisType)

        code = random.randint(10000, 99999)
        Verify.objects.create(phone=thisUsername, type="register", code=code)

        return {
            "phone": thisUsername,
            "code": code
        }


class VerifySerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=11, min_length=11)

    class Meta:
        model = Verify
        fields = ['type', 'phone', 'code']

    def check(self):
        thisPhone = self.validated_data['phone']
        thisCode = self.validated_data['code']
        thisType = self.validated_data['type']
        verify = Verify.objects.filter(phone=thisPhone).first()

        if verify and verify.code == thisCode and verify.type == thisType:
            Account.objects.filter(phone=thisPhone).update(isVerified=True)
            verify.delete()
            return True
        else:
            return False
