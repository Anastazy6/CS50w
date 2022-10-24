from django import forms
from django.forms import TextInput, Textarea
from .models import *

class NewPostForm(forms.ModelForm):
    class Meta:
        model   = Post
        fields  = ['title', 'body']
        widgets = { 'body':  Textarea (attrs={  'id'         : "new-post-body",
                                                'cols'       : 60,
                                                'rows'       : 6,
                                                'placeholder': 'Type your post here (up to 4096 characters).',
                                                'style'      : 'resize: none;'
                                    }),
                    'title': TextInput(attrs={  'id'         : "new-post-title",
                                                'placeholder': 'Title (optional, up to 64 characters).',
                                                'size'       : 60})
                }
        labels  = {'title': '', 'body': ''}

#class FollowForm(forms.ModelForm):
#   class Meta:
#           model   = Follower
#   pass