from wagtail import hooks
from django.conf import settings
from django.templatetags.static import static

@hooks.register('insert_editor_js')
def editor_js():
    js_files = [
        'js/conditional_fields.js',
    ]
    js_includes = ''.join(['<script src="{0}"></script>'.format(static(file)) for file in js_files])
    return js_includes
