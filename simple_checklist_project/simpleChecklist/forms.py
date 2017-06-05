from django import forms
from simpleChecklist.models import TodoList, Task

class TodoListForm(forms.ModelForm):
    name = forms.CharField(max_length=128)
    slug = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = TodoList
        fields = ['name']

class TaskForm(forms.ModelForm):
    name = forms.CharField(max_length=128)
    slug = forms.CharField(widget=forms.HiddenInput, required=False)
    note = forms.CharField(widget=forms.Textarea, max_length=200, required=False)
    PRIORITY_CHOICES = (
        ('1', 'Low'),
        ('2', 'Normal'),
        ('3', 'High'),
    )
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, initial="2")

    class Meta:
        model = Task
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'})
        }
        exclude = ['todolist']
