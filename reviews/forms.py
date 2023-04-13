from django import forms
from .models import Review, Comment


class ReviewForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Review
        fields = ('title', 'content', 'movie', 'image',)


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

