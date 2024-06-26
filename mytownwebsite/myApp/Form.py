from .models import AddReport
from django import forms
from .models import Message
class AddReportForm(forms.ModelForm):
    class Meta:
        model = AddReport
        fields = ['title', 'neighborhood', 'facility','description', 'location', 'picture']
        labels = {
            'title': '',
            'neighborhood': '',
            'facility': '',
            'description': '',
            'location': '',
            'picture': '',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'neighborhood': forms.TextInput(attrs={'class': 'form-control'}),
             'facility': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'picture': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['worker_name', 'worker_email', 'message']