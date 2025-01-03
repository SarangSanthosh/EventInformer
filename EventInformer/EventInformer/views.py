from django.shortcuts import render

def homepage(request):
    return render(request, 'homepage.html')  # Renders homepage.html for the main page
