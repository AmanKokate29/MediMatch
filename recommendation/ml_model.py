# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
import re


class MedicineRecommender:
    """Enhanced ML-based medicine recommendation system with improved accuracy"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=2000, 
            stop_words='english',
            ngram_range=(1, 2),  # Use bigrams for better context
            min_df=1
        )
        self.medicine_data = self._load_medicine_data()
        self.symptom_synonyms = self._load_symptom_synonyms()
        self.tfidf_matrix = None
        self._train_model()
    
    def _load_symptom_synonyms(self):
        """Load medical term synonyms for better matching"""
        return {
            'headache': ['head pain', 'cephalalgia', 'migraine'],
            'fever': ['high temperature', 'pyrexia', 'febrile'],
            'cough': ['coughing', 'tussis'],
            'cold': ['common cold', 'rhinitis', 'nasal congestion'],
            'stomach pain': ['abdominal pain', 'stomach ache', 'gastralgia'],
            'nausea': ['vomiting', 'sick feeling', 'queasiness'],
            'diarrhea': ['loose stool', 'loose motion', 'dysentery'],
            'rash': ['skin rash', 'dermatitis', 'skin irritation'],
            'allergy': ['allergic reaction', 'hypersensitivity'],
        }
    
    def _preprocess_symptoms(self, symptoms):
        """Enhanced preprocessing with synonym expansion"""
        symptoms_lower = symptoms.lower()
        
        # Expand with synonyms
        for main_term, synonyms in self.symptom_synonyms.items():
            for synonym in synonyms:
                if synonym in symptoms_lower:
                    symptoms_lower += f" {main_term}"
        
        return symptoms_lower
    
    def _load_medicine_data(self):
        """Load expanded medicine data with more medicines"""
        data = {
            'medicine_name': [
                # Pain Relief & Fever
                'Paracetamol', 'Ibuprofen', 'Aspirin', 'Naproxen', 'Diclofenac',
                # Antibiotics
                'Amoxicillin', 'Azithromycin', 'Ciprofloxacin', 'Doxycycline', 'Cephalexin',
                'Metronidazole', 'Clarithromycin',
                # Antihistamines & Allergy
                'Cetirizine', 'Loratadine', 'Fexofenadine', 'Diphenhydramine', 'Chlorpheniramine',
                # Gastrointestinal
                'Omeprazole', 'Ranitidine', 'Pantoprazole', 'Domperidone', 'Ondansetron',
                'Loperamide', 'Antacid',
                # Respiratory
                'Salbutamol', 'Montelukast', 'Prednisolone', 'Dexamethasone',
                'Guaifenesin', 'Bromhexine',
                # Diabetes
                'Metformin', 'Glimepiride', 'Insulin',
                # Cardiovascular
                'Lisinopril', 'Amlodipine', 'Atenolol', 'Aspirin Low Dose',
                # Vitamins & Supplements
                'Vitamin D3', 'Vitamin C', 'Vitamin B Complex', 'Iron Supplement', 'Calcium',
                # Anti-inflammatory
                'Diclofenac Gel', 'Hydrocortisone Cream',
                # Others
                'Antibiotic Eye Drops', 'Antihistamine Eye Drops', 'Antiseptic Cream',
                'Cough Syrup', 'Throat Lozenges', 'Paracetamol Suspension'
            ],
            'treats_symptoms': [
                # Pain Relief & Fever
                'fever headache pain body ache muscle pain mild pain temperature',
                'fever pain inflammation headache body ache joint pain arthritis muscle pain',
                'fever pain inflammation headache blood thinner heart protection',
                'pain inflammation arthritis joint pain muscle pain back pain',
                'pain inflammation arthritis joint pain muscle pain severe pain',
                # Antibiotics
                'bacterial infection throat infection respiratory infection ear infection tooth infection',
                'bacterial infection respiratory infection skin infection throat infection bronchitis pneumonia',
                'bacterial infection urinary tract infection uti diarrhea gastroenteritis',
                'bacterial infection respiratory infection acne skin infection',
                'bacterial infection skin infection urinary tract infection respiratory infection',
                'bacterial infection anaerobic infection dental infection',
                'bacterial infection respiratory infection sinusitis',
                # Antihistamines & Allergy
                'allergy sneezing itching runny nose hay fever watery eyes allergic reaction',
                'allergy sneezing itching runny nose hay fever long acting',
                'allergy sneezing hay fever allergic rhinitis urticaria',
                'allergy sneezing itching insomnia sleep aid allergic reaction',
                'allergy sneezing runny nose watery eyes hay fever',
                # Gastrointestinal
                'acidity heartburn gastric ulcer stomach pain gerd reflux',
                'acidity heartburn gastric problem stomach upset',
                'acidity heartburn gastric ulcer gerd severe reflux',
                'nausea vomiting gastric motility stomach bloating',
                'nausea vomiting severe vomiting antiemetic chemotherapy nausea',
                'diarrhea loose stool loose motion traveler diarrhea',
                'acidity heartburn stomach pain indigestion gas',
                # Respiratory
                'asthma breathing difficulty wheezing cough bronchospasm',
                'asthma allergic rhinitis breathing difficulty long term management',
                'severe inflammation asthma severe allergy inflammatory conditions',
                'severe inflammation allergy swelling skin rash severe allergic reaction',
                'cough chest congestion mucus productive cough',
                'cough mucus chest congestion phlegm',
                # Diabetes
                'diabetes high blood sugar type 2 diabetes insulin resistance',
                'diabetes high blood sugar type 2 diabetes combination therapy',
                'diabetes type 1 diabetes type 2 diabetes high blood sugar',
                # Cardiovascular
                'high blood pressure hypertension heart condition kidney protection',
                'high blood pressure hypertension heart condition angina',
                'high blood pressure hypertension heart rate control',
                'heart protection stroke prevention blood thinner cardiovascular',
                # Vitamins & Supplements
                'vitamin deficiency weakness bone pain fatigue calcium absorption',
                'vitamin deficiency weakness immunity cold prevention antioxidant',
                'vitamin deficiency fatigue weakness nerve health',
                'anemia iron deficiency fatigue weakness pale skin',
                'bone weakness osteoporosis calcium deficiency weak bones',
                # Anti-inflammatory
                'joint pain muscle pain inflammation topical pain relief',
                'skin inflammation rash itching eczema dermatitis topical',
                # Others
                'eye infection conjunctivitis red eyes eye pain bacterial',
                'eye allergy itchy eyes watery eyes allergic conjunctivitis',
                'wound infection cut scrape minor burns skin infection',
                'cough dry cough wet cough throat irritation',
                'sore throat throat pain throat irritation',
                'fever pain headache children pediatric liquid'
            ],
            'category': [
                'Pain Relief', 'Pain Relief', 'Pain Relief', 'Pain Relief', 'Pain Relief',
                'Antibiotic', 'Antibiotic', 'Antibiotic', 'Antibiotic', 'Antibiotic',
                'Antibiotic', 'Antibiotic',
                'Antihistamine', 'Antihistamine', 'Antihistamine', 'Antihistamine', 'Antihistamine',
                'Antacid', 'Antacid', 'Antacid', 'Antiemetic', 'Antiemetic',
                'Antidiarrheal', 'Antacid',
                'Bronchodilator', 'Antiasthmatic', 'Steroid', 'Steroid',
                'Expectorant', 'Expectorant',
                'Antidiabetic', 'Antidiabetic', 'Antidiabetic',
                'Antihypertensive', 'Antihypertensive', 'Antihypertensive', 'Antiplatelet',
                'Vitamin', 'Vitamin', 'Vitamin', 'Supplement', 'Supplement',
                'Topical', 'Topical',
                'Eye Drops', 'Eye Drops', 'Topical',
                'Cough Syrup', 'Throat Relief', 'Pediatric'
            ],
            'description': [
                # Pain Relief & Fever
                'Effective pain reliever and fever reducer, safe for most ages',
                'Anti-inflammatory drug for pain, fever, and inflammation',
                'Pain reliever with blood-thinning properties',
                'Strong anti-inflammatory for arthritis and chronic pain',
                'Powerful NSAID for severe pain and inflammation',
                # Antibiotics
                'Broad-spectrum antibiotic for common bacterial infections',
                'Macrolide antibiotic effective for respiratory infections',
                'Fluoroquinolone antibiotic for urinary and GI infections',
                'Tetracycline antibiotic for various bacterial infections',
                'First-generation cephalosporin antibiotic',
                'Antibiotic effective against anaerobic bacteria',
                'Macrolide antibiotic for respiratory infections',
                # Antihistamines
                'Non-drowsy antihistamine for allergy relief',
                'Long-acting antihistamine for daily allergy management',
                'Non-drowsy antihistamine for hay fever',
                'Effective antihistamine with sedative properties',
                'First-generation antihistamine for allergies',
                # Gastrointestinal
                'Proton pump inhibitor for severe acid reflux',
                'H2 blocker for acid reduction and heartburn',
                'Strong PPI for gastric ulcers and GERD',
                'Prokinetic agent for nausea and bloating',
                'Powerful antiemetic for severe nausea',
                'Antidiarrheal medication to reduce bowel movements',
                'Antacid for quick relief from heartburn',
                # Respiratory
                'Fast-acting bronchodilator for asthma relief',
                'Leukotriene receptor antagonist for asthma control',
                'Corticosteroid for severe inflammation',
                'Powerful steroid for severe allergic reactions',
                'Expectorant to loosen chest congestion',
                'Mucolytic agent to break down mucus',
                # Diabetes
                'First-line medication for type 2 diabetes',
                'Sulfonylurea for blood sugar control',
                'Hormone for blood sugar regulation',
                # Cardiovascular
                'ACE inhibitor for blood pressure and heart protection',
                'Calcium channel blocker for hypertension',
                'Beta-blocker for heart rate and blood pressure',
                'Low-dose aspirin for heart attack prevention',
                # Vitamins & Supplements
                'Essential vitamin for bone health and immunity',
                'Antioxidant vitamin for immunity and healing',
                'B vitamins for energy and nerve health',
                'Iron supplement for anemia treatment',
                'Calcium supplement for bone strength',
                # Topical
                'Topical anti-inflammatory gel for joint pain',
                'Mild corticosteroid cream for skin inflammation',
                # Others
                'Antibiotic eye drops for eye infections',
                'Antihistamine eye drops for eye allergies',
                'Topical antiseptic for wound care',
                'Multi-symptom cough relief syrup',
                'Soothing throat lozenges for sore throat',
                'Liquid paracetamol for children'
            ],
            'usage': [
                # Pain Relief & Fever
                'Take 1-2 tablets every 4-6 hours. Max 4000mg/day',
                'Take 1 tablet every 6-8 hours with food. Max 1200mg/day',
                'Take 1 tablet with food as needed. Max 300mg/day',
                'Take 1 tablet twice daily with food',
                'Take 1 tablet 2-3 times daily with food',
                # Antibiotics
                'Take 500mg every 8 hours. Complete full course',
                'Take 500mg once daily for 3-5 days',
                'Take 500mg twice daily. Complete full course',
                'Take 100mg twice daily. Complete full course',
                'Take 500mg every 6 hours for 7-10 days',
                'Take 400mg three times daily',
                'Take 500mg twice daily for 7-14 days',
                # Antihistamines
                'Take 1 tablet once daily, with or without food',
                'Take 1 tablet once daily in the morning',
                'Take 1 tablet once daily',
                'Take 1 tablet every 4-6 hours as needed',
                'Take 1 tablet every 4-6 hours',
                # Gastrointestinal
                'Take 1 capsule 30 minutes before breakfast',
                'Take 1 tablet twice daily before meals',
                'Take 1 tablet once daily before breakfast',
                'Take 1 tablet 3 times daily before meals',
                'Take 1 tablet 30 minutes before chemotherapy',
                'Take 2mg after each loose stool. Max 16mg/day',
                'Take 1-2 tablets as needed for heartburn',
                # Respiratory
                'Use 1-2 puffs every 4-6 hours as needed',
                'Take 1 tablet once daily in the evening',
                'Take as prescribed by doctor, usually 5-60mg/day',
                'Use as prescribed by doctor in emergency situations',
                'Take 1-2 teaspoons every 4 hours',
                'Take 1 tablet 3 times daily with water',
                # Diabetes
                'Take 500-2000mg daily with meals',
                'Take 1-4mg once daily before breakfast',
                'Inject as prescribed by doctor',
                # Cardiovascular
                'Take 5-10mg once daily',
                'Take 5-10mg once daily',
                'Take 25-100mg once daily',
                'Take 75-100mg once daily with food',
                # Vitamins
                'Take 1 tablet daily with food',
                'Take 500-1000mg daily',
                'Take 1 tablet daily',
                'Take 1 tablet daily on empty stomach',
                'Take 1-2 tablets daily with meals',
                # Topical
                'Apply thin layer to affected area 2-3 times daily',
                'Apply thin layer to affected area 1-2 times daily',
                # Others
                'Instill 1-2 drops in affected eye 3-4 times daily',
                'Instill 1 drop in affected eye twice daily',
                'Apply to cleaned wound 2-3 times daily',
                'Take 2 teaspoons every 4-6 hours',
                'Dissolve 1 lozenge slowly every 2-3 hours',
                'Give 10-15ml every 4-6 hours based on age'
            ],
            'side_effects': [
                # Pain Relief
                'Rare: liver problems with overdose, nausea',
                'Stomach upset, heartburn, dizziness, kidney issues',
                'Stomach bleeding, allergic reactions, increased bleeding risk',
                'Stomach upset, headache, dizziness, fluid retention',
                'Stomach pain, heartburn, diarrhea, increased bleeding risk',
                # Antibiotics
                'Diarrhea, nausea, allergic rash, stomach upset',
                'Stomach upset, diarrhea, nausea',
                'Nausea, diarrhea, dizziness, headache',
                'Sun sensitivity, nausea, diarrhea, tooth discoloration',
                'Diarrhea, nausea, allergic reactions',
                'Metallic taste, nausea, diarrhea',
                'Stomach upset, taste disturbance',
                # Antihistamines
                'Drowsiness (mild), dry mouth, headache',
                'Minimal drowsiness, headache, fatigue',
                'Minimal side effects, mild headache',
                'Significant drowsiness, dry mouth, dizziness',
                'Drowsiness, dry mouth, blurred vision',
                # Gastrointestinal
                'Headache, diarrhea, nausea, vitamin B12 deficiency',
                'Headache, dizziness, constipation, diarrhea',
                'Headache, diarrhea, abdominal pain',
                'Dry mouth, diarrhea, headache',
                'Headache, constipation, dizziness',
                'Constipation, drowsiness, nausea',
                'Constipation, chalky taste, gas',
                # Respiratory
                'Tremor, headache, increased heart rate, nervousness',
                'Headache, stomach upset, dizziness',
                'Increased appetite, mood changes, insomnia, weight gain',
                'Increased blood sugar, weight gain, mood changes',
                'Nausea, vomiting, diarrhea',
                'Nausea, vomiting, stomach upset',
                # Diabetes
                'Nausea, diarrhea, stomach upset, vitamin B12 deficiency',
                'Low blood sugar, weight gain, dizziness',
                'Low blood sugar, weight gain, injection site reactions',
                # Cardiovascular
                'Dizziness, dry cough, fatigue, high potassium',
                'Ankle swelling, flushing, headache, dizziness',
                'Fatigue, cold hands/feet, slow heart rate, dizziness',
                'Stomach upset, increased bleeding risk, heartburn',
                # Vitamins
                'Rare: constipation with high doses, nausea',
                'Stomach upset with high doses, diarrhea',
                'Nausea, flushing, rare allergic reactions',
                'Constipation, stomach upset, dark stools',
                'Constipation, bloating, kidney stones (rare)',
                # Topical
                'Skin irritation, redness at application site',
                'Skin thinning with prolonged use, burning',
                # Others
                'Eye irritation, burning, temporary blurred vision',
                'Mild burning, headache',
                'Skin irritation, redness',
                'Drowsiness, nausea, dizziness',
                'Throat numbness (temporary)',
                'Same as tablets but easier to dose for children'
            ],
            'precautions': [
                # Pain Relief
                'Do not exceed recommended dose. Avoid alcohol. Check liver function with long-term use.',
                'Take with food. Avoid if stomach ulcers. Monitor kidney function.',
                'Avoid if blood clotting disorders. Take with food. Not for children under 16.',
                'Take with food. Monitor kidney and liver function. Avoid in pregnancy.',
                'Take with food. Not for pregnant women. Monitor blood pressure.',
                # Antibiotics
                'Complete full course. Inform if allergic to penicillin. Take with water.',
                'Complete full course. May interact with antacids. Take on empty stomach.',
                'Drink plenty of water. Avoid dairy products. May cause sun sensitivity.',
                'Avoid dairy, antacids. May cause permanent tooth discoloration in children.',
                'Complete full course. May cause allergic reactions.',
                'Avoid alcohol. May cause dark urine. Complete full course.',
                'Complete full course. May interact with other medications.',
                # Antihistamines
                'May cause mild drowsiness. Avoid with alcohol.',
                'Can be taken long-term. Safe for daily use.',
                'Non-drowsy. Safe for driving.',
                'Causes drowsiness. Do not drive or operate machinery.',
                'Avoid driving. Limit alcohol consumption.',
                # Gastrointestinal
                'Take on empty stomach for best results. Long-term use may affect B12.',
                'Avoid smoking and alcohol for best results.',
                'May mask stomach cancer symptoms. Monitor with long-term use.',
                'May cause irregular heartbeat in some patients.',
                'Use only for severe nausea. May cause headache.',
                'Do not use for more than 2 days without doctor advice.',
                'May interact with other medications. Take 2 hours apart.',
                # Respiratory
                'Rinse mouth after use. Do not exceed recommended dose.',
                'Take in evening for best results. Safe for long-term use.',
                'Do not stop suddenly. Taper as directed by doctor.',
                'Use only in emergencies. Carry medical alert card.',
                'Drink plenty of water. Avoid if cough is chronic.',
                'Drink plenty of water with each dose.',
                # Diabetes
                'Monitor blood sugar regularly. Take with meals. Avoid alcohol.',
                'Monitor blood sugar. May cause low blood sugar. Take with breakfast.',
                'Monitor blood sugar closely. Rotate injection sites.',
                # Cardiovascular
                'Monitor blood pressure. May cause dizziness. Rise slowly from sitting.',
                'May cause ankle swelling. Monitor blood pressure regularly.',
                'Do not stop suddenly. May mask low blood sugar symptoms.',
                'Take with food. Avoid if bleeding disorders. Monitor for bleeding.',
                # Vitamins
                'Take with meals for better absorption. Safe for long-term use.',
                'High doses may cause diarrhea. Take with food.',
                'Take with meals. May cause flushing.',
                'Take on empty stomach or with vitamin C. May cause constipation.',
                'Take with food. Avoid if kidney stones. Stay hydrated.',
                # Topical
                'For external use only. Avoid on open wounds.',
                'Do not use for more than 2 weeks. Avoid on face long-term.',
                # Others
                'For eye use only. Remove contact lenses before use.',
                'For eye use only. Wait 10 minutes before contacts.',
                'For external use only. Keep wound clean.',
                'Read label for age-appropriate dosing.',
                'Do not exceed 12 lozenges per day.',
                'Dose based on child weight and age. Check with pediatrician.'
            ]
        }
        
        return pd.DataFrame(data)
    
    def _train_model(self):
        """Train the TF-IDF model on medicine symptom data"""
        self.tfidf_matrix = self.vectorizer.fit_transform(
            self.medicine_data['treats_symptoms']
        )
    
    def recommend_medicines(self, symptoms, age=None, gender=None, top_n=5):
        """
        Enhanced medicine recommendation with age/gender consideration
        
        Args:
            symptoms (str): Patient symptoms
            age (int): Patient age for age-appropriate recommendations
            gender (str): Patient gender
            top_n (int): Number of recommendations to return
            
        Returns:
            list: List of recommended medicines with details
        """
        # Preprocess symptoms with synonym expansion
        processed_symptoms = self._preprocess_symptoms(symptoms)
        
        # Transform input symptoms
        symptoms_vector = self.vectorizer.transform([processed_symptoms])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(symptoms_vector, self.tfidf_matrix)[0]
        
        # Apply age-based filtering
        if age is not None:
            similarities = self._apply_age_filter(similarities, age)
        
        # Get top N similar medicines (fetch more initially for filtering)
        top_indices = similarities.argsort()[-min(top_n * 2, len(similarities)):][::-1]
        
        # Prepare recommendations
        recommendations = []
        seen_categories = {}
        
        for idx in top_indices:
            if similarities[idx] > 0:  # Only include if there's some similarity
                medicine_name = self.medicine_data.iloc[idx]['medicine_name']
                category = self.medicine_data.iloc[idx]['category']
                
                # Limit same category medicines to avoid redundancy
                if category not in seen_categories:
                    seen_categories[category] = 0
                
                if seen_categories[category] < 2:  # Max 2 medicines per category
                    recommendations.append({
                        'medicine_name': medicine_name,
                        'category': category,
                        'description': self.medicine_data.iloc[idx]['description'],
                        'usage': self.medicine_data.iloc[idx]['usage'],
                        'side_effects': self.medicine_data.iloc[idx]['side_effects'],
                        'precautions': self.medicine_data.iloc[idx]['precautions'],
                        'similarity_score': round(similarities[idx] * 100, 2)
                    })
                    seen_categories[category] += 1
                    
                    if len(recommendations) >= top_n:
                        break
        
        return recommendations
    
    def _apply_age_filter(self, similarities, age):
        """Apply age-based filtering to recommendations"""
        filtered_similarities = similarities.copy()
        
        for idx, medicine_name in enumerate(self.medicine_data['medicine_name']):
            # Reduce score for pediatric medicines if adult
            if age >= 18 and 'Pediatric' in medicine_name or 'Suspension' in medicine_name:
                filtered_similarities[idx] *= 0.5
            
            # Reduce score for aspirin if under 16 (Reye's syndrome risk)
            if age < 16 and 'Aspirin' in medicine_name and 'Low Dose' not in medicine_name:
                filtered_similarities[idx] *= 0.3
        
        return filtered_similarities


# Singleton instance
_recommender_instance = None

def get_recommender():
    """Get or create recommender instance"""
    global _recommender_instance
    if _recommender_instance is None:
        _recommender_instance = MedicineRecommender()
    return _recommender_instance
