# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class LoadPanel(Component):
    """A LoadPanel component.


Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- animation (dict; default {show: {type: 'fade', from: 0, to: 1}, hide: {type: 'fade', to: 0}}):
    Configures UI component visibility animations. This object
    contains two fields: show and hide.

- closeOnOutsideClick (boolean; default True):
    Specifies whether to close the UI component if a user clicks
    outside it.

- container (string; optional):
    Specifies the UI component's container.

- deferRendering (boolean; default True):
    Specifies whether to render the UI component's content when it is
    displayed. If False, the content is rendered immediately.

- delay (number; default 0):
    The delay in milliseconds after which the load panel is displayed.

- elementAttr (dict; optional):
    Specifies the global attributes to be attached to the UI
    component's container element.

- focusStateEnabled (boolean; default False):
    Specifies whether or not the UI component can be focused.

- height (number | string; default 90):
    Specifies the UI component's height in pixels.

- hint (string; optional):
    Specifies text for a hint that appears when a user pauses on the
    UI component.

- hoverStateEnabled (boolean; default False):
    Specifies whether the UI component changes its state when a user
    pauses on it.

- indicatorSrc (string; default ''):
    A URL pointing to an image to be used as a load indicator.

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

- maxHeight (number | string; optional):
    Specifies the maximum height the UI component can reach while
    resizing.

- maxWidth (number | string; optional):
    Specifies the maximum width the UI component can reach while
    resizing.

- message (string; default 'Loading...'):
    Specifies the text displayed in the load panel. Ignored in the
    Material Design theme.

- minHeight (number | string; optional):
    Specifies the minimum height the UI component can reach while
    resizing.

- minWidth (number | string; optional):
    Specifies the minimum width the UI component can reach while
    resizing.

- position (a value equal to: 'bottom', 'center', 'left', 'left bottom', 'left top', 'right', 'right bottom', 'right top', 'top' | dict; default {my: 'center', at: 'center', of: window}):
    Positions the UI component.

- rtlEnabled (boolean; default False):
    Switches the UI component to a right-to-left representation.

- shading (boolean; default True):
    Specifies whether to shade the background when the UI component is
    active.

- shadingColor (string; default 'transparent'):
    Specifies the shading color. Applies only if shading is enabled.

- showIndicator (boolean; default True):
    A Boolean value specifying whether or not to show a load
    indicator.

- showPane (boolean; default True):
    A Boolean value specifying whether or not to show the pane behind
    the load indicator.

- visible (boolean; default False):
    A Boolean value specifying whether or not the UI component is
    visible.

- width (number | string; default 222):
    Specifies the UI component's width in pixels."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, animation=Component.UNDEFINED, closeOnOutsideClick=Component.UNDEFINED, container=Component.UNDEFINED, deferRendering=Component.UNDEFINED, delay=Component.UNDEFINED, elementAttr=Component.UNDEFINED, focusStateEnabled=Component.UNDEFINED, height=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, indicatorSrc=Component.UNDEFINED, maxHeight=Component.UNDEFINED, maxWidth=Component.UNDEFINED, message=Component.UNDEFINED, minHeight=Component.UNDEFINED, minWidth=Component.UNDEFINED, onContentReady=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onHidden=Component.UNDEFINED, onHiding=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onShowing=Component.UNDEFINED, onShown=Component.UNDEFINED, position=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, shading=Component.UNDEFINED, shadingColor=Component.UNDEFINED, showIndicator=Component.UNDEFINED, showPane=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'animation', 'closeOnOutsideClick', 'container', 'deferRendering', 'delay', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'indicatorSrc', 'loading_state', 'maxHeight', 'maxWidth', 'message', 'minHeight', 'minWidth', 'position', 'rtlEnabled', 'shading', 'shadingColor', 'showIndicator', 'showPane', 'visible', 'width']
        self._type = 'LoadPanel'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'animation', 'closeOnOutsideClick', 'container', 'deferRendering', 'delay', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'indicatorSrc', 'loading_state', 'maxHeight', 'maxWidth', 'message', 'minHeight', 'minWidth', 'position', 'rtlEnabled', 'shading', 'shadingColor', 'showIndicator', 'showPane', 'visible', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(LoadPanel, self).__init__(**args)
