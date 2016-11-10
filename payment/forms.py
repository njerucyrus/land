from django import forms


class LandTransFerFeeForm(forms.Form):
    phone_number = forms.CharField(max_length=13, widget=forms.TextInput(
        attrs={'id': 'phone_number', 'placeholder': 'Enter Phone Number format(+2547 xxx xxx'}
    ))
    amount = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(
        attrs={'id': 'amount', }
    ), disabled=True)

