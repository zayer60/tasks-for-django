from django import forms
from django.forms import fields

from .models import Article


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields =('headline','content','pub_date')
        widgets ={
            'headline': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'pub_date': forms.DateInput(),
        }



