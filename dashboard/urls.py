from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('contact_us/', views.contact_view, name='contact'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('my_account/', views.my_account, name='my_account'),
    path('about/', views.about, name='about'),
    path('change_password/', views.change_password, name='change_password'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('app/', views.your_view_name, name='app'),
    path('messages/', views.messages_view, name='messages'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about/', views.about, name='about'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
  
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('my_account/', views.my_account, name='my_account'),
    path('report/', views.report, name='report'),
    path('recommend_crop/', views.recommend_crop, name='recommend_crop'), 
    path('recommend_crop/home/', views.home, name='recommend_crop_home'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin_user_messages/', views.admin_user_messages, name='admin_user_messages'),
    path('chatbot/', include('chatbot.urls')),

]
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('my_account/', views.my_account, name='my_account'),
]
from django.urls import path
from .views import register

urlpatterns = [
    path('register/', register, name='register'),
    # Add other URL patterns here
]
from django.urls import path
from .views import register

urlpatterns = [
    path('register/', register, name='register'),
    # other paths...
]
from django.urls import path
from .views import user_logout

urlpatterns = [
    # Other URL patterns
    path('logout/', user_logout, name='logout'),  # URL for logging out
    path('logout_page/', TemplateView.as_view(template_name='logout.html'), name='logout_page'),  # URL for logout page
]
from django.urls import path
from .views import user_logout, LogoutPage

urlpatterns = [
    # Other URL patterns...
    path('logout/', user_logout, name='logout'),  # URL for logging out
    path('logout_page/', LogoutPage.as_view(), name='logout_page'),  # URL for logout page
]
from django.urls import path
from .views import logout_view

urlpatterns = [
    # other paths
    path('logout/', logout_view, name='logout'),
]
from django.urls import path, include

urlpatterns = [
    # ... other urls
    path('chatbot/', include('chatbot.urls')),
]
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # other paths...
    path('chatbot/', include('chatbot.urls')),  # This line should be included




]
