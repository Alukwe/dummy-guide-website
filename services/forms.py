from django import forms
from .models import Categories, Services, ServiceImages

class ServicesForms(forms.ModelForm):
    # category = forms.ModelChoiceField(queryset=Category.objects.all())
    # subcategory = forms.ModelChoiceField(queryset=Subcategory.objects.all(), required=False)

    class Meta:
        model = Services
        fields = ['name', 'description', 'price', 'category'] #'subcategory']

class ServiceImageForm(forms.ModelForm):
    class Meta:
        model = ServiceImages
        fields = ['image']

class ServiceUpdateForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ['name', 'description', 'price', 'category',]