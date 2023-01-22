from django.shortcuts import render
from .forms import UACorrectingMachineSearchForm
from .functions import CORPUS, show_corrections


def index(request):
    found = []
    doc_ids = []
    if request.POST:
        form = UACorrectingMachineSearchForm(request.POST)

        for doc in CORPUS:
            if form.data.get('search') in doc.source:
                found.append(f'{str(doc.target)[:100]}...')
                doc_ids.append(doc.doc_id)
    else:
        form = UACorrectingMachineSearchForm
    return render(request,
                  'UACorrectingMachine/index.html',
                  context={'form': form, 'searches': dict(zip(found, doc_ids))})


def found(request, index):
    doc = str(CORPUS.get_doc(f'{index:>04}').annotated)
    return render(request,
                  'UACorrectingMachine/found.html',
                  context={'doc': show_corrections(doc)})


def about(request):
    return render(request,
                  'UACorrectingMachine/about.html')
