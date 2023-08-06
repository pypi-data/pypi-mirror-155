# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Validator(Component):
    """A Validator component.


Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    A collection of an node's child elements.

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- adapter (dict; optional):
    An object that specifies what and when to validate, and how to
    apply the validation result.

- elementAttr (dict; optional):
    Specifies the global attributes to be attached to the UI
    component's container element.

- height (number | string; optional):
    Specifies the UI component's height.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer.

    `loading_state` is a dict with keys:

    - component_name (string; optional):
        Holds the name of the component that is loading.

    - is_loading (boolean; optional):
        Determines if the component is loading or not.

    - prop_name (string; optional):
        Holds which property is loading.

- name (string; optional):
    Specifies the editor name to be used in the validation default
    messages.

- validationGroup (string; optional):
    Specifies the validation group the editor will be related to.

- validationRules (list of dicts; optional):
    An array of validation rules to be checked for the editor with
    which the dxValidator object is associated.

- width (number | string; optional):
    Specifies the UI component's width."""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, adapter=Component.UNDEFINED, elementAttr=Component.UNDEFINED, height=Component.UNDEFINED, name=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onValidated=Component.UNDEFINED, validationGroup=Component.UNDEFINED, validationRules=Component.UNDEFINED, width=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'adapter', 'elementAttr', 'height', 'loading_state', 'name', 'validationGroup', 'validationRules', 'width']
        self._type = 'Validator'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'adapter', 'elementAttr', 'height', 'loading_state', 'name', 'validationGroup', 'validationRules', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Validator, self).__init__(children=children, **args)
