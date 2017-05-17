from django import forms
 
from models import PostPhoto
 
 
class UploadFileForm(forms.ModelForm):
     
    class Meta:
        model = PostPhoto
