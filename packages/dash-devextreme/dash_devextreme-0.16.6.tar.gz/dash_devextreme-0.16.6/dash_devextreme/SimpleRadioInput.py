# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class SimpleRadioInput(Component):
    """A SimpleRadioInput component.


Keyword arguments:

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- autoComplete (string; optional):
    This attribute indicates whether the value of the control can be
    automatically completed by the browser.

- autoFocus (a value equal to: 'autoFocus', 'autofocus', 'AUTOFOCUS' | boolean; optional):
    The element should be automatically focused after the page loaded.
    autoFocus is an HTML boolean attribute - it is enabled by a
    boolean or 'autoFocus'. Alternative capitalizations `autofocus` &
    `AUTOFOCUS` are also acccepted.

- checked (boolean; optional)

- className (string; optional):
    The class of the input element.

- defaultChecked (boolean; optional)

- disabled (a value equal to: 'disabled', 'DISABLED' | boolean; optional):
    If True, the input is disabled and can't be clicked on. disabled
    is an HTML boolean attribute - it is enabled by a boolean or
    'disabled'. Alternative capitalizations `DISABLED`.

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
    The name of the control, which is submitted with the form data.

- pattern (string; optional):
    A regular expression that the control's value is checked against.
    The pattern must match the entire value, not just some subset. Use
    the title attribute to describe the pattern to help the user. This
    attribute applies when the value of the type attribute is text,
    search, tel, url, email, or password, otherwise it is ignored. The
    regular expression language is the same as JavaScript RegExp
    algorithm, with the 'u' parameter that makes it treat the pattern
    as a sequence of unicode code points. The pattern is not
    surrounded by forward slashes.

- persisted_props (list of a value equal to: 'value's; default ['value']):
    Properties whose user interactions will persist after refreshing
    the component or the page. Since only `value` is allowed this prop
    can normally be ignored.

- persistence (boolean | string | number; optional):
    Used to allow user interactions in this component to be persisted
    when the component - or the page - is refreshed. If `persisted` is
    truthy and hasn't changed from its previous value, a `value` that
    the user has changed while using the app will keep that change, as
    long as the new `value` also matches what was given originally.
    Used in conjunction with `persistence_type`.

- persistence_type (a value equal to: 'local', 'session', 'memory'; default 'local'):
    Where persisted user changes will be stored: memory: only kept in
    memory, reset on page refresh. local: window.localStorage, data is
    kept after the browser quit. session: window.sessionStorage, data
    is cleared once the browser quit.

- readOnly (boolean | a value equal to: 'readOnly', 'readonly', 'READONLY'; optional):
    This attribute indicates that the user cannot modify the value of
    the control. The value of the attribute is irrelevant. If you need
    read-write access to the input value, do not add the \"readonly\"
    attribute. It is ignored if the value of the type attribute is
    hidden, range, color, checkbox, radio, file, or a button type
    (such as button or submit). readOnly is an HTML boolean attribute
    - it is enabled by a boolean or 'readOnly'. Alternative
    capitalizations `readonly` & `READONLY` are also acccepted.

- required (a value equal to: 'required', 'REQUIRED' | boolean; optional):
    This attribute specifies that the user must fill in a value before
    submitting a form. It cannot be used when the type attribute is
    hidden, image, or a button type (submit, reset, or button). The
    :optional and :required CSS pseudo-classes will be applied to the
    field as appropriate. required is an HTML boolean attribute - it
    is enabled by a boolean or 'required'. Alternative capitalizations
    `REQUIRED` are also acccepted.

- style (dict; optional):
    The input's inline styles.

- value (string | number; optional):
    The value of the input."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, value=Component.UNDEFINED, style=Component.UNDEFINED, checked=Component.UNDEFINED, defaultChecked=Component.UNDEFINED, className=Component.UNDEFINED, autoComplete=Component.UNDEFINED, autoFocus=Component.UNDEFINED, disabled=Component.UNDEFINED, name=Component.UNDEFINED, pattern=Component.UNDEFINED, readOnly=Component.UNDEFINED, required=Component.UNDEFINED, loading_state=Component.UNDEFINED, persistence=Component.UNDEFINED, persisted_props=Component.UNDEFINED, persistence_type=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'autoComplete', 'autoFocus', 'checked', 'className', 'defaultChecked', 'disabled', 'loading_state', 'name', 'pattern', 'persisted_props', 'persistence', 'persistence_type', 'readOnly', 'required', 'style', 'value']
        self._type = 'SimpleRadioInput'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'autoComplete', 'autoFocus', 'checked', 'className', 'defaultChecked', 'disabled', 'loading_state', 'name', 'pattern', 'persisted_props', 'persistence', 'persistence_type', 'readOnly', 'required', 'style', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(SimpleRadioInput, self).__init__(**args)
