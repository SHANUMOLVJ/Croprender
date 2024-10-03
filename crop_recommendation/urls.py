from django.contrib import admin
from django.urls import path,include
from dashboard import views  # Assuming dashboard app has all views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about/', views.about, name='about'),
    path('home/', views.home, name='home'),  # Home URL, accessed by /home/
    path('profile/', views.profile, name='profile'),
    path('contact_us/', views.contact_view, name='contact_us'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('my_account/', views.my_account, name='my_account'),
    path('', views.home, name='home'),  
    path('report/', views.report, name='report'), 
    path('recommend_crop/', views.recommend_crop, name='recommend_crop'),
    path('upload/', views.upload_view, name='upload'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage_users/', views.Manage_user, name='manage_users'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin_user_messages/', views.admin_user_messages, name='admin_user_messages'),
    path('chatbot/', include('chatbot.urls')),


    path('crop/<int:crop_id>/', views.crop_detail, name='crop_detail'),
    path('purchase/<int:crop_id>/', views.purchase_crop, name='purchase_crop'),
    path('confirm_purchase/', views.confirm_purchase, name='confirm_purchase'),
    path('purchase_success/', views.purchase_success, name='purchase_success'),
    path('add_crop/', views.add_crop, name='add_crop'),
    path('manage_crops/', views.manage_crops, name='manage_crops'),
    path('edit_crop/<int:crop_id>/', views.edit_crop, name='edit_crop'),
    path('delete_crop/<int:crop_id>/', views.delete_crop, name='delete_crop'),
    path('add-to-cart/<int:crop_id>/', views.add_to_cart, name='add_to_cart'),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('purchase_all/', views.purchase_all_crops, name='purchase_all_crops'),
    path('feedback/', views.feedback_list_view, name='feedback_admin'),
    path('feedback/delete/<int:id>/', views.delete_feedback_view, name='delete_feedback'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
