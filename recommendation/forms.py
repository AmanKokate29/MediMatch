# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import PatientQuery


class SymptomForm(forms.ModelForm):
    """Form for patient to enter symptoms and details"""
    
    symptoms = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': _('Enter your symptoms (e.g., fever, headache, cough)')
        }),
        label=_('Symptoms')
    )
    
    age = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your age')
        }),
        label=_('Age'),
        min_value=1,
        max_value=120
    )
    
    gender = forms.ChoiceField(
        choices=[
            ('Male', _('Male')),
            ('Female', _('Female')),
            ('Other', _('Other'))
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=_('Gender')
    )
    
    medical_history = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': _('Any existing medical conditions or allergies (optional)')
        }),
        label=_('Medical History'),
        required=False
    )
    
    class Meta:
        model = PatientQuery
        fields = ['symptoms', 'age', 'gender', 'medical_history']
