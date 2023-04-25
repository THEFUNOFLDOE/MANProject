from django import forms


class UACorrectingMachineSearchForm(forms.Form):
    txt_for_correction = forms.CharField(label="Введіть ваш текст, для того, щоб нейронна мережа його перевірила",
                                         widget=forms.Textarea(attrs={'rows': '3',
                                                                      'id': 'textInput',
                                                                      'class': 'form-control form-control-lg'}))
    nn_numb_predicts = forms.CharField(label="Вкажіть, скільки варіантів виправлень має запропонувати нейронна мережа",
                                          widget=forms.TextInput(attrs={'id': 'integerInput',
                                                                        'class': 'form-control form-control-lg'}))
