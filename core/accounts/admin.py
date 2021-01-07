from django.contrib import admin
from .models import Account, Verify


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass


@admin.register(Verify)
class VerifyAdmin(admin.ModelAdmin):
    pass