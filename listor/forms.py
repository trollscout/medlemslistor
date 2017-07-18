'''
Created on 11 juli 2017

@author: perhk
'''

from django import forms

# class EmailForm(forms.Form):
#     username = forms.EmailField(label='E-postadress', max_length=100)
   
class UploadFileForm(forms.Form):
#     title = forms.CharField(max_length=50)
    file = forms.FileField()
