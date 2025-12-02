from django.shortcuts import render
from .forms import FeedbackForm
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from datetime import datetime 
from .models import Blog, Comment, Product, Order
from .forms import CommentForm, BlogForm, ProductForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import json




def custom_logout(request):
    logout(request)
    return redirect('index')

def index(request):
    return render(request, 'main/about.html') 

def about(request):
    return render(request, 'main/about.html')

def contacts(request):
    return render(request, 'main/contacts.html')

def links(request):
    return render(request, 'main/links.html')

def shop(request):
    products = Product.objects.all()
    return render(request, 'main/shop.html', {'products': products})

def services(request):
    return render(request, 'main/services.html')


def feedback_view(request):
    submitted = False
    data = {}

    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data  
            submitted = True  
            form = FeedbackForm() 
            return render(request, "main/poolreq.html", {"data": data})
 
    else:
        form = FeedbackForm()

    return render(request, "main/pool.html", {"form": form, "submitted": submitted, "data": data})

def registration(request):
    assert isinstance(request, HttpRequest)
    if request.method == "POST": # проверка на отправку формы
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False  
            reg_f.is_active = True  
            reg_f.is_superuser = False  
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()
            reg_f.save()
            return redirect('about')  
    else:
        regform = UserCreationForm() # создание объекта формы
    return render(
        request,
        'main/registration.html',
        {
            'regform': regform,
            'year': datetime.now().year,
        }
    )
def blog(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest) # выполняет проверку типа объекта request во время выполнения программы.
    posts = Blog.objects.all()  
    return render(
        request,
        'main/blog.html',  
        {
            'title': 'Блог',
            'posts': posts,  # Передача 
            'year': datetime.now().year,
        }
    )

def blogpost(request, parametr):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr)  
    comments = Comment.objects.filter(post=parametr)  

    if request.method == "POST":  
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user  
            comment_f.date = datetime.now()  
            comment_f.post = Blog.objects.get(id=parametr) 
            comment_f.save()  
            return redirect('blogpost', parametr=post_1.id)  
    else:
        form = CommentForm()  

    return render(
        request,
        'main/blogpost.html',
        {
            'post_1': post_1,
            'comments': comments,  # Передача 
            'form': form, 
            'year': datetime.now().year,
        }
    )


def newpost(request):
    if not request.user.is_superuser:  # Доступ только для администратора
        return redirect('blog')
    
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)  # Обрабатываем POST и файлы
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Устанавливаем автора
            post.save()
            return redirect('blog')  # Перенаправляем на страницу блога
    else:
        form = BlogForm()
    
    return render(request, 'main/newpost.html', {'form': form})


def add_product(request):
    if not request.user.is_superuser:  # Доступ только для администратора
        return redirect('shop')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # Обрабатываем POST и файлы
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('shop')  # Перенаправляем на страницу магазина
    else:
        form = ProductForm()
    
    return render(request, 'main/newshop.html', {'form': form})

def videopost(request):
    """Renders the videopost page."""
    return render(request, 'main/videopost.html')


def get_cart(request):
    """Получить корзину из сессии"""
    if 'cart' not in request.session:
        request.session['cart'] = {}
    return request.session['cart']


