from django import forms

from lists.models import Item

#constant for error message
EMPTY_ITEM_ERROR = "You can't have an empty list item"

class ItemForm(forms.ModelForm):
    
    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.TextInput(
              attrs={'class':'form-control input-lg',
                     'placeholder':'Enter a to-do item'
              }),
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }
    
    def save(self,for_list):
        self.instance.list = for_list
        return super().save()
    

#example of a form--we replaced it for a modelform
#class ItemForm(forms.Form):
#    item_text = forms.CharField(
#        widget=forms.fields.TextInput(attrs={'class': 'form-control input-lg',
#                                             'placeholder':'Enter a to-do item'})
#    )