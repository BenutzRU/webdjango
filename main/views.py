from django.shortcuts import render

def index(request):
    return render(request, 'main/about.html')  # Главная страница

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
