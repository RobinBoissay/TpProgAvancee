from django import forms
from django.shortcuts import render
from monapp.models import *


class ContactUsForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.EmailField()
    message = forms.CharField(max_length=1000)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('price_ttc', 'status')

class ProductItemForm(forms.ModelForm):
    class Meta:
        model = ProductItem
        fields = '__all__'
        # exclude = ('color', 'name')

    
class ProductAttributeForm(forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = '__all__'
        # exclude = ('color', 'name')

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = '__all__'

class ProductFournisseurForm(forms.ModelForm):
    class Meta:
        model = ProductFournisseur
        fields = '__all__'

class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = '__all__'