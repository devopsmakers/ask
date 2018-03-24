from django import forms
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import AppendedText, FieldWithButtons, StrictButton
from taggit_bootstrap import TagsInput

from haystack.forms import ModelSearchForm

from .models import Question, Document
from .widgets import SimpleMarkdownEditor

# EmptySearchForm
class EmptySearchForm(ModelSearchForm):
    def search(self):
        sqs = self.searchqueryset
        return sqs


# QuestionForm
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content', 'tags']

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget = SimpleMarkdownEditor()
        self.fields['tags'].widget = TagsInput()
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Ask'))


# DocumentForm
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'teaser', 'content', 'topic', 'tags']

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget = SimpleMarkdownEditor()
        self.fields['tags'].widget = TagsInput()
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Save'))
