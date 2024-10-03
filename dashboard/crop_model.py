import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def load_data():
    data = pd.read_csv('crop_data.csv')  # You need to have crop_data.csv with N, P, K, temp, humidity, pH, rainfall
    X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
    y = data['label']
    return X, y

def train_model():
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(X_train, y_train)
    return clf

def predict_crop(model, features):
    return model.predict([features])[0]
from flask import Flask, render_template
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, auc
import os

app = Flask(__name__)

# Ensure that the 'static' directory exists
if not os.path.exists('static'):
    os.makedirs('static')

# Dummy data for illustration purposes
y_test = [1, 0, 1, 1, 0, 1]
y_pred = [1, 0, 1, 0, 0, 1]
y_score = [0.1, 0.4, 0.35, 0.8, 0.5, 0.7]
crops = ['Wheat', 'Rice', 'Maize', 'Soybean']
values = [20, 30, 15, 35]

def generate_confusion_matrix():
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('Actual label')
    plt.xlabel('Predicted label')
    path = os.path.join('static', 'confusion_matrix.png')
    plt.savefig(path)
    plt.close()  # Close the plot to free memory
    return path

def generate_roc_curve():
    fpr, tpr, _ = roc_curve(y_test, y_score)
    roc_auc = auc(fpr, tpr)
    plt.figure(figsize=(6, 4))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend(loc="lower right")
    path = os.path.join('static', 'roc_curve.png')
    plt.savefig(path)
    plt.close()  # Close the plot to free memory
    return path

def generate_crop_distribution():
    plt.figure(figsize=(6, 4))
    plt.pie(values, labels=crops, autopct='%1.1f%%', startangle=140)
    plt.title('Crop Distribution')
    path = os.path.join('static', 'crop_distribution.png')
    plt.savefig(path)
    plt.close()  # Close the plot to free memory
    return path

@app.route('/')
def index():
    # Generate charts
    generate_confusion_matrix()
    generate_roc_curve()
    generate_crop_distribution()
    return render_template('index.html')

@app.route('/about')
def about():
    return 'About Us'

if __name__ == '__main__':
    app.run(debug=True)
