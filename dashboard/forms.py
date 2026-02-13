from django import forms
from staff.models import StaffModel, UserModel


class GuruForm(forms.Form):
    id_user = forms.ModelChoiceField(
        queryset=UserModel.objects.exclude(staffmodel__isnull=False),
        label="User",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
