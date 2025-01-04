from django import forms 

class InputForm(forms.Form): 
    user_input = forms.URLField(widget=forms.URLInput(attrs={ 
        'id':'',
        'class': 'input_box',
        'placeholder': 'Enter a URL here' }),label=''
    )