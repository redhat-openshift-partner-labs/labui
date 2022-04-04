from django import forms

# TODO get openshift versions from the api and populate openshift_versions global
openshift_versions = [('ocp-4.8.23', '4.8.23'), ('ocp-4.9.10', '4.9.10')]


class LabRequestsForm(forms.Form):
    cluster_id = forms.UUIDField()
    project_name = forms.CharField(max_length=12, label='Project Name')
    company_name = forms.CharField(max_length=12, label='Company Name')
    request_type = forms.ChoiceField(choices=[('general', 'General'), ('engineering', 'Engineering'), ('nvidia', 'Nvidia')],
                                     label='Request Type')
    sponsor = forms.CharField(label='Sponsor')
    primary_first_name = forms.CharField(max_length=32, label='First Name')
    primary_last_name = forms.CharField(max_length=32, label='Last Name')
    primary_email_address = forms.EmailField(label='Email Address')
    primary_phone_number = forms.IntegerField(label='Phone Number')
    secondary_first_name = forms.CharField(max_length=32, label='First Name')
    secondary_last_name = forms.CharField(max_length=32, label='Last Name')
    secondary_email_address = forms.EmailField(label='Email Address')
    secondary_phone_number = forms.IntegerField(label='Phone Number')
    description = forms.CharField(widget=forms.Textarea, label='Description')
    notes = forms.CharField(widget=forms.Textarea, label='Notes')
    cluster_name = forms.CharField(max_length=12, label='Cluster Name')
    cluster_size = forms.ChoiceField(
        choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('x-large', 'X-Large')],
        label='Cluster Size')
    openshift_version = forms.ChoiceField(choices=openshift_versions, label='OpenShift Version')
    reservation_time = forms.ChoiceField(
        choices=[('1d', 'One Day'), ('1w', 'One Week'), ('2w', 'Two Weeks'), ('1m', 'One Month')],
        label='Reservation Time')
    start_date = forms.DateField(label='Start Date')
    timezone = forms.ChoiceField(
        choices=[('americas', 'Americas UTC-5'), ('emea', 'EMEA UTC+1'), ('apac', 'APAC UTC+7')], label='Timezone')
    extend_time = forms.BooleanField(label='Extend Time')
    cloud_provider = forms.ChoiceField(choices=[('aws', 'AWS'), ('ibm', 'IBM'), ('gcp', 'Google'), ('azure', 'Azure')],
                                       label='Cloud Provider')
    hold = forms.BooleanField(label='Save')
