from django import forms


class BookingForm(forms.Form):
    tenant = forms.CharField(max_length=100, label='Tenant Name')
    rent_start_date = forms.DateField(label='Rent start date')
    rent_end_date = forms.DateField(label='Rent end date')

    def clean(self):
        cleaned_data = super().clean()
        rent_start_date = cleaned_data.get('rent_start_date')
        rent_end_date = cleaned_data.get('rent_end_date')

        if rent_start_date and rent_end_date and rent_end_date <= rent_start_date:
            raise forms.ValidationError("Rent end date must be after rent start date")
