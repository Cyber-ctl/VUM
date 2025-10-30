"""from django import forms

class ExcelUploadForm(forms.Form):
    file = forms.FileField(
      widget=forms.ClearableFileInput(attrs={
        'class': 'form-control custom-upload input-lg',
        'style': 'padding: 10px; border: 1px solid #ccc;'})
    )
"""

from django import forms

class ExcelUploadForm(forms.Form):
    File = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
        'class': 'form-control custom-upload input-lg mb-2 ',
        'style': 'padding: 10px; border: 1px solid #ccc; width:50%'
        })

    )
