from django import forms


class JobsForm(forms.Form):
    latitude = forms.CharField()
    longitude = forms.CharField()
    depart = forms.DateTimeField(required=False)
    transit_time = forms.IntegerField(required=False)
