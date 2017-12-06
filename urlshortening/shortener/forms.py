from django import forms

from .validators import validate_url

# 사용자가 url을 입력하는 form
class SubmitUrlForm(forms.Form):

    url = forms.CharField(
        label='',
        validators=[validate_url],
        widget=forms.TextInput(
            attrs={
                "placeholder": "Long URL",
                "class": "form-control"
            }
        )
    )


