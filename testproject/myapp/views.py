from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseNotFound, Http404
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import os
import json
import datetime

from .models import User
from .forms import UserForm


def download_pdf(request: HttpRequest) -> HttpResponse:
    """Обработчик сохранения pdf-файла"""

    file_path = settings.MEDIA_ROOT / 'pdf' / 'sample.pdf'
    with open(file_path, 'rb') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=user_report_{datetime.date.today().strftime("%Y-%m-%d")}.pdf'
        return response


@csrf_exempt
def get_or_create_users(request: HttpRequest) -> HttpResponse:
    """Обработчик страницы пользователей"""

    users = User.objects.all()

    if request.method == 'GET':
        if 'format' in request.GET:
            if request.GET['format'] == 'json':
                json_response = []
                for user in users:
                    json_response.append({
                        'id': user.pk, 
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                    })
                return JsonResponse(json_response, safe=False)
            if request.GET['format'] == 'text':
                text_response = ''
                for user in users:
                    text_response += f'{user.pk}) {user.first_name} {user.last_name} ({user.email})\n'
                return HttpResponse(text_response, content_type='text/plain;charset=utf-8')
            
        context = {'users': users}
        return render(
            request=request,
            template_name='myapp/users.html',
            context=context,
        )
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.create(first_name=data['first_name'], last_name=data['last_name'], email=data['email'])
        data = {'id': user.pk} | data
        return JsonResponse(data, status=201)


def get_users_by_header(request: HttpRequest) -> HttpResponse:
    """Обработчик страницы получения пользователей в выбранном формате в зависимости от заголовка"""

    if 'Accept' in request.headers:
        users = User.objects.all()

        if request.headers['Accept'] == 'application/json':
            json_response = []
            for user in users:
                json_response.append({
                    'id': user.pk,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                })
            return JsonResponse(json_response, safe=False)
        elif request.headers['Accept'] == 'text/plain':
            text_response = ''
            for user in users:
                text_response += f'{user.pk}) {user.first_name} {user.last_name} ({user.email})\n'
            return HttpResponse(text_response, content_type='text/plain;charset=utf-8')
        
    return HttpResponseNotFound('Страницы с таким типом не существует!')
    # raise Http404('Страницы с таким типом не существует!')


@csrf_exempt
def get_or_update_or_delete_user(request: HttpRequest, user_id: int) -> HttpResponse:
    """Обработчик страницы изменения или удаления пользователей"""

    user = User.objects.get(pk=user_id)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            return redirect('users:get_or_create_users')
        else:
            context = {
                'user': user,
                'form': user_form,
            }
            return render(
                request=request,
                template_name='myapp/user.html',
                context=context
            )

    if request.method == 'GET':
        user_form = UserForm(instance=user)
        context = {
            'user': user,
            'form': user_form,
        }
        return render(
            request=request,
            template_name='myapp/user.html',
            context=context
        )

    if request.method == 'PATCH':
        data = {"id": user_id} | json.loads(request.body)

        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            user.email = data['email']

        user.save()
        return JsonResponse(data)
    
    if request.method == 'DELETE':
        try:
            user = User.objects.get(pk=user_id)
            user.delete()
        except User.DoesNotExist:
            user = None

        return HttpResponse(status=204)


