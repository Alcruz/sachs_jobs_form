import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render_to_response
from formtools.wizard.views import SessionWizardView


class JobApplicationWizard(SessionWizardView):
    file_storage = FileSystemStorage(location=settings.MEDIA_ROOT)
    template_name = 'jobs_form/apply.html'

    def done(self, form_list, **kwargs):
        return render_to_response('jobs_form/done.html', {
            'form_data': [form.cleaned_data for form in form_list]
        })
