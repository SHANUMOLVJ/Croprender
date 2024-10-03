from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .forms import UserRegisterForm, UserUpdateForm, CustomUserCreationForm
from .models import CropPrediction  # Ensure this model is defined in models.py

def home(request):
    crops = Crop.objects.all()  # Fetching crops, adjust as needed
    cart_count = request.session.get('cart_count', 0)  # Adjust this according to your cart logic
    return render(request, 'home.html', {
        'crops': crops,
        'cart_count': cart_count,
    })

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user instance
            phone = form.cleaned_data.get('phone')  # Get the phone number
            Profile.objects.create(user=user, phone=phone)  # Create a Profile instance
            messages.success(request, f'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

# Login view
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')  # Redirect to the dashboard after login
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout view
@login_required
def logout_view(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('login')

# Dashboard view
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# Profile view
@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

# Change password view
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Keep user logged in after password change
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})

# Report view
@login_required
def generate_report(request):
    user = request.user
    try:
        prediction = CropPrediction.objects.get(user=user)
    except CropPrediction.DoesNotExist:
        return HttpResponse("No prediction data found for this user.")

    context = {
        'user_name': user.username,
        'nitrogen': prediction.nitrogen,
        'phosphorus': prediction.phosphorus,
        'potassium': prediction.potassium,
        'temperature': prediction.temperature,
        'humidity': prediction.humidity,
        'pH_value': prediction.pH_value,
        'rainfall': prediction.rainfall,
        'recommended_crop': prediction.recommended_crop,
        'additional_insights': prediction.additional_insights,
    }

    return render(request, 'report.html', context)

def report(request):
    # Your logic here
    return render(request, 'report.html')

   
# About view
def about(request):
    return render(request, 'about.html')



# Edit Profile view
@login_required
def edit_profile(request):
    return render(request, 'edit_profile.html')

# My Account view
@login_required
def my_account(request):
    return render(request, 'my_account.html')
# crop_recommendation/dashboard/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'home.html', {'form': form})
# In your views.py
from django.shortcuts import render

def about(request):
    return render(request, 'about.html')
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to dashboard page
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CropRecommendation  # Make sure to import your model
from django.contrib.auth.decorators import login_required
import json

@csrf_exempt
@login_required  # Ensure the user is logged in
def recommend_crop(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Extract data
            nitrogen = data.get('Nitrogen')
            phosphorus = data.get('Phosphorus')
            potassium = data.get('Potassium')
            temperature = data.get('Temperature')
            rainfall = data.get('Rainfall')
            ph_value = data.get('pH')
            humidity = data.get('Humidity')

            # Placeholder recommendation logic
            recommended_crop = recommend_crop_logic(nitrogen, phosphorus, potassium, temperature, rainfall, ph_value, humidity)

            # Save the recommendation to the database
            recommendation = CropRecommendation(
                nitrogen=nitrogen,
                phosphorus=phosphorus,
                potassium=potassium,
                temperature=temperature,
                humidity=humidity,
                ph_value=ph_value,
                rainfall=rainfall,
                user=request.user  # Save the logged-in user
            )
            recommendation.save()

            return JsonResponse({'crop': recommended_crop})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def recommend_crop_logic(nitrogen, phosphorus, potassium, temperature, rainfall, ph_value, humidity):
    # Replace this with your actual recommendation logic
    crop = "Wheat"  # Default crop recommendation

    # Example recommendation logic based on input parameters
    if nitrogen > 50 and ph_value > 7 and temperature > 20 and humidity > 60:
        crop = "Rice"
    # Add other conditions as needed...

    return crop

from django.shortcuts import render

def recommend_crop(request):
    return render(request, 'recommend_crop.html')

from django.shortcuts import render

def upload_view(request):
    return render(request, 'upload.html')
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if the entered credentials match the static admin credentials
        if username == 'admin' and password == 'admin@123':
            # Try to retrieve the admin user from the database
            user, created = User.objects.get_or_create(username='admin', is_staff=True, is_superuser=True)
            
            if created:
                # Set a default password for the admin user if it doesn't exist
                user.set_password('admin@123')
                user.save()

            login(request, user)  # Log in the admin user
            return redirect('admin_dashboard')  # Redirect to the admin dashboard
        else:
            return render(request, 'admin_login.html', {'error': 'Invalid login credentials'})

    return render(request, 'admin_login.html')

    
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Crop, Purchase
from django.db.models import Sum
# def admin_dashboard(request):
#     users = User.objects.all()
#     profiles = Profile.objects.all()  # Optional if you want to display profile data too
#     return render(request, 'admin_dashboard.html', {'users': users, 'profiles': profiles})

def admin_dashboard(request):
    total_users = User.objects.count()
    total_crops = Crop.objects.count()
    most_purchased_products = Purchase.objects.values('crop__name').annotate(total_purchases=Sum('quantity')).order_by('-total_purchases')[:5]  # Top 5 most purchased crops

    context = {
        'total_users': total_users,
        'total_crops': total_crops,
        'most_purchased_products': most_purchased_products,
    }
    return render(request, 'admin_dashboard.html', context)

def add_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        return redirect('admin_dashboard')
    return render(request, 'add_user.html')

# View for editing user details
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Get user by id
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, 'User updated successfully!')
        return redirect('manage_users')  # Redirect to admin dashboard after editing
    return render(request, 'edit_user.html', {'user': user})

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('manage_users')
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User


from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404

from django.http import JsonResponse
from .models import Feedback

def get_feedback(request):
    feedbacks = Feedback.objects.all().values('id', 'name', 'email', 'message')
    return JsonResponse(list(feedbacks), safe=False)
from django.core.mail import send_mail
from django.http import JsonResponse
import json

def send_reply(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']
        reply = data['reply']

        # Send email to the user (or save reply in DB)
        send_mail(
            'Reply from Admin',
            reply,
            'admin@example.com',
            [email],
            fail_silently=False,
        )
        return JsonResponse({'status': 'success'})
from django.shortcuts import render


# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *


from django.db.models import Q    
    # Continue with the rest of your view logic
@login_required
def my_account(request):
    user = request.user
    user_profile = user.profile  # Assuming you have a related profile model for additional fields like 'phone'

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            # Check for duplicate username or email
            username = user_form.cleaned_data['username']
            email = user_form.cleaned_data['email']

            if User.objects.filter(Q(username=username) & ~Q(id=user.id)).exists():
                messages.error(request, 'Username already exists.')
            elif User.objects.filter(Q(email=email) & ~Q(id=user.id)).exists():
                messages.error(request, 'Email is already taken.')
            else:
                user_form.save()
                profile_form.save()  # Save the updated profile
                messages.success(request, 'Your profile has been updated successfully.')
                return redirect('my_account')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileForm(instance=user_profile)  # Load existing profile data

    return render(request, 'my_account.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': user,
        'user_profile': user_profile
    })

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import transaction
from .models import Profile  # Adjust according to your project structure

from django.core.exceptions import ValidationError
import re

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Check for password match
        if password1 != password2:
            return render(request, 'register.html', {'error': 'Passwords do not match.'})

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already taken.'})

        # Validate the phone number
        if not re.match(r'^\d{10}$', phone):
            return render(request, 'register.html', {'error': 'Phone number must be 10 digits long and contain only numbers.'})

        # Create user
        user = User.objects.create_user(username=username, password=password1, email=email)

        # Create or update the profile
        profile, created = Profile.objects.get_or_create(user=user)  # This will either fetch the existing profile or create a new one
        profile.phone = phone  # Set the phone number
        profile.save()  # Save the profile with the phone number

        # Redirect to login or another page
        return redirect('login')
    
    return render(request, 'register.html')

from django.shortcuts import render, redirect, get_object_or_404
from .models import Feedback  # Ensure this matches your structure

# View for listing feedback
def feedback_list(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'feedback_list.html', {'feedbacks': feedbacks})

# View for replying to feedback
def reply_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    if request.method == 'POST':
        feedback.reply = request.POST['reply']
        feedback.save()
        return redirect('feedback_list')
    return render(request, 'reply_feedback.html', {'feedback': feedback})
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required
def user_logout(request):
    logout(request)
    return redirect('logout_page')  # Redirect to the logout page
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

@login_required
def user_logout(request):
    logout(request)
    return redirect('logout_page')  # Make sure this matches the name in your urls.py

class LogoutPage(TemplateView):
    template_name = 'logout.html'  # This should point to your logout.html template
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)  # Log the user out
    return redirect('/')  # Redirect to the home page or any other page

from .models import ContactMessage
from .forms import ContactForm

# View to handle contact form submission
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Create a ContactMessage instance but don't save to DB yet
            contact_message = form.save(commit=False)
            contact_message.save()  # Save the form data to the database
            return redirect('contact_us')  # Redirect to a success page or back to the contact form
    else:
        form = ContactForm()
    
    return render(request, 'contact_us.html', {'form': form})

# View to display submitted messages
def admin_user_messages(request):
    messages = ContactMessage.objects.all()
    return render(request, 'admin_user_messages.html', {'messages': messages})

#------------------------------------------------------------------------------------------------------------------------------------------------------------------
from django.shortcuts import render, get_object_or_404
from .models import Crop

def crop_detail(request, crop_id):
    crop = get_object_or_404(Crop, pk=crop_id)
    return render(request, 'crop_detail.html', {'crop': crop})


def purchase_crop(request, crop_id):
    if request.method == 'POST':
        # Retrieve crop and quantity from the form
        crop = get_object_or_404(Crop, pk=crop_id)

        # Retrieve quantity from the form, default to 1 if not provided
        quantity = request.POST.get('quantity', 1)
        quantity = int(quantity)

        # Check if requested quantity exceeds available stock
        if quantity > crop.stock_quantity:
            # If the requested quantity is more than available
            message = f"Only {crop.stock_quantity} quantity available."
            return render(request, 'purchase.html', {'crop': crop, 'quantity': quantity, 'message': message})

        # Calculate total price
        total_price = crop.price * quantity
        crops = Crop.objects.all()

        # Update the stock quantity in the database
        crop.stock_quantity -= quantity
        crop.save()  # Save the updated crop instance

        # Render purchase confirmation page with details
        return render(request, 'purchase.html', {
            'crop': crops,
            'price':crops,
            'quantity': quantity,
            'total_price': total_price,
            'message': 'Purchase successful!' 
        })

    # If not POST, redirect or handle accordingly
    return redirect('view_cart')  # Redirect to cart if method is not POST


def confirm_purchase(request):
    if request.method == 'POST':
        # Logic for handling payment and stock update

        return redirect('purchase_success')    
    
from .forms import CropForm

def add_crop(request):
    if request.method == 'POST':
        form = CropForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Redirect to your admin dashboard after saving
    else:
        form = CropForm()

    return render(request, 'add_crop.html', {'form': form})    

def purchase_success(request):
    return render(request, 'purchase_success.html')


def manage_crops(request):
    crops = Crop.objects.all()  # Get all crops
    return render(request, 'manage_crops.html', {'crops': crops})

# View to edit a crop
def edit_crop(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id)  # Get the crop or return 404
    if request.method == 'POST':
        form = CropForm(request.POST, request.FILES, instance=crop)
        if form.is_valid():
            form.save()  # Save the edited crop
            messages.success(request, 'Crop updated successfully!')
            return redirect('manage_crops')
    else:
        form = CropForm(instance=crop)  # Load the form with existing crop data
    return render(request, 'edit_crop.html', {'form': form, 'crop': crop})

# View to delete a crop
def delete_crop(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id)  # Get the crop or return 404
    if request.method == 'POST':
        crop.delete()  # Delete the crop
        messages.success(request, 'Crop deleted successfully!')
        return redirect('manage_crops')
    return render(request, 'confirm_delete.html', {'crop': crop})


from .models import Crop, CartItem

@login_required
def add_to_cart(request, crop_id):
    crop = Crop.objects.get(id=crop_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, crop=crop)
    
    if not created:
        cart_item.quantity += 1  # Increase quantity if item already exists in cart
    cart_item.save()

    # Add a success message
    messages.success(request, f"{crop.name} has been added to your cart.")
    
    return redirect('home')

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_amount = sum(item.total_price() for item in cart_items)
    
    
    return render(request, 'view_cart.html', {'cart_items': cart_items, 'total_amount': total_amount})

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')



from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .models import CartItem, Crop


@login_required
def purchase_all_crops(request):
    if request.method == 'POST':
        cart_item_ids = request.POST.getlist('cart_item_ids')
        crops = []  # List to hold crops being purchased
        total_price = 0  # Variable to hold the total price
        quantities = {}  # Dictionary to hold quantities per crop

        for item_id in cart_item_ids:
            try:
                cart_item = CartItem.objects.get(id=item_id)
                crop = cart_item.crop
                
                # Check if the desired quantity is available
                if cart_item.quantity > crop.stock_quantity:
                    messages.error(request, f'Only {crop.stock_quantity} of {crop.name} available.')
                    return redirect('view_cart')  # Return to cart on error
                else:
                    # Add crop information to the crops list
                    crops.append(crop)
                    total_price += crop.price * cart_item.quantity  # Calculate total price
                    quantities[crop.id] = cart_item.quantity  # Store the quantity

                    # Deduct the quantity from the stock
                    crop.stock_quantity -= cart_item.quantity
                    crop.save()

                    # Optionally, delete the cart item after purchase
                    cart_item.delete()
                    messages.success(request, f'Purchased {cart_item.quantity} of {crop.name} successfully.')

            except CartItem.DoesNotExist:
                messages.error(request, 'Item not found in the cart.')

        # After processing all items, render the purchase confirmation page
        return render(request, 'purchase.html', {
            'crops': crops,
            'quantities': quantities,
            'total_price': total_price,
        })

    return redirect('view_cart')  # Redirect to the cart if not a POST request


def update_cart_quantity(request, item_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        cart_item = get_object_or_404(CartItem, id=item_id)
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1
        cart_item.save()
    return redirect('view_cart')  # Redirect back to the cart view

# View for the admin dashboard - displays all users
def Manage_user(request):
    users = User.objects.all()  # Fetch all users
    return render(request, 'manage_users.html', {'users': users})


# View to display feedback messages
def feedback_list_view(request):
    # Fetch all feedback from the ContactMessage model
    feedback_list = ContactMessage.objects.all()
    return render(request, 'feedback_admin.html', {'feedback_list': feedback_list})

def delete_feedback_view(request, id):
    # Get the specific feedback message by ID and delete it
    feedback = get_object_or_404(ContactMessage, id=id)
    feedback.delete()
    return redirect('feedback_admin')  # Redirect to the feedback list after deletion