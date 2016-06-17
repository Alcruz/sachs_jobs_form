from django import forms
from django.forms import widgets

YES_NO_CHOICES = [('Yes', 'Yes'), ('No', 'No')]
SALARY_FORMAT_CHOICES = [(c,c) for c in ['Hourly', 'Weekly', 'Bi-weekly', 'Monthly', 'Year',]]
EDUCATION_TYPE_CHOICES = [(c, c) for c in ['Diploma', 'Degree', 'Other']]


class PersonalInfoForm(forms.Form):
    position_name = forms.CharField(label='*Position Name and Number You are Applying For')
    first_name = forms.CharField(label='*First Name')
    middle_name = forms.CharField(label='M.I.', required=False)
    last_name = forms.CharField(label='*Last Name')
    phone_number = forms.CharField(label='*Phone Number')
    resume_file = forms.FileField(label='*Upload Your Resume', required=False)
    cover_letter_file = forms.FileField(label="*Upload Your Cover Letter/Letter of Interest", required=False)
    have_worked_under_another_name = forms.ChoiceField(
        label='*Have you ever worked under another name?',
        widget=widgets.RadioSelect,
        choices=YES_NO_CHOICES
    )
    under_what_name = forms.CharField(label='If yes, under what name(s)')
    street_address = forms.CharField(label='Street Address')
    street_address2 = forms.CharField(label='Addres line 2')
    city = forms.CharField(label='City')
    state = forms.CharField(label='State')
    zip_code = forms.CharField(label='Postal/Zip Code')
    country = forms.ComboField(label='Country')
    hear_about_this_job = forms.CharField(label='*How did you hear about this job?')
    referred_by_employee = forms.ChoiceField(
        label='Were you referred by an employee?',
        widget=widgets.RadioSelect,
        choices=YES_NO_CHOICES
    )
    employee_name = forms.CharField(label='If yes, list name(s)', required=False)
    day_available_for_work = forms.DateField(label='*Day available for work')
    salary_required = forms.DecimalField(label='*Salary required')
    salary_format = forms.ChoiceField(
        label='*Please select a format',
        widget=widgets.RadioSelect,
        choices=SALARY_FORMAT_CHOICES
    )
    have_applied_to_sachs = forms.ChoiceField(
        label='*Have you ever applied to work at SACHS?',
        widget=widgets.RadioSelect,
        choices=YES_NO_CHOICES
    )


class EducationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(EducationForm, self).__init__(*args, **kwargs)
        for i in range(1,4):
            self.fields['institution_name_%d' % i] = forms.CharField(label='*Name of Educational Institution #%d' % i)
            self.fields['major_%d' % i] = forms.CharField(label='*Major')
            self.fields['number_of_year_%d' % i] = forms.IntegerField(label='*Number of Years')
            self.fields['type_%d' % i] = forms.ChoiceField(
                label='*Type',
                widget = widgets.RadioSelect,
                choices=EDUCATION_TYPE_CHOICES
            )
            self.fields['other_type_%d' % i] = forms.CharField(label='If other, describe')



class EmploymentHistoryForm(forms.Form):
    company_name = forms.CharField(label='*Company Name #1')
    employer_phone_number = forms.CharField(label="*Employer's Phone Number")
    address_street = forms.CharField(label='Street Address')
    address_street_line2 = forms.CharField(label='Address line 2')
    city = forms.CharField(label='City')
    state = forms.CharField(label='State')
    country = forms.CharField(label='Country')
    job_title = forms.CharField(label='*Job Title')
    employed_from = forms.DateField(label='*Employed From', widget=forms.widgets.SelectDateWidget)
    employed_to = forms.DateField(label='*To', widget=forms.widgets.SelectDateWidget)
    starting_salary = forms.DecimalField(label='*Starting Salary')
    ending_salary = forms.DecimalField(label='*Ending Salary')
    starting_salary = forms.CharField(label="*Supervisor's Name")
    contact_employer = forms.ChoiceField(
        label='*Can we contact this employer?',
        choices=YES_NO_CHOICES,
        widget=forms.RadioSelect
    )
    job_duties = forms.CharField(label='Job Duties', widget=forms.widgets.Textarea)


class ProfessionalLicenseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ProfessionalLicenseForm, self).__init__(*args, **kwargs)
        for i in range(1,4):
            self.fields['license_%d' % i] = forms.CharField(label='License/Certification', required=False)
            self.fields['state_%d' % i] = forms.CharField(label='State', required=False)
            self.fields['license_number_%d' % i] = forms.CharField(label='License Number', required=False)
            self.fields['expire_date_%d' % i] = forms.DateField(
                label='Date Expires',
                widget=forms.widgets.SelectDateWidget,
                required=False
            )


class ProfessionalReferenceForm(forms.Form):
    eligible_for_employment_in_us = forms.ChoiceField(
        label='*Are you legally eligible for employment in the United States of America?',
        choices=YES_NO_CHOICES,
        widget=forms.widgets.RadioSelect
    )
    supporting_documentation = forms.ChoiceField(
        label='*If so, are you able to furnish supporting documentation',
        choices=YES_NO_CHOICES,
        widget=forms.widgets.RadioSelect
    )

    def __init__(self, *args, **kwargs):
        super(ProfessionalReferenceForm, self).__init__(*args, *kwargs)
        for i in range(1,4):
            self.fields['reference_%d' % i] = forms.CharField(label='Reference #%d' % i, required=False)
            self.fields['current_position_%d' % i] = forms.CharField(label='Current Position and Company', required=False)
            self.fields['phone_number_%d' % i] = forms.CharField(label='Phone Number', required=False)


class CertificationAndRelease(forms.Form):
    signature = forms.CharField(label='*Signature (Enter your full name)')
    date = forms.DateTimeField(
        label="*Enter Today's Date and Time of Signature",
        widget=forms.widgets.SplitDateTimeWidget
    )
