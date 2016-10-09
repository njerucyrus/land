from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", max_length=100, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for field_name in ['username', 'password', 'password2']:
            self.fields[field_name].help_text = None


class LandUserProfileForm(forms.Form):
    id_no = forms.CharField(max_length=20, widget=forms.NumberInput(
        attrs={'id': 'id_no', 'placeholder': 'Enter National ID No'}
    ))
    ward = forms.CharField(max_length=32, widget=forms.TextInput(
        attrs={'id': 'ward', 'placeholder': 'Enter the ward name'}
    ))
    location = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'id': 'location', 'placeholder': 'Enter Land Location'}
    ))
    district = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'id': 'district', 'placeholder': 'Enter District Name'}
    ))
    phone_number = forms.CharField(max_length=13, widget=forms.TextInput(
        attrs={'id': 'district', 'placeholder': 'Enter your phone number (+2547 xxx xxx)'}
    ))
    address = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'id': 'district', 'placeholder': 'Enter your physical address'}
    ))


class RegisterLandForm(forms.Form):
    title_deed = forms.CharField(max_length=32, widget=forms.TextInput(
        attrs={'id': 'title_deed', 'placeholder': 'Enter Title Deed No', }
    ))
    approximate_size = forms.CharField(max_length=32, widget=forms.NumberInput(
        attrs={'id': 'land_size', 'placeholder': 'Enter The Land Size (Hacters)', }
    ))
    registry_map_sheet_no = forms.CharField(max_length=32, widget=forms.TextInput(
        attrs={'id': 'map_sheet', 'placeholder': 'Enter Map-sheet Number)', }
    ))
    district = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'id': 'district', 'placeholder': 'Enter district', }
    ))
    location = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'id': 'location', 'placeholder': 'Enter location)', }
    ))
    sale_price = forms.CharField(max_length=128, widget=forms.NumberInput(
        attrs={'id': 'location', 'placeholder': 'Enter Sale Price Ksh (Optional)', }
    ), required=False, )


class LoginForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)


class LandPurchaseForm(forms.Form):
    phone_number = forms.CharField(max_length=13, widget=forms.TextInput(
        attrs={'id': 'phone_number', 'placeholder': 'Enter Your Phone Number format(+2547 XXX XXX)'}
    ))
    deposit_amount = forms.CharField(max_length=14, widget=forms.NumberInput(
        attrs={'id': 'deposit_amount', }
    ), disabled=True, required=True)
