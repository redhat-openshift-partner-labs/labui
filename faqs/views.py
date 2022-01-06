from django.shortcuts import render
from .forms import FaqsForm


def faq(request):
    form = FaqsForm()
    return render(request, 'faqs/faqs.html', {'form': form})
