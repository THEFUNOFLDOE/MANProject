from django import forms


class UACorrectingMachineSearchForm(forms.Form):
    search = forms.CharField(label="Слово або фраза",
                             widget=forms.TextInput(attrs={'onchange': 'on_change();'}))
