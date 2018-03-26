from django import forms
from django.utils.html import mark_safe, escape

class SimpleMarkdownEditor(forms.Widget):
    """
    Code Editor built upon SimpleMDE
    """

    def render(self, name, value, attrs=None, renderer=None):

        template = '''
            <textarea name="%(name)s" id="id_%(name)s"
            onsubmit="simplemde.clearAutosavedValue();">%(value)s</textarea>
            <script>
                var simplemde = new SimpleMDE({
            		element: document.getElementById("id_%(name)s"),
            		spellChecker: true,
                    autoDownloadFontAwesome: true,
                    forceSync: true,
                    hideIcons: ["image"],
                    showIcons: ["code", "table"],
            		autosave: {
            			enabled: false,
            		},
            	});
            </script>
        '''
        context = {'name': name, 'value': escape(value) if value else ''}
        return mark_safe(template % context)
