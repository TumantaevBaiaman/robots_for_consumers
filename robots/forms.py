from django import forms


class RobotForm(forms.Form):
    model = forms.CharField(max_length=2, required=True)
    version = forms.CharField(max_length=2, required=True)
    created = forms.DateTimeField(required=True)