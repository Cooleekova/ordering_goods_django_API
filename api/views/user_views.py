from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render, redirect

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, viewsets

from api.forms import RegistrationForm, ConfirmAccountForm
from api.models import Contact, ConfirmEmailToken, User
from api.serializers import UserSerializer, ContactSerializer

from api.tasks import new_user_registered_email


class RegisterAccount(APIView):
    """
    Для регистрации покупателей
    """

    def get(self, request, *args, **kwargs):
        context = {}
        form = RegistrationForm()
        context['registration_form'] = form
        return render(request, 'api/signup.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user.id)
            new_user_registered_email.delay(
                token=token.key,
                subject=f"Password Token for {token.user.email}",
                recipient_list=token.user.email,
            )
            login(request, user)
            return redirect('/api/v1/user/register/confirm')
        else:
            context['registration_form'] = form
            return render(request, 'api/signup.html', context)


class ConfirmAccount(APIView):
    """
    Класс для подтверждения почтового адреса
    """
    def get(self, request, *args, **kwargs):
        return render(request, 'api/confirm-account.html')

    # Отправка данных методом POST
    def post(self, request, *args, **kwargs):
        context = {}
        form = ConfirmAccountForm(request.POST)

        # проверяем обязательные аргументы
        if {'email', 'token'}.issubset(request.data):

            token = ConfirmEmailToken.objects.filter(user__email=request.data['email'],
                                                     key=request.data['token']).first()
            if token:
                token.user.is_active = True
                token.user.save()
                token.delete()
                return redirect('/api/v1/products/')
            else:
                context['errors'] = form.errors
                return Response(form.errors)

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class AccountDetailsViewSet(viewsets.ModelViewSet):
    """
    Класс для работы c данными пользователя
    """

    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        """Админы могут получать все заказы, остальное пользователи только свои."""
        return User.objects.filter(id=self.request.user.id)


class ContactViewSet(viewsets.ModelViewSet):
    """
    Класс для работы с контактами покупателей
    """

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['user'] = request.user

        new_contact = Contact.objects.create(
            city=request.data['city'],
            street=request.data['street'],
            phone=request.data['phone'],
            user=request.data['user'],
        )
        new_contact.save()
        serializer = ContactSerializer(new_contact)
        return Response(serializer.data)

