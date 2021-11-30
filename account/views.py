from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from account.models import Account
from account.permissions import AccountPermission
from account.serializers import AccountSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    permission_classes = [AccountPermission]

    @action(methods=['post'], detail=True)
    def follow(self, request, pk=None):
        user = request.user
        account_to_follow = self.get_object()
        if user == account_to_follow:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': 'You cannot follow yourself'})
        account_to_follow.followers.add(user)
        return Response(status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def unfollow(self, request, pk=None):
        user = request.user
        account_to_unfollow = self.get_object()
        if user == account_to_unfollow:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': 'You cannot unfollow yourself'})
        account_to_unfollow.followers.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True, url_path='followers')
    def get_followers(self, request, pk=None):
        queryset = self.get_object().followers.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, url_path='following')
    def get_following(self, request, pk=None):
        queryset = Account.objects.filter(followers=self.get_object())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='me')
    def get_me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
