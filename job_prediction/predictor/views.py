from django.shortcuts import render
import joblib
import os

# Load model once
model_path = os.path.join(os.path.dirname(__file__), 'notebooks/best_job_fraud_model.pkl')
model = joblib.load(model_path)

def predict_job_fraud(request):
    prediction = None

    if request.method == 'POST':
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        requirements = request.POST.get('requirements', '')
        benefits = request.POST.get('benefits', '')

        combined_text = f"{title} {description} {requirements} {benefits}"
        prediction_result = model.predict([combined_text])[0]
        prediction = "Fake" if prediction_result == 1 else "Legit"

    return render(request, 'predict.html', {'prediction': prediction})
