from django import forms
from .models import Item

STYLE = 'w-full py-4 px-6 rounded-xl border'

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'name', 'desc', 'price', 'image')

        widgets = {
            'category': forms.Select(attrs={
                'class': STYLE
            }),
            'name': forms.TextInput(attrs={
                'class': STYLE
            }),
            'desc': forms.Textarea(attrs={
                'class': STYLE
            }),
            'price': forms.TextInput(attrs={
                'class': STYLE
            }),
            'image': forms.FileInput(attrs={
                'class': STYLE
            })
        }


class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'desc', 'price', 'image', 'is_sold')

        widgets = {
            'name': forms.TextInput(attrs={
                'class': STYLE
            }),
            'desc': forms.Textarea(attrs={
                'class': STYLE
            }),
            'price': forms.TextInput(attrs={
                'class': STYLE
            }),
            'image': forms.FileInput(attrs={
                'class': STYLE
            })
        }