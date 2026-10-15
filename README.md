# MediMatch - Medicine Recommendation System

An intelligent medicine recommendation system that helps users find appropriate over-the-counter medications based on their symptoms using machine learning.

## Features
- 🤖 AI-powered medicine recommendations
- 🌐 Multi-language support (English & Hindi)
- 📊 Personalized recommendations based on age, gender, and medical history
- 📜 Query history tracking
- 🎨 Modern, responsive UI with Bootstrap 5
- 🏥 Nearby medical facilities finder (hospitals, clinics, pharmacies)

## Technologies Used
- **Backend:** Django 5.0
- **Machine Learning:** scikit-learn, pandas, numpy
- **Translation:** deep-translator
- **Frontend:** Bootstrap 5, Font Awesome
- **Database:** SQLite (development), PostgreSQL (production-ready)

## Usage
1. Navigate to "Get Recommendation" page
2. Enter your symptoms
3. Provide age, gender, and medical history
4. Select language preference (English/Hindi)
5. Get personalized medicine recommendations
6. View recommendation history

### Finding Nearby Medical Facilities
1. Log in to your account
2. Click "Nearby Care" in the navigation bar (or the "Find Nearby Care" button on the home page)
3. Enter your address or click the GPS button to use your current location
4. Select the facility type (Hospitals, Clinics, Pharmacies, or All)
5. Set your search radius
6. Click "Search" to see results on a map and as a list

## Project Structure

```
MediMatch/
├── medicine_project/      # Django project settings
├── recommendation/        # Main application
│   ├── models.py         # Database models
│   ├── views.py          # View logic
│   ├── forms.py          # Forms
│   ├── ml_model.py       # ML recommendation engine
│   └── urls.py           # URL routing
├── templates/            # HTML templates
├── static/              # Static files (CSS, images)
├── locale/              # Translation files
├── requirements.txt     # Python dependencies
├── Procfile            # Heroku deployment
└── runtime.txt         # Python version
```

## Important Notes

⚠️ **Medical Disclaimer:** This system is for informational purposes only and should not replace professional medical advice. Always consult with a healthcare provider before taking any medication.
