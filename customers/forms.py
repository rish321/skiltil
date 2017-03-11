from proj.forms import SiteForm

from django import forms


class ProfileForm(SiteForm):
    contact_name = forms.CharField(required=True)
    contact_phone = forms.CharField(required=True)
    contact_email = forms.CharField(required=True, disabled=True)

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = "Name: "
        self.fields['contact_phone'].label = "Phone: "
        self.fields['contact_email'].label = "Email: "
