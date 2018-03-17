from django import forms
from django.utils.html import mark_safe

class SimpleMarkdownEditor(forms.Widget):
    """
    Code Editor built upon SimpleMDE
    """

    def render(self, name, value, attrs=None, renderer=None):

        template = '''
            <textarea name="%(name)s" id="id_%(name)s" required>%(value)s</textarea>
            <script>
                var simplemde = new SimpleMDE({
            		element: document.getElementById("id_%(name)s"),
            		spellChecker: true,
                    autoDownloadFontAwesome: true,
                    forceSync: true,
                    hideIcons: ["image"],
                    showIcons: ["code", "table"],
            		autosave: {
            			enabled: true,
            			unique_id: "%(name)s",
            		},
            	});
                document.getElementById("id_%(name)s").onsubmit = function(){simplemde.clearAutosavedValue();}
            </script>
        '''
        context = {'name': name, 'value': escape(value) if value else ''}
        return mark_safe(template % context)
