import random
from datetime import datetime

from django import forms
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView

from reg.models import Reg, klass_names


class RegForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'number' in self.fields:
            self.fields['number'].help_text = \
                f"Занятые номера: {', '.join(Reg.objects.values_list('number', flat=True))}"
    
    def clean_number(self):
        return str(int(self.cleaned_data['number']))
    
    def save(self, commit=True):
        self.instance.competition = 'last_attack_heat_2022'
        return super().save(commit)
    
    class Meta:
        model = Reg
        fields = ('fio', 'phone', 'number', 'klass', 'city', 'team', 'bike')


class RegFormOutdate(RegForm):
    
    def save(self, commit=True):
        numbers = list(
            map(
                lambda number: int(number),
                Reg.objects.values_list('number', flat=True)
            )
        )
        
        number = random.randint(500, 600)
        while number in numbers:
            number = random.randint(500, 600)
        
        self.instance.number = number
        
        return super().save(commit)
    
    class Meta:
        model = Reg
        fields = ('fio', 'phone', 'klass', 'city', 'team', 'bike')


class RegCreateView(CreateView):
    form_class = RegForm
    model = Reg
    
    def get_success_url(self):
        return f'/list/#number-{self.object.number}'
    
    def get_form_class(self):
        if datetime.now().date() > datetime.strptime('2022-06-22', '%Y-%m-%d').date():
            return RegFormOutdate
        return super().get_form_class()


class RegListView(ListView):
    queryset = Reg.objects.filter(
        competition='last_attack_heat_2022'
    ).order_by(
        'klass', 'number'
    )
    
    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs['klass_names'] = dict(klass_names)
        return super().get_context_data(object_list=object_list, **kwargs)