@require_http_methods(["POST"])
def add_to_cart(request):
    """Добавить товар в корзину"""
    try:
        data = json.loads(request.body)
        product_id = str(data.get('product_id'))
        
        if not product_id:
            return JsonResponse({'error': 'Product ID required'}, status=400)
        
        # Проверим, что товар существует
        try:
            product = Product.objects.get(id=int(product_id))
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        
        cart = get_cart(request)
        
        if product_id in cart:
            cart[product_id]['quantity'] += 1
        else:
            cart[product_id] = {
                'quantity': 1,
                'title': product.title,
                'price': float(product.price)
            }
        
        request.session['cart'] = cart
        request.session.modified = True
        
        return JsonResponse({
            'success': True,
            'message': f'{product.title} добавлен в корзину',
            'cart_count': sum(item['quantity'] for item in cart.values())
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)


def cart(request):
    """Отобразить страницу корзины"""
    cart_items = get_cart(request)
    products_in_cart = []
    total_price = 0
    
    for product_id, item in cart_items.items():
        try:
            product = Product.objects.get(id=int(product_id))
            item_total = item['price'] * item['quantity']
            products_in_cart.append({
                'id': product_id,
                'product': product,
                'quantity': item['quantity'],
                'price': item['price'],
                'total': item_total
            })
            total_price += item_total
        except Product.DoesNotExist:
            # Удалим товар, который больше не существует
            del cart_items[product_id]
            request.session['cart'] = cart_items
            request.session.modified = True
    
    return render(request, 'main/cart.html', {
        'cart_items': products_in_cart,
        'total_price': total_price
    })


@require_http_methods(["POST"])
def update_cart_item(request):
    """Изменить количество товара в корзине"""
    try:
        data = json.loads(request.body)
        product_id = str(data.get('product_id'))
        quantity = int(data.get('quantity', 1))
        
        if quantity < 1:
            return JsonResponse({'error': 'Quantity must be at least 1'}, status=400)
        
        cart = get_cart(request)
        
        if product_id in cart:
            cart[product_id]['quantity'] = quantity
            request.session['cart'] = cart
            request.session.modified = True
            
            item_total = cart[product_id]['price'] * quantity
            total_price = sum(item['price'] * item['quantity'] for item in cart.values())
            
            return JsonResponse({
                'success': True,
                'item_total': item_total,
                'total_price': total_price
            })
        else:
            return JsonResponse({'error': 'Product not in cart'}, status=404)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Invalid request'}, status=400)


@require_http_methods(["POST"])
def remove_from_cart(request):
    """Удалить товар из корзины"""
    try:
        data = json.loads(request.body)
        product_id = str(data.get('product_id'))
        
        cart = get_cart(request)
        
        if product_id in cart:
            del cart[product_id]
            request.session['cart'] = cart
            request.session.modified = True
            
            total_price = sum(item['price'] * item['quantity'] for item in cart.values())
            
            return JsonResponse({
                'success': True,
                'total_price': total_price,
                'cart_count': sum(item['quantity'] for item in cart.values())
            })
        else:
            return JsonResponse({'error': 'Product not in cart'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)


@login_required(login_url='login')
def checkout(request):
    """Оформление заказа"""
    cart_items = get_cart(request)
    
    if not cart_items:
        return redirect('cart')
    
    # Рассчитываем общую сумму и подготавливаем товары для шаблона
    total_price = 0
    items_for_template = []
    
    for product_id, item in cart_items.items():
        item_total = item['price'] * item['quantity']
        total_price += item_total
        items_for_template.append({
            'id': product_id,
            'title': item['title'],
            'price': item['price'],
            'quantity': item['quantity'],
            'total': item_total
        })
    
    # Создаём заказ
    order = Order.objects.create(
        user=request.user,
        order_data=dict(cart_items),
        total_price=total_price,
        status='processing'
    )
    
    # Очищаем корзину
    request.session['cart'] = {}
    request.session.modified = True
    
    return render(request, 'main/order_confirmation.html', {
        'order': order,
        'cart_items': items_for_template
    })


@login_required(login_url='login')
def my_orders(request):
    """Просмотр заказов пользователя"""
    orders = Order.objects.filter(user=request.user).order_by('-created')
    
    return render(request, 'main/my_orders.html', {
        'orders': orders
    })


def admin_orders(request):
    """Просмотр всех заказов для администратора"""
    if not request.user.is_superuser:
        return redirect('shop')
    
    orders = Order.objects.all().order_by('-created')
    
    return render(request, 'main/admin_orders.html', {
        'orders': orders
    })


@require_http_methods(["POST"])
def update_order_status(request):
    """Изменение статуса заказа"""
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')
        new_status = data.get('status')
        
        try:
            order = Order.objects.get(id=order_id)
            order.status = new_status
            order.save()
            
            return JsonResponse({
                'success': True,
                'status': order.get_status_display()
            })
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)