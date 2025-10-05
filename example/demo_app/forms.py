from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "border rounded px-3 py-2 w-full",
                    "placeholder": "Enter task title...",
                }
            )
        }
