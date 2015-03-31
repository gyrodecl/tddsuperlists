from django import forms

from lists.models import Item
from django.core.exceptions import ValidationError

#constant for error message
EMPTY_ITEM_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "You've already got this in your list"

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
    

class ExistingListItemForm(ItemForm):
    def __init__(self, for_list,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)
    
    def save(self):
        return forms.models.ModelForm.save(self)
    
    
    #I like this better#
    def clean_text(self):
        data = self.cleaned_data['text']
        if data in [item.text for item in self.instance.list.item_set.all()]:
            raise forms.ValidationError(DUPLICATE_ITEM_ERROR)
        return data


#example of a form--we replaced it for a modelform
#class ItemForm(forms.Form):
#    item_text = forms.CharField(
#        widget=forms.fields.TextInput(attrs={'class': 'form-control input-lg',
#                                             'placeholder':'Enter a to-do item'})
#    )