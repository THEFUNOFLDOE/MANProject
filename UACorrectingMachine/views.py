from django.contrib import messages
from django.shortcuts import render
from .forms import UACorrectingMachineSearchForm
from .model.model import predict_correction


def index(request):
    if request.POST:
        try:
            form = UACorrectingMachineSearchForm(request.POST)
            txt_for_correction = form.data.get("txt_for_correction")
            nn_numb_predicts = int(form.data.get("nn_numb_predicts"))
            
            if len(txt_for_correction) > 170:
                messages.warning(request, "Оскільки введене вами речення перевищує довжину у 170 символів, його частина була втрачена.")
            if nn_numb_predicts > 10:
                messages.warning(request, "Бажана кількість варіантів виправлень перевищує можливості нейронної мережі. Буде отримано 10 варіантів відповіді.")
                nn_numb_predicts = 10
            
            nn_prediction = tuple(zip(*predict_correction(text=txt_for_correction, num_return_sequences=nn_numb_predicts)))
            
        except Exception as error:
            print(error.args)
            return render(request, 'UACorrectingMachine/error.html')
        return render(request,
                            'UACorrectingMachine/checked.html',
                            context={'result': nn_prediction})
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
    nn_numb_predicts=6
    text=''
    if id == 1:
        text='Це самий лучший день'
    elif id == 2:
        text='Степанко радий старатися хоч і страшнувато було'
    else:
        text='я й не думав що лінгвістика це легко'

    nn_prediction = tuple(zip(*predict_correction(text=text, num_return_sequences=nn_numb_predicts)))

    return render(request,
                  'UACorrectingMachine/checked.html',
                  context={'result': nn_prediction})