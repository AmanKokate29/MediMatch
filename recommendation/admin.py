from django.contrib import admin
from .models import MedicineData, PatientQuery


@admin.register(MedicineData)
class MedicineDataAdmin(admin.ModelAdmin):
    list_display = ['medicine_name', 'category']
    search_fields = ['medicine_name', 'category']
    list_filter = ['category']


@admin.register(PatientQuery)
class PatientQueryAdmin(admin.ModelAdmin):
    list_display = ['id', 'age', 'gender', 'created_at']
    list_filter = ['gender', 'created_at']
    search_fields = ['symptoms']
