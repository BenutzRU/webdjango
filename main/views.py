from django.shortcuts import render
from .forms import FeedbackForm
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from datetime import datetime 
from .models import Blog, Comment, Product
from .forms import CommentForm, BlogForm, ProductForm
from django.shortcuts import render




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