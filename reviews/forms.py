from django import forms
from .models import Review, Comment


class ReviewForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Review
        fields = ('title', 'content', 'movie', 'image',)
    title = forms.CharField(
        widget=forms.TextInput(
        attrs={
        'class' : 'form-control',
        'style' : 'width: 250px',
        }
        )
    )

    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'style': 'width: 250px',
            }
        )
    )

    movie = forms.CharField(
        widget=forms.TextInput(
        attrs={
        'class' : 'form-control',
        'style' : 'width: 250px',
        }
        )
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
    content = forms.CharField(
        widget=forms.TextInput(
        attrs={
            'class' : 'form-control',
            'style' : 'width: 250px'
        }
        )
    )

