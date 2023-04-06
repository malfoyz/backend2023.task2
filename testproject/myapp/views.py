from django.shortcuts import render
from django.urls import reverse
from django.http import (
    HttpRequest, 
    HttpResponse, 
    JsonResponse, 
    HttpResponseNotFound, 
    Http404, 
    HttpResponseRedirect,
)
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

from .models import *
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

    if request.method == 'POST':
        user = User.objects.get(pk=user_id)
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
        user = User.objects.get(pk=user_id)
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
        user = User.objects.get(pk=user_id)
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
    

def get_products(request: HttpRequest) -> HttpResponse:
    """Обработчик страницы с продуктами"""

    products = Product.objects.all()
    context = {
        'products': products,
        'title': 'Список продуктов',
    }

    return render(
        request=request,
        template_name='myapp/products.html',
        context=context,
    )


def add_to_cart(request: HttpRequest, product_id: int) -> HttpResponse:
    """Обработчик добавления товара в корзину с помощью куки"""

    cart = request.COOKIES.get('cart')

    if not cart:
        cart = {}
    else:
        cart = json.loads(cart)
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    response = HttpResponseRedirect(reverse('myapp:get_products'))
    response.set_cookie('cart', json.dumps(cart))
    return response


# def add_to_cart(request: HttpRequest, product_id: int) -> HttpResponse:
#     """Обработчик добавления товара в корзину с помощью сессии"""

#     cart = request.session.get('cart', {})

#     if str(product_id) in cart:
#         cart[str(product_id)] += 1
#     else:
#         cart[str(product_id)] = 1

#     request.session['cart'] = cart
#     return redirect('myapp:get_products')


def remove_from_cart(request: HttpRequest, product_id: int) -> HttpResponse:
    """Обработчик удаления товара из корзины с помощью куки"""
    
    cart = request.COOKIES.get('cart')
    if cart:
        cart = json.loads(cart)
        if str(product_id) in cart:
            del cart[str(product_id)]
            response = HttpResponseRedirect(reverse('myapp:get_cart'))
            response.set_cookie('cart', json.dumps(cart))
            return response
    return HttpResponse(status=204)


# def remove_from_cart(request: HttpRequest, product_id: int) -> HttpResponse:
#     """Обработчик удаления товара из корзины с помощью сессии"""

#     cart = request.session.get('cart', {})
#     if str(product_id) in cart:
#         del cart[str(product_id)]
#         request.session['cart'] = cart
#     return redirect('myapp:get_cart')


def get_cart(request: HttpRequest) -> HttpResponse:
    """Обработчик страницы с корзиной с помощью куки"""

    cart = request.COOKIES.get('cart')
    if cart:
        cart = json.loads(cart)
    else:
        cart = {}

    products_ids = cart.keys()
    products = Product.objects.filter(pk__in=products_ids)
    products_dicts = []
    for product in products:
        products_dicts.append({
            'id': product.pk,
            'name': product.name,
            'price': float(product.price) * cart[str(product.pk)],
            'image': product.image,
            'quantity': cart[str(product.pk)]
        })

    context = {
        'products': products_dicts,
        'title': 'Корзина',
    }

    return render(
        request=request,
        template_name='myapp/cart.html',
        context=context,
    )


def get_cart(request: HttpRequest) -> HttpResponse:
    """Обработчик страницы с корзиной с помощью сессии"""

    cart = request.session.get('cart', {})
    products_ids = cart.keys()
    products = Product.objects.filter(pk__in=products_ids)
    products_dicts = []

    for product in products:
        products_dicts.append({
            'id': product.pk,
            'name': product.name,
            'price': float(product.price) * cart[str(product.pk)],
            'image': product.image,
            'quantity': cart[str(product.pk)]
        })
    context = {
        'products': products_dicts,
        'title': 'Корзина',
    }

    return render(
        request=request,
        template_name='myapp/cart.html',
        context=context,
    )