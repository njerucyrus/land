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
        attrs={'id': 'id_no_id', 'placeholder': 'Enter National ID No'}
    ))
    ward = forms.CharField(max_length=32, widget=forms.TextInput(
        attrs={'id': 'ward_id', 'placeholder': 'Enter the ward name'}
    ))
    location = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'id': 'location_id', 'placeholder': 'Enter Land Location'}
    ))
    district = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'id': 'district_id', 'placeholder': 'Enter District Name'}
    ))
    phone_number = forms.CharField(max_length=13, widget=forms.TextInput(
        attrs={'id': 'phone_number_id', 'placeholder': 'Enter your phone number (+2547 xxx xxx)'}
    ))
    address = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'id': 'address_id', 'placeholder': 'Enter your physical address'}
    ))


class RegisterLandForm(forms.Form):
    title_deed = forms.CharField(max_length=32, widget=forms.TextInput(
        attrs={'id': 'title_deed_id', 'placeholder': 'Enter Title Deed No', }
    ))
    approximate_size = forms.FloatField(widget=forms.NumberInput(
        attrs={'id': 'land_size_id', 'placeholder': 'Enter The Land Size (Hacters)', }
    ))
    registry_map_sheet_no = forms.CharField(max_length=32, widget=forms.TextInput(
        attrs={'id': 'map_sheet_id', 'placeholder': 'Enter Map-sheet Number)', }
    ))
    district = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'id': 'district_id', 'placeholder': 'Enter district', }
    ))
    location = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'id': 'location_id', 'placeholder': 'Enter location)', }
    ))
    sale_price = forms.FloatField(widget=forms.NumberInput(
        attrs={'id': 'sale_price_id', 'placeholder': 'Enter Sale Price Ksh (Optional)', }
    ), required=False, )


class LoginForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)


class LandPurchaseForm(forms.Form):
    phone_number = forms.CharField(max_length=13, widget=forms.TextInput(
        attrs={'id': 'phone_number_id', 'placeholder': 'Enter Your Phone Number format(+2547 XXX XXX)'}
    ))
    deposit_amount = forms.CharField(max_length=14, widget=forms.NumberInput(
        attrs={'id': 'deposit_amount', }
    ), disabled=True, required=True)


class TransFerLandPaymentForm(forms.Form):
    phone_number = forms.CharField(max_length=13, widget=forms.TextInput(
        attrs={'id': 'phone_number_id', 'placeholder': 'Enter Your Phone Number format(+2547 XXX XXX)'}
    ))
    amount = forms.CharField(max_length=14, widget=forms.NumberInput(
        attrs={'id': 'amount_id', }
    ), disabled=True, required=True)


class LandTransferForm(forms.Form):
    first_name = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'id': 'first_name_id'}
    ))
    middle_name = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'id': 'middle_name_id'}
    ))
    last_name = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'id': 'last_name_id'},
    ))
    id_no = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'id': 'id_no_id'}
    ))
    district = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'id': 'district_id'}
    ))
    location = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'id': 'location_id'}
    ))
    sub_location = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'id': 'sub_location_id'}
    ))
    transfer_from = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'id': 'transfer_from_id'}
    ), disabled=True)
    land_size = forms.FloatField(disabled=True)
    transfer_size = forms.FloatField()

    def clean_transfer_size(self):
        cd = self.cleaned_data
        transfer_size = float(cd['transfer_size'])
        land_size = float(cd['land_size'])
        if transfer_size > land_size:
            raise forms.ValidationError('Insufficient amount of land for this transfer')
        return cd['transfer_size']


class ConfirmCodeForm(forms.Form):
    code = forms.CharField(max_length=20, label="Verification Code",
                           widget=forms.TextInput(
                               attrs={'placeholder': 'Enter Verification Code'}
                           )
                           )
