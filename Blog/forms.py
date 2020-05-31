from django import forms

from . import models

# CATEGORY FORM
class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ['name', 'image']


# COMMENT FORM
class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['comment']