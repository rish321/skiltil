# make sure this is at the top if it isn't already
from django import forms

from django.utils.safestring import mark_safe

class SiteForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(SiteForm, self).__init__(*args, **kwargs)

# our new form
class ContactForm(SiteForm):
	contact_name = forms.CharField(required=True)
	contact_phone = forms.CharField(required=True)
	contact_email = forms.EmailField(required=False)
	preferred_communication_time = forms.CharField(required=False)
	content = forms.CharField(
        	required=False, widget=forms.Textarea(attrs={'rows': 4})
	)

	def __init__(self, *args, **kwargs):
        	super(ContactForm, self).__init__(*args, **kwargs)
        	self.fields['contact_name'].label = "Name:* "
		self.fields['contact_phone'].label = "Phone:* "
        	self.fields['contact_email'].label = "Email:"
		self.fields['preferred_communication_time'].label = mark_safe("Preferred Time for Communication:<br />")
        	self.fields['content'].label = mark_safe("Anything else you want to convey to us:<br />")
