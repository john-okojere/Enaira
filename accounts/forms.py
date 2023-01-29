from django import forms

from accounts.models import Transfer, User

class Transerform(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['amount', 'comment']