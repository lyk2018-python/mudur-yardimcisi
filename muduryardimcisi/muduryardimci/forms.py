from django import forms

class AuthTokenForm(forms.Form):
    token_label = forms.CharField(max_length=10)