from django import forms


class UACorrectingMachineSearchForm(forms.Form):
    search = forms.CharField(label="Введіть ваш текст, для його перевірки нейронною мережею",
                             widget=forms.Textarea(attrs={'rows': '3',
                                                          'class': 'form-control form-control-lg'}))
