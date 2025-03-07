# django_app/urls.py

from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

def hello_name(request):
    """
    A simple view that returns 'Hello, {name}, age : {age} ' in JSON format.
    Uses query parameters named 'name' and age
    """
    # Get 'name' from the query string, default to 'World' if missing
    # Get age from the query string, default to Unknown
    name = request.GET.get("name", "World")
    age = request.GET.get("age","Unknown")
    return JsonResponse({"message": f"Hello, {name}!" , "age": age })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_name), 
    # Example usage: /hello/?name=BOB&age=20
    # returns {"message":"Hello, BOB!","age":"20"}
]
