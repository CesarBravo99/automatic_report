from django.shortcuts import render

def tutorial(request):
    return render(request, 'tutorial.html')