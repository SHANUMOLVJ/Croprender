# crop_recommendation/views.py
from django.shortcuts import render

def some_view(request):
    # Your view function logic here
    context = {}
    return render(request, 'template_name.html', context)

from django.shortcuts import render

def about(request):
    return render(request, 'about.html')
def home(request):
    return render(request, 'home.html')  # Replace 'home.html' with the actual template name

def profile(request):
    return render(request, 'profile.html')  # Replace 'dashboard/profile.html' with the actual template name



def login(request):
    return render(request, 'login.html')  # Replace 'dashboard/home.html' with the actual template name

def edit_profile(request):
    return render(request, 'edit_profile.html')  # Replace 'dashboard/edit_profile.html' with the actual template name

def my_account(request):
    return render(request, 'my_account.html') 
 # Replace 'dashboard/my_account.html' with the actual template name

def report(request):
    return render(request, 'report.html')
def recommend_crop(request):
    return render(request, 'recommend_crop.html')
def recommend_crop(request):
    return render(request, 'recommend_crop.html')




from django.shortcuts import render
import joblib
import numpy as np

# Load the model
model = joblib.load('crop_recommendation_model.pkl')

def recommend_crop(request):
    if request.method == 'POST':
        try:
            # Get user inputs from the form
            nitrogen = float(request.POST['nitrogen'])
            phosphorus = float(request.POST['phosphorus'])
            potassium = float(request.POST['potassium'])
            temperature = float(request.POST['temperature'])
            humidity = float(request.POST['humidity'])
            ph_value = float(request.POST['ph_value'])
            rainfall = float(request.POST['rainfall'])

            # Predict using the model
            prediction = model.predict([[nitrogen, phosphorus, potassium, temperature, humidity, ph_value, rainfall]])

            # Render result on the same page
            return render(request, 'recommend_crop.html', {
                'prediction': prediction[0],
                'nitrogen': nitrogen,
                'phosphorus': phosphorus,
                'potassium': potassium,
                'temperature': temperature,
                'humidity': humidity,
                'ph_value': ph_value,
                'rainfall': rainfall
            })

        except Exception as e:
            return render(request, 'recommend_crop.html', {'error': str(e)})

    return render(request, 'recommend_crop.html')

from django.shortcuts import render
from django.http import HttpResponse
import numpy as np

# Assuming you have a trained model loaded
# Load the model (ensure you load it correctly)
# model = load_model('path_to_your_model')
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
import joblib

# Load the dataset
data = pd.read_csv('crop_recommendation.csv')

# Features and target
X = data[['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'pH_Value', 'Rainfall']]
y = data['Crop']

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define a pipeline for preprocessing and classification
pipeline = Pipeline(steps=[
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Train the model
pipeline.fit(X_train, y_train)

# Save the model to a file
joblib.dump(pipeline, 'crop_recommendation_model.pkl')

def recommend_crop(request):
    if request.method == "POST":
        try:
            # Get input values from the form
            nitrogen = float(request.POST['nitrogen'])
            phosphorus = float(request.POST['phosphorus'])
            potassium = float(request.POST['potassium'])
            temperature = float(request.POST['temperature'])
            humidity = float(request.POST['humidity'])
            ph_value = float(request.POST['ph_value'])
            rainfall = float(request.POST['rainfall'])

            # Format data for prediction (assuming this shape is what your model expects)
            input_data = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph_value, rainfall]])

            # Get prediction from the model
            # prediction = model.predict(input_data)
            prediction = "Wheat"  # This is a placeholder. Replace with actual model prediction.

            # Render the result in the template
            return render(request, 'recommend_crop.html', {'prediction': prediction})

        except Exception as e:
            # Handle errors gracefully
            error_message = str(e)
            return render(request, 'recommend_crop.html', {'error': error_message})
    
    # If it's a GET request, simply render the form
    return render(request, 'recommend_crop.html')
from django.shortcuts import render, redirect

def recommend(request):
    if request.method == "POST":
        # Extract input data from the form
        nitrogen = request.POST['nitrogen']
        phosphorus = request.POST['phosphorus']
        potassium = request.POST['potassium']
        temperature = request.POST['temperature']
        humidity = request.POST['humidity']
        ph_value = request.POST['ph_value']
        rainfall = request.POST['rainfall']

        # Example crop recommendation logic
        crop = recommend_crop(nitrogen, phosphorus, potassium, temperature, humidity, ph_value, rainfall)

        # Redirect to the report page with the data
        return redirect('report', nitrogen=nitrogen, phosphorus=phosphorus, potassium=potassium,
                        temperature=temperature, humidity=humidity, ph_value=ph_value, rainfall=rainfall, crop=crop)

    return render(request, 'recommend.html')
def report(request):
    nitrogen = request.GET['nitrogen']
    phosphorus = request.GET['phosphorus']
    potassium = request.GET['potassium']
    temperature = request.GET['temperature']
    humidity = request.GET['humidity']
    ph_value = request.GET['ph_value']
    rainfall = request.GET['rainfall']
    crop = request.GET['crop']

    context = {
        'nitrogen': nitrogen,
        'phosphorus': phosphorus,
        'potassium': potassium,
        'temperature': temperature,
        'humidity': humidity,
        'ph_value': ph_value,
        'rainfall': rainfall,
        'crop': crop,
    }

    return render(request, 'report.html', context)
from django.shortcuts import render

def upload_view(request):
    return render(request, 'upload.html')
from django.shortcuts import render

def recommend_crop(request):
    # Extract query parameters
    nitrogen = float(request.GET.get('nitrogen', 0))
    phosphorus = float(request.GET.get('phosphorus', 0))
    potassium = float(request.GET.get('potassium', 0))
    temperature = float(request.GET.get('temperature', 0))
    humidity = float(request.GET.get('humidity', 0))
    ph_value = float(request.GET.get('ph_value', 0))
    rainfall = float(request.GET.get('rainfall', 0))

    # Perform crop recommendation
    data = {
        'nitrogen': nitrogen,
        'phosphorus': phosphorus,
        'potassium': potassium,
        'temperature': temperature,
        'humidity': humidity,
        'ph_value': ph_value,
        'rainfall': rainfall
    }
    
    recommended_crop = recommend_crop_logic(data)  # Implement this function as needed

    return render(request, 'recommend_crop.html', {'recommended_crop': recommended_crop})

def recommend_crop_logic(data):
    # Implement crop recommendation logic here
    # Example:
    if data['nitrogen'] > 50 and data['ph_value'] > 7 and data['temperature'] > 20 and data['humidity'] > 60:
        return "Rice"
    # Add more conditions as needed
    return "Unknown Crop"

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to login page after successful registration
            return redirect('login')
        else:
            # If form is invalid, re-render the registration page with errors
            return render(request, 'register.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:  # Check if user is admin (staff)
            login(request, user)
            return redirect('admin_dashboard')  # Redirect to admin dashboard
        else:
            return render(request, 'admin_login.html', {'error': 'Invalid login'})
    return render(request, 'admin_login.html')


@login_required
def admin_dashboard(request):
    # Render the admin dashboard page after successful login
    return render(request, 'admin_dashboard.html')

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