import string
import random
from uuid import UUID


reserved_nicknames = [ ]
reserved_asset_titles = []
reserved_paths = ['admin', ]


def rand_string(chars=4):
    return ''.join(random.choices(string.ascii_lowercase +
                                  string.digits, k=chars))


def uuid_to_hex(uuid):
    return UUID(uuid).hex


def is_valid_nickname(nickname):
    return nickname not in reserved_nicknames


def bootstrap_fields(fields):
    for field in fields:
        widget = fields[field].widget
        css_class = ''
        if hasattr(widget, 'input_type'):
            if widget.input_type == 'select':
                css_class = 'form-select form-select-lg'
            elif widget.input_type == 'checkbox':
                css_class = 'form-check-input checkbox-black'
            elif widget.input_type == 'file':
                css_class = 'form-control'
            else:
                css_class = 'form-control form-control-lg'

        fields[field].widget.attrs['class'] = css_class + ' bg-light text-dark border-0'

    return fields
