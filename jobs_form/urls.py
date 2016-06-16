from django.conf.urls import url

from jobs_form.forms import PersonalInfoForm, EducationForm, EmploymentHistoryForm
from jobs_form.forms import CertificationAndRelease, ProfessionalLicenseForm, ProfessionalReferenceForm
from jobs_form.views import JobApplicationWizard

job_application_forms = [PersonalInfoForm, EducationForm, EmploymentHistoryForm,
                         ProfessionalLicenseForm, ProfessionalReferenceForm, CertificationAndRelease]

urlpatterns = [
    url(r'^apply/$', JobApplicationWizard.as_view(job_application_forms), name="jobs_apply")
]