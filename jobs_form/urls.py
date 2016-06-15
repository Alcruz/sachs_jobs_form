from django.conf.urls import url

from jobs_form.forms import PersonalInfoForm, EducationForm
from jobs_form.views import JobApplicationWizard

urlpatterns = [
    url(r'^apply/$', JobApplicationWizard.as_view([PersonalInfoForm, EducationForm]), name="jobs_apply")
]