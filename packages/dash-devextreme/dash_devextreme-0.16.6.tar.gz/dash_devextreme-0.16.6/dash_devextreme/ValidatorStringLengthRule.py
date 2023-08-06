# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ValidatorStringLengthRule(Component):
    """A ValidatorStringLengthRule component.


Keyword arguments:

- ignoreEmptyValue (boolean; default False):
    If set to True, empty values are valid.

- max (number; optional):
    Specifies the maximum length allowed for the validated value.

- message (string; default 'The length of the value is not correct'):
    Specifies the message that is shown if the rule is broken.

- min (number; optional):
    Specifies the minimum length allowed for the validated value.

- trim (boolean; default True):
    Indicates whether or not to remove the Space characters from the
    validated value.

- type (a value equal to: 'required', 'numeric', 'range', 'stringLength', 'custom', 'compare', 'pattern', 'email', 'async'; default 'stringLength'):
    Specifies the rule type. Set it to \"stringLength\" to use the
    StringLengthRule."""
    @_explicitize_args
    def __init__(self, ignoreEmptyValue=Component.UNDEFINED, max=Component.UNDEFINED, message=Component.UNDEFINED, min=Component.UNDEFINED, trim=Component.UNDEFINED, type=Component.UNDEFINED, **kwargs):
        self._prop_names = ['ignoreEmptyValue', 'max', 'message', 'min', 'trim', 'type']
        self._type = 'ValidatorStringLengthRule'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['ignoreEmptyValue', 'max', 'message', 'min', 'trim', 'type']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(ValidatorStringLengthRule, self).__init__(**args)
