from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import AppendedText, FieldWithButtons, StrictButton


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
                             StrictButton('<i class="fas fa-search"></i>',
                                          css_class="btn-primary",
                                          type="submit")),
        )
