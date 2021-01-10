from enum import unique
import random

from django.core.validators import MaxLengthValidator
from accounts.models import Account, Verify
from rest_framework import fields, serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator


# CUSTOM VALIDATIORS
def SizeValidator(value, length):
    if len(str(value)) != length:
        raise serializers.ValidationError(
            "%s is not %d character." % (str(value), length)
        )
    return value


class RegistrationSerializer(serializers.ModelSerializer):
    confirm = serializers.CharField(write_only=True)
    email = serializers.EmailField(validators=[
        UniqueValidator(queryset=User.objects.all())
    ])
    phone = serializers.CharField(min_length=11, max_length=11, validators=[
        UniqueValidator(Account.objects.all())
    ])
    type = serializers.CharField(validators=[
        MaxLengthValidator(10),
    ])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm', 'phone', 'type']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self):
        thisPassword = self.validated_data['password']
        thisConfirm = self.validated_data['confirm']
        thisEmail = self.validated_data['email']
        thisUsername = self.validated_data['username']
        thisPhone = self.validated_data['phone']
        thisType = self.validated_data['type']

        if thisPassword != thisConfirm:
            raise serializers.ValidationError(
                {'password': 'Passwords must match.'})

        user = User(email=thisEmail, username=thisUsername)
        user.set_password(thisPassword)
        user.save()

        Account.objects.create(user=user, phone=thisPhone, type=thisType)

        code = random.randint(10000, 99999)
        Verify.objects.create(phone=thisPhone, type="register", code=code)

        return {
            "phone": thisPhone,
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
            if verify.type == 'register':
                verify.delete()
            return True
        else:
            return False
