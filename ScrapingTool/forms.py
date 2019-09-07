from django.forms import forms



class HomePageForm(forms.Form):

    URL = forms.char(label="Username")