from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .serializer import MyProfileSerializer, LoginSerializer, RegisterSerializer, AccountUpdateSerializer, MyHistoryJobSerializer
from .models import Account, MyHistoryJob
from account.permissons import IsOwnerReadOnly


class AccountRegisterView(generics.GenericAPIView):
    # http://127.0.0.1.8000/account/api/register
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data  # user data da keladi malumotlari
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True, 'data': "Account successfully created"}, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    # http://127.0.0.1.8000/account/api/login
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"tokens": serializer.data['tokens']}, status=status.HTTP_200_OK)


class AccountRU(generics.RetrieveUpdateAPIView):
    serializer_class = AccountUpdateSerializer
    queryset = Account.objects.all()
    permission_classes = [IsOwnerReadOnly, IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query = self.get_object()
        if query:
            serializer = self.serializer_class(query)
            return Response({"success": True, 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': 'query did not exit'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({"success": False, 'message': "credentials is invalid"}, status=status.HTTP_404_NOT_FOUND)


class MyProfileList(generics.ListAPIView):
    serializer_class = MyProfileSerializer
    queryset = Account.objects.all()
    permission_classes = [IsOwnerReadOnly]


class MyHistoryJobListCreate(generics.ListCreateAPIView):
    queryset = MyHistoryJob.objects.all()
    serializer_class = MyHistoryJobSerializer
    permission_classes = (IsAuthenticated, IsOwnerReadOnly)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['author'] = self.request.user
        return ctx
