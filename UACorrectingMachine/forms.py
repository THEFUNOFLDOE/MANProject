from django import forms


class UACorrectingMachineSearchForm(forms.Form):
    txt_for_correction = forms.CharField(label="Введіть ваш текст, для того, щоб нейронна мережа його перевірила",
                                         widget=forms.Textarea(attrs={'rows': '3',
                                                                      'class': 'form-control form-control-lg'}))
    nn_numb_predicts = forms.IntegerField(label="Вкажіть, скільки виправлень має запропонувати нейронна мережа",
                                          widget=forms.NumberInput(attrs={'class': 'form-control form-control-lg'}))
