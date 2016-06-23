from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
from django.shortcuts import render

from formtools.wizard.views import SessionWizardView
from wkhtmltopdf.views import PDFTemplateResponse




class JobApplicationWizard(SessionWizardView):
    file_storage = FileSystemStorage(location=settings.MEDIA_ROOT)
    template_name = 'jobs_form/apply.html'

    def done(self, form_list, form_dict, **kwargs):

        email = EmailMessage(
            "SACHS Apply",
            "A new job application has arrive.",
            "alvinj.delacruz@gmail.com",
            ["alvinj.delacruz@gmail.com"],
        )

        cover_letter_file = form_dict['0'].cleaned_data['cover_letter_file']
        resume_file = form_dict['0'].cleaned_data['resume_file']

        email.attach_file(cover_letter_file.file.name)
        email.attach_file(resume_file.file.name)

        pdf = PDFTemplateResponse(
            self.request,
            template='jobs_form/pdf_body.html',
            context={'forms': form_list},
        )
        pdf.render()

        email.attach(
            filename='form.pdf',
            content=pdf.content,
            mimetype='application/pdf'
        )

        email.send()

        return render(self.request, 'jobs_form/done.html')