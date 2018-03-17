from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import AppendedText, FieldWithButtons, StrictButton

from .models import Question, Document
from .widgets import SimpleMarkdownEditor

# SearchForm
class SearchForm(forms.Form):
    """ The form for search """
    search = forms.CharField(label="Search", required=True,
                             widget=forms.TextInput(attrs={
                                 'placeholder': 'Ask a question...',
                                 'onclick': 'this.select();',
                                 'onmouseup': 'return false;'}))

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'GET'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            FieldWithButtons('search',
                             StrictButton('<i class="fa fa-search"></i>',
                                          css_class="btn-primary",
                                          type="submit")),
        )


# QuestionForm
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content', 'tags']

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget = SimpleMarkdownEditor()
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Ask'))


# DocumentForm
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'content', 'topic', 'tags']

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget = SimpleMarkdownEditor()
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Save'))
