from django import forms


class FaqsForm(forms.Form):
    question = forms.CharField(required=True)
    category = forms.ChoiceField(required=True, choices=[('general', 'General'), ('openshift', 'OpenShift'), ('support', 'Support')])
