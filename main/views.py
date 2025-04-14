from django.shortcuts import render
from .forms import FeedbackForm
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from datetime import datetime  # Добавляем импорт
from .models import Blog

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
    return render(request, 'main/shop.html')

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
    assert isinstance(request, HttpRequest)
    posts = Blog.objects.all()  # Запрос на выбор всех статей
    return render(
        request,
        'main/blog.html',  # Путь к шаблону
        {
            'title': 'Блог',
            'posts': posts,  # Передача списка статей
            'year': datetime.now().year,
        }
    )

def blogpost(request, parametr):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr)  # Запрос на выбор статьи по ID
    return render(
        request,
        'main/blogpost.html',
        {
            'post_1': post_1,  # Передача статьи
            'year': datetime.now().year,
        }
    )