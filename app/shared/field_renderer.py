from wtforms.validators import DataRequired, Length, Email, EqualTo


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
        field.render_kw['data-rule-minlength'] = max(
            field.render_kw.get('data-rule-minlength', 0), validator.min)
        if validator.message:
            field.render_kw['data-msg-minlength'] = validator.message
    if validator.max >= 0:
        field.render_kw['data-rule-maxlength'] = min(
            field.render_kw.get('data-rule-maxlength', float('inf')),
            validator.max)
        if validator.message:
            field.render_kw['data-msg-maxlength'] = validator.message


def add_attr_Email(field, validator):
    # Regex from https://stackoverflow.com/questions/201323/how-to-validate-
    # an-email-address-using-a-regular-expression#answer-201378
    field.render_kw['data-rule-pattern'] = (
        r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+"""
        r""")*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\["""
        r"""\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0"""
        r"""-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4]"""
        r"""[0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1"""
        r"""[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c"""
        r"""\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\]"""
        r""")""")
    field.render_kw['data-rule-email'] = "true"
    if validator.message:
        field.render_kw['data-msg-pattern'] = validator.message
        field.render_kw['data-msg-email'] = validator.message


def add_attr_EqualTo(field, validator):
    field.render_kw['data-rule-equalto'] = '#{}'.format(validator.fieldname)
    if validator.message:
        field.render_kw['data-msg-equalto'] = validator.message


def log_new_validator(field, validator):
    print('Warning: Unhandled validator {} of field {}'.format(
        type(validator).__name__, field.id))


_validator_mapping = {
    DataRequired: add_attr_DataRequired,
    Length: add_attr_Length,
    Email: add_attr_Email,
    EqualTo: add_attr_EqualTo
}
