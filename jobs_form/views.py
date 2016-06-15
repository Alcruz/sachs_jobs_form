import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render_to_response
from formtools.wizard.views import SessionWizardView


class JobApplicationWizard(SessionWizardView):
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'temps'))

    def done(self, form_list, **kwargs):
        return render_to_response('done.html', {
            'form_data': [form.cleaned_data for form in form_list]
        })
