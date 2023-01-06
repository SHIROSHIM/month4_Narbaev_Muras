from django import forms


class PostCreateForm(forms.Form):
    title = forms.CharField(min_length=8)
    description = forms.CharField(widget=forms.Textarea())
    rate = forms.FloatField(max_value=10)


class CommentCreateForm(forms.Form):
    text = forms.CharField(min_length=3)