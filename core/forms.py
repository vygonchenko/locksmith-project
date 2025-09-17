from django import forms
from phonenumber_field.formfields import PhoneNumberField

class CallbackForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name',
            'required': True
        })
    )
    
    phone = PhoneNumberField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Phone Number',
            'required': True
        })
    )
    
    time = forms.ChoiceField(
        choices=[
            ('morning', 'Morning (9:00 - 12:00)'),
            ('afternoon', 'Afternoon (12:00 - 17:00)'),
            ('evening', 'Evening (17:00 - 21:00)'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': True
        })
    )
    
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Additional information (optional)'
        })
    )
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Дополнительная валидация номера телефона, если нужно
        return phone