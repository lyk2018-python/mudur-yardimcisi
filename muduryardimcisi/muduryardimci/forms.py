from django import forms
from django.utils.translation import ugettext_lazy as _
from muduryardimci.models import Courses,Profile
class AuthTokenForm(forms.Form):
    token_label = forms.CharField(max_length=6)

class AddNoteForm(forms.Form):
    Note = forms.CharField(max_length=3000)
    Course = forms.ModelChoiceField(Courses.objects.all(),required=True,empty_label="Select Course")
    User = forms.ModelChoiceField(Profile.objects.filter(course_id=Course.label))

    def __init__(self, user, *args, **kwargs):
        super(AddNoteForm, self).__init__(*args, **kwargs)
        self.fields['User'].queryset = Profile.objects.filter(course_id = user)