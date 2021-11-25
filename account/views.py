from rest_framework import viewsets
from rest_framework import permissions

from account.models import Account
from account.permissions import AccountPermission
from account.serializers import AccountSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    permission_classes = [AccountPermission]
