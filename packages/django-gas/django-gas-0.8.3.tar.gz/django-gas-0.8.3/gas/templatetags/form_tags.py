from django import forms
from django import template
from django.template.loader import render_to_string

register = template.Library()


def base_form_field(field, css=None, container_class='', add_another_url=None, field_template=None):
    if field.is_hidden:
        return str(field)

    classes = field.field.widget.attrs.get('class', '').split(' ')
    classes.append('form-control')
    if css:
        classes.append(css)

    if isinstance(field.field.widget, forms.Select):
        classes.append('select2')
    elif isinstance(field.field, forms.DateField):
        field.field.widget.input_type = 'date'

    if isinstance(field.field, forms.SplitDateTimeField):
        field.field.widget.widgets[1].attrs['placeholder'] = '00:00:00'
    else:
        field.field.widget.attrs['placeholder'] = field.label

    if field_template is None:
        if isinstance(field.field.widget, forms.CheckboxInput):
            field_template = 'gas/tags/forms/checkbox.html'
        else:
            field_template = 'gas/tags/forms/field.html'

    field.field.widget.attrs['class'] = " ".join(classes)
    return render_to_string(field_template, {
        'field': field,
        'add_another_url': add_another_url,
        'container_class': container_class,
    })


@register.simple_tag
def add_widget_attrs(field, **attrs):
    field.field.widget.attrs.update(attrs)
    return ''


@register.inclusion_tag('gas/tags/forms/errors.html')
def form_errors(form, container_class=''):
    return {
        'form': form,
        'container_class': container_class,
    }


register.simple_tag(base_form_field, name='form_field')
