from django.shortcuts import render

# Create your views here.
def home(request):
    if request.method == 'GET':
        return render(request, 'home/home.html')

def aboutus(request):
    if request.method == 'GET':
        return render(request, 'home/aboutus.html')

def contact(request):
    if request.method == 'GET':
        return render(request, 'home/contactus.html')