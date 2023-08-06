# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class SimpleBoxView(Component):
    """A SimpleBoxView component.


Keyword arguments:

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- boxClick (dict; optional):
    Dash event.

- boxTemplate (string; default undefined):
    An alias for the rowTemplate property specified in React. Accepts
    a rendering function.

- className (string; default 'simple-box-view'):
    The class of the parent element.

- dataSource (dict | list of dicts; optional):
    Binds the UI component to data.

- elementAttr (dict; optional):
    Specifies the global attributes to be attached to the UI
    component's container element.

- filterValue (dict | list; optional):
    Specifies a filter expression.

- height (number | string; optional):
    Specifies the UI component's height.

- keyExpr (string | list of strings; default 'id'):
    Specifies the key property (or properties) that provide(s) key
    values to access data items. Each key value must be unique. This
    property applies only if data is a simple array.

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

- onBoxClick (string; optional):
    A function that is executed when a box is clicked or tapped.

- style (dict; optional):
    The input's inline styles.

- valueExpr (string; optional):
    Specifies which data field provides unique values to the UI
    component's value.

- width (number | string; optional):
    Specifies the UI component's width."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, boxClick=Component.UNDEFINED, boxTemplate=Component.UNDEFINED, className=Component.UNDEFINED, dataSource=Component.UNDEFINED, elementAttr=Component.UNDEFINED, filterValue=Component.UNDEFINED, height=Component.UNDEFINED, keyExpr=Component.UNDEFINED, onBoxClick=Component.UNDEFINED, style=Component.UNDEFINED, valueExpr=Component.UNDEFINED, width=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'boxClick', 'boxTemplate', 'className', 'dataSource', 'elementAttr', 'filterValue', 'height', 'keyExpr', 'loading_state', 'onBoxClick', 'style', 'valueExpr', 'width']
        self._type = 'SimpleBoxView'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'boxClick', 'boxTemplate', 'className', 'dataSource', 'elementAttr', 'filterValue', 'height', 'keyExpr', 'loading_state', 'onBoxClick', 'style', 'valueExpr', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(SimpleBoxView, self).__init__(**args)
