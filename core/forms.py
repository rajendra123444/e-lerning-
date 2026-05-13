from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from .models import User, Branch

class UserCreationForm(BaseUserCreationForm):
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), required=False)
    semester = forms.IntegerField(min_value=1, max_value=8, required=False)
    college = forms.CharField(max_length=100, required=False)

    class Meta(BaseUserCreationForm.Meta):
        model = User   # important – custom User model
        fields = ('username', 'email', 'password1', 'password2', 'branch', 'semester', 'college')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # make branch and semester optional in form
        self.fields['branch'].required = False
        self.fields['semester'].required = False
        self.fields['college'].required = False