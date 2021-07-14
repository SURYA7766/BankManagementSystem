from django import forms

from .models import UserDetails,Transactions


class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['FirstName','LastName','FatherName','MotherName','PhoneNumber','Email','District','State']


class TransactionsForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ['ReceiptantName','Money']