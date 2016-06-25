from django import forms
from django.forms import widgets

from django_countries.fields import countries, LazyTypedChoiceField
from django_countries.widgets import CountrySelectWidget

YES_NO_CHOICES = [('Yes', 'Yes'), ('No', 'No')]
SALARY_FORMAT_CHOICES = [(c,c) for c in ['Hourly', 'Weekly', 'Bi-weekly', 'Monthly', 'Year',]]
EDUCATION_TYPE_CHOICES = [(c, c) for c in ['Diploma', 'Degree', 'Other']]

CERTIFICATION_AND_REALEASE_TEXT = "I authorize SACHS to verify, in any manner, all statements made by me. SACHS may," \
                                  " for example, interview former employers, schools, references, or others and request" \
                                  " information and supporting documentation such as transcripts and evaluations. " \
                                  "I authorize any and all former employers, references, or educational institutions " \
                                  "to release all information relevant to my employment or education to SACHS, " \
                                  "without giving me prior notice. If employed by SACHS, I agree to comply with all " \
                                  "policies and procedures, safety rules, and cooperate in any reasonable security " \
                                  "investigation. I understand that I am not employed by or entitled to employment by " \
                                  "SACHS unless and until I have received and accepted a written offer of employment " \
                                  "from a Company representative. I also understand that no other act of SACHS, " \
                                  "including the acceptance of my application for employment, the scheduling of " \
                                  "interviews with me, or any oral or written statements of interest or encouragement, " \
                                  "creates an employment relationship with me, and I will not rely on any such act of " \
                                  "SACHS. I understand that if I am employed by SACHS, such employment is “at-will,” " \
                                  "which means that my employment and related compensation may be terminated at any " \
                                  "time, with or without cause, and with or without advance notice by me or SACHS. " \
                                  "I certify that the information I have provided in this employment application, " \
                                  "my resume, any supplementary materials submitted by me is accurate and has been " \
                                  "completed to the best of my knowledge and ability. " \
                                  "I understand that any falsification, misrepresentation or omission in my " \
                                  "interviews or any other employment record, will be sufficient reason to deny " \
                                  "employment and/or may be reason for future dismissal."


class PersonalInfoForm(forms.Form):

    position_name = forms.CharField(
        label='*Position Name and Number You are Applying For'
    )

    first_name = forms.CharField(
        label='*First Name'
    )

    middle_name = forms.CharField(
        label='M.I.', required=False
    )

    last_name = forms.CharField(
        label='*Last Name'
    )

    phone_number = forms.CharField(
        label='*Phone Number'
    )

    resume_file = forms.FileField(
        label='*Upload Your Resume',
    )

    cover_letter_file = forms.FileField(
        label="*Upload Your Cover Letter/Letter of Interest",
    )

    have_worked_under_another_name = forms.ChoiceField(
        label='*Have you ever worked under another name?',
        widget=widgets.RadioSelect,
        choices=YES_NO_CHOICES
    )

    under_what_name = forms.CharField(
        label='If yes, under what name(s)',
        required=False,
    )

    street_address = forms.CharField(
        label='Street Address'
    )

    street_address2 = forms.CharField(
        label='Addres line 2',
        required=False
    )

    city = forms.CharField(
        label='City'
    )

    state = forms.CharField(
        label='State'
    )

    zip_code = forms.CharField(
        label='Postal/Zip Code'
    )

    country = LazyTypedChoiceField(
        label='Country',
        choices=countries,
        initial='US',
        widget=CountrySelectWidget()
    )

    hear_about_this_job = forms.CharField(
        label='*How did you hear about this job?'
    )

    referred_by_employee = forms.ChoiceField(
        label='Were you referred by an employee?',
        widget=widgets.RadioSelect,
        choices=YES_NO_CHOICES
    )

    employee_name = forms.CharField(
        label='If yes, list name(s)',
        required=False
    )

    day_available_for_work = forms.DateField(
        label='*Day available for work',
        widget=forms.DateInput(
            attrs={
                'class': 'date',
            }
        )
    )

    salary_required = forms.DecimalField(
        label='*Salary required'
    )

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

    def clean(self):
        cleaned_data = super(PersonalInfoForm, self).clean()

        have_worked_under_another_name = cleaned_data.get('have_worked_under_another_name')
        under_what_name = cleaned_data.get('under_what_name')

        referred_by_employee = cleaned_data.get('referred_by_employee')
        employee_name = cleaned_data.get('employee_name')

        if not have_worked_under_another_name or \
            (have_worked_under_another_name == 'Yes' and not under_what_name):
            self.add_error('under_what_name', 'You must supply this field if you had worked under another name.')

        if not referred_by_employee or \
                (referred_by_employee == 'Yes' and not employee_name):
            self.add_error('employee_name', 'You must supply this field if you were referred by an employee.')


class EducationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(EducationForm, self).__init__(*args, **kwargs)
        self._create_form(1, required=True, star='*')
        for i in range(2,4):
            self._create_form(i)

    def _create_form(self, i, required=False, star=''):
        self.fields['institution_name_%d' % i] = forms.CharField(
            label=star+'Name of Educational Institution #%d' % i,
            required=required
        )
        self.fields['major_%d' % i] = forms.CharField(
            label=star+'Major',
            required=required
        )
        self.fields['number_of_year_%d' % i] = forms.IntegerField(
            label=star+'Number of Years',
            required=required
        )
        self.fields['type_%d' % i] = forms.ChoiceField(
            label=star+'Type',
            widget=widgets.RadioSelect,
            choices=EDUCATION_TYPE_CHOICES,
            required=required
        )
        self.fields['other_type_%d' % i] = forms.CharField(
            label='If other, describe',
            required=required
        )


class EmploymentHistoryForm(forms.Form):
    company_name = forms.CharField(label='*Company Name')
    employer_phone_number = forms.CharField(label="*Employer's Phone Number")
    address_street = forms.CharField(label='Street Address')
    address_street_line2 = forms.CharField(label='Address line 2', required=False)
    city = forms.CharField(label='City')
    state = forms.CharField(label='State')
    country = LazyTypedChoiceField(label='Country', choices=countries, initial='US')
    job_title = forms.CharField(label='*Job Title')
    employed_from = forms.DateField(
        label='*Employed From',
        widget=forms.DateInput(
            attrs={
                'class': 'date',
            }
        )
    )
    employed_to = forms.DateField(
        label='*To',
        widget=forms.DateInput(
            attrs={
                'class': 'date',
            }
        )
    )
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
            self._create_form(i)

    def _create_form(self, i, required=False):
        self.fields['license_%d' % i] = forms.CharField(label='License/Certification', required=required)
        self.fields['state_%d' % i] = forms.CharField(label='State', required=required)
        self.fields['license_number_%d' % i] = forms.CharField(label='License Number', required=required)
        self.fields['expire_date_%d' % i] = forms.DateField(
            label='Date Expires',
            widget=forms.DateInput(
                attrs={
                    'class': 'date',
                }
            ),
            required=required
        )

    # def clean(self):
    #     cleaned_data = super(ProfessionalLicenseForm, self).clean()
    #
    #     fields1 = ['license_%d' % i for i in range(1, 4)]
    #     fields2 = ['state_%d' % i for i in range(1, 4)]
    #     fields3 = ['license_number_%d' % i for i in range(1, 4)]
    #     fields4 = ['expire_date_%d' % i for i in range(1, 4)]
    #
    #     for i in range(4):
    #         field1 = cleaned_data.get(fields1[i])
    #         field2 = cleaned_data.get(fields2[i])
    #         field3 = cleaned_data.get(fields3[i])
    #         field4 = cleaned_data.get(fields4[i])
    #
    #         if field1:
    #             if not field2:
    #                 self.add_error(fields2[i], 'This field is required')
    #             if not field3:
    #                 self.add_error(fields3[i], 'This field is required')
    #             if not field4:
    #                 self.add_error(fields4[i], 'This field is required')


class ProfessionalReferenceForm(forms.Form):
    eligible_for_employment_in_us = forms.ChoiceField(
        label='*Are you legally eligible for employment in the United States of America?',
        choices=YES_NO_CHOICES,
        widget=forms.widgets.RadioSelect
    )

    supporting_documentation = forms.ChoiceField(
        label='*If so, are you able to furnish supporting documentation?',
        required=False,
        choices=YES_NO_CHOICES,
        widget=forms.widgets.RadioSelect
    )

    def __init__(self, *args, **kwargs):
        super(ProfessionalReferenceForm, self).__init__(*args, **kwargs)

        for i in range(1, 4):
            self._create_form(i)

    def clean(self):
        cleaned_data = super(ProfessionalReferenceForm, self).clean()
        eligible_for_employment_in_us = cleaned_data.get('eligible_for_employment_in_us')
        supporting_documentation = cleaned_data.get('supporting_documentation')

        if not eligible_for_employment_in_us or \
            (eligible_for_employment_in_us == 'Yes' and not supporting_documentation):
            self.add_error(
                'supporting_documentation',
                'You must supply this field if you are legally eligible for employment in the '
                'United State of America.'
            )

    def _create_form(self, i, required=False):
        self.fields['reference_%d' % i] = forms.CharField(
            label='Reference #%d' % i,
            required=required
        )

        self.fields['current_position_%d' % i] = forms.CharField(
            label='Current Position and Company',
            required=required
        )

        self.fields['phone_number_%d' % i] = forms.CharField(
            label='Phone Number',
            required=required
        )


class CertificationAndRelease(forms.Form):
    certification_and_release = forms.CharField(
        label='Certification and Release',
        widget=widgets.Textarea(attrs={'readonly':'readonly'}),
        initial=CERTIFICATION_AND_REALEASE_TEXT
    )

    signature = forms.CharField(label='*Signature (Enter your full name)')

    date = forms.DateTimeField(
        label="*Enter Today's Date and Time of Signature",
        widget=forms.DateInput(
            attrs={
                'class': 'datetime',
            }
        )
    )
