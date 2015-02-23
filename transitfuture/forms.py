from django import forms


class JobsForm(forms.Form):
    latitude = forms.CharField()
    longitude = forms.CharField()
    depart = forms.DateTimeField(required=False)
    transit_time = forms.IntegerField(required=False)


class BikingForm(forms.Form):
    latitude = forms.CharField()
    longitude = forms.CharField()
    transit_time = forms.IntegerField()
    safety = forms.FloatField(min_value=0.0, max_value=1.0)
    quick = forms.FloatField(min_value=0.0, max_value=1.0)
    slope = forms.FloatField(min_value=0.0, max_value=1.0)
    bike_speed = forms.IntegerField()
