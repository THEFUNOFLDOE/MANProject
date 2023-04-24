from django.shortcuts import render
from .forms import UACorrectingMachineSearchForm
from .model.model import predict_correction


def index(request):
    if request.POST:
        try:
            form = UACorrectingMachineSearchForm(request.POST)
            txt_for_correction = form.data.get("txt_for_correction")
            nn_numb_predicts = int(form.data.get("nn_numb_predicts"))
            return render(request,
                        'UACorrectingMachine/checked.html',
                        context={'result': predict_correction(text=txt_for_correction,
                                                                num_return_sequences=nn_numb_predicts)})
        except Exception as error:
            print(error.args)
            return render(request, 'UACorrectingMachine/error.html')
    
    else:
        form = UACorrectingMachineSearchForm
    return render(request,
                'UACorrectingMachine/index.html',
                context={'form': form})
    
def about(request):
    return render(request,
                  'UACorrectingMachine/about.html')


def instruction(request):
    return render(request,
                  'UACorrectingMachine/instruction.html')

def render_example(request, id):
    num_return_sequences=6
    text=''
    match id:
        case 1:
            text='Це самий лучший день'
        case 2:
            text='Степанко радий старатися хоч і страшнувато було'
        case _:
            text='я й не думав що лінгвістика це легко'
    return render(request,
                  'UACorrectingMachine/checked.html',
                  context={'result': predict_correction(text=text,
                                                        num_return_sequences=num_return_sequences)})