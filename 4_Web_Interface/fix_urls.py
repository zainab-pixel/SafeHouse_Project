import os

# The specific path from your error message
file_path = r"C:\Users\zaina\SafeHouse_Project\4_Web_Interface\safehouse_project\urls.py"

# The correct content (without the bad line)
new_content = """from django.contrib import admin
from django.urls import path
from dashboard import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('api/login/', views.api_login, name='api_login'),
    path('api/register/', views.api_register, name='api_register'),
    path('api/set_state/', views.set_state, name='set_state'),
]
"""

try:
    with open(file_path, "w") as f:
        f.write(new_content)
    print("✅ SUCCESS: The file urls.py has been forcibly updated!")
except FileNotFoundError:
    print(f"❌ ERROR: Could not find file at {file_path}")