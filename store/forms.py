from django import forms
from django.contrib.auth.forms import UserCreationForm
from store.models import CustomUser,Orders

class SignUpForm(UserCreationForm):

    class Meta:

        model=CustomUser

        fields=['username', 'email' , 'password1' , 'password2']

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control '
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    
class SignInForm(forms.Form):

    username = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control mb-3 border-2px', 'placeholder': 'Enter your username'})
    )
    password = forms.CharField(max_length=200,
                               widget=forms.PasswordInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter your password'})
    )

class OrderForm(forms.ModelForm):

    class Meta:

        model=Orders

        fields=['address','phone','payment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['class'] = 'form-control'
        self.fields['payment'].widget.attrs['class'] = 'form-select'


class BMIForm(forms.Form):
    height = forms.FloatField(label="Height (in cm)", min_value=1, required=True)
    weight = forms.FloatField(label="Weight (in kg)", min_value=1, required=True)

    def clean(self):

        cleaned_data = super().clean()
        height = cleaned_data.get("height")
        weight = cleaned_data.get("weight")
        if height <= 0 or weight <= 0:
            raise forms.ValidationError("Height and weight must be positive values.")
        return cleaned_data