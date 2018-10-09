from wtforms.validators import DataRequired, Length

def field_renderer(field, *args, **kwargs):
    field.render_kw = field.render_kw or {}
    for validator in field.validators:
        add_attr_func = _validator_mapping.get(
            type(validator), log_new_validator)
        add_attr_func(field, validator)
    return field()


def add_attr_DataRequired(field, validator):
    field.render_kw['required'] = True
    if validator.message:
        field.render_kw['data-msg-required'] = validator.message

def add_attr_Length(field, validator):
    if validator.min >= 0:
        field.render_kw['minlength'] = max(
            field.render_kw.get('minlength', 0), validator.min)
        if validator.message:
            field.render_kw['data-msg-minlength'] = validator.message
    if validator.max >= 0:
        field.render_kw['maxlength'] = min(
            field.render_kw.get('maxlength', float('inf')), validator.max)
        if validator.message:
            field.render_kw['data-msg-maxlength'] = validator.message

def log_new_validator(field, validator):
    print('Warning: Unhandled validator {} of field {}'.format(
        type(validator).__name__, field.id))

# TODO: Add more add_attr_xxx functions
_validator_mapping = {
    DataRequired: add_attr_DataRequired,
    Length: add_attr_Length
}
