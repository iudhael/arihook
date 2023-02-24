from django import forms
from . models import Subscribers, MailMessage


class SubscibersForm(forms.ModelForm):
    email_subscriber = forms.EmailField(label='', required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'your mail',
        'autocomplete': 'on',
    }))
    """
    def clean_email(self):
        email_subscriber = self.cleaned_data.get('email')
        subscriber_count = Subscribers.objects.filter(email_subscriber=email_subscriber).count()
        if subscriber_count > 1:
            raise forms.ValidationError("This email has already been registered.")
        return email_subscriber
    """

    class Meta:
        model = Subscribers
        fields = ['email_subscriber', ]


class MailMessageForm(forms.ModelForm):
    class Meta:
        model = MailMessage
        fields = ['title', 'message']
