from collections import OrderedDict
from os.path import splitext

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
from django.shortcuts import render

from formtools.wizard.views import CookieWizardView

from easy_pdf.rendering import render_to_pdf_response, render_to_pdf


class JobApplicationWizard(CookieWizardView):
    file_storage = FileSystemStorage(location=settings.MEDIA_ROOT)
    template_name = 'jobs_form/apply.html'

    def done(self, form_list, form_dict, **kwargs):

        email = EmailMessage(
            settings.EMAIL_MESSAGE_SUBJECT,
            settings.EMAIL_MESSAGE_BODY,
            settings.EMAIL_MESSAGE_SENDER,
            settings.EMAIL_MESSAGE_RECIPIENTS,
        )

        cover_letter_file = form_dict['0'].cleaned_data['cover_letter_file']
        resume_file = form_dict['0'].cleaned_data['resume_file']

        email.attach('cover_letter' + splitext(cover_letter_file.name)[1],
                     cover_letter_file.file.read(),
                     mimetype=cover_letter_file.content_type)

        email.attach('resume' + splitext(resume_file.name)[1],
                     resume_file.file.file.read(),
                     mimetype=resume_file.content_type)

        forms_fields = [form.fields for form in form_list]
        forms_data = [form.cleaned_data for form in form_list]

        forms = []
        for index, fields in enumerate(forms_fields):
            form = OrderedDict()
            for key, value in fields.items():
                if key != 'cover_letter_file' and key != 'resume_file':
                    form[key] = {
                        'label': value.label,
                        'value': forms_data[index][key]
                    }
            forms.append(form)

        pdf = render_to_pdf('jobs_form/pdf_body.html', {'forms': forms})

        email.attach(
            filename='form.pdf',
            content=pdf,
            mimetype='application/pdf'
        )

        email.send()

        return render(self.request, template_name='jobs_form/done.html')