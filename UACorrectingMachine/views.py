from django.shortcuts import render
from .forms import UACorrectingMachineSearchForm
from .model.model import predict_correction


def index(request):
    if request.POST:
        form = UACorrectingMachineSearchForm(request.POST)
        txt_for_correction = form.data.get("txt_for_correction")
        nn_numb_predicts = int(form.data.get("nn_numb_predicts"))
        return render(request,
                      'UACorrectingMachine/found.html',
                      context={'result': predict_correction(text=txt_for_correction,
                                                            num_return_sequences=nn_numb_predicts)})
    else:
        form = UACorrectingMachineSearchForm
    return render(request,
                  'UACorrectingMachine/index.html',
                  context={'form': form})


def about(request):
    return render(request,
                  'UACorrectingMachine/about.html')
