from django import forms
from .models import NoteModel, CategoryModel


class NoteForm(forms.Form):
    text = forms.CharField(required=True, label='متن', widget=forms.Textarea(attrs={
        'placeholder': 'یادداشت خود را وارد کنید.',
        'required': 'required'
    }))

    title = forms.CharField(required=True, max_length=50, label='عنوان', widget=forms.TextInput(attrs={
        'placeholder': 'عنوان یادداشت را وارد کنید.',
        'required': 'required'
    }))

    #
    # category = forms.ModelChoiceField(queryset=CategoryModel.objects.all(),
    #                                                  label='دسته بندی', required=True)

    def __init__(self, user, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(queryset=CategoryModel.objects.filter(user=user),
                                                         label='دسته بندی', required=True)


class CategoryForm(forms.Form):
    title = forms.CharField(required=True, label='عنوان دسته بندی', widget=forms.TextInput(attrs={
        'placeholder': 'عنوان دسته بندی وارد کنید.',
        'required': 'required'
    }))

# class NoteModelForm(forms.ModelForm):
#     class Meta:
#         model=NoteModel
#         fields=['text','categories','title']
#
#         widgets={
#             'text':forms.Textarea(attrs={
#                 'placeholder':'متن',
#                 'required':"required"
#             }),
#             'title': forms.TextInput(attrs={
#                 'placeholder': 'عنوان',
#                 'required': "required"
#             })
#         }
