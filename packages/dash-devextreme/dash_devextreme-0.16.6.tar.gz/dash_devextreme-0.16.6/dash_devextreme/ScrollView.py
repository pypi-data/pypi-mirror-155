# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ScrollView(Component):
    """A ScrollView component.


Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    A collection of an node's child elements.

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- bounceEnabled (boolean; default False):
    A Boolean value specifying whether to enable or disable the
    bounce-back effect.

- direction (a value equal to: 'both', 'horizontal', 'vertical'; default 'vertical'):
    A string value specifying the available scrolling directions.

- disabled (boolean; default False):
    Specifies whether the UI component responds to user interaction.

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

- pulledDownText (string; default 'Release to refresh...'):
    Specifies the text shown in the pullDown panel when pulling the
    content down lowers the refresh threshold.

- pullingDownText (string; default 'Pull down to refresh...'):
    Specifies the text shown in the pullDown panel while pulling the
    content down to the refresh threshold.

- reachBottomText (string; default 'Loading...'):
    Specifies the text shown in the pullDown panel displayed when
    content is scrolled to the bottom.

- refreshingText (string; default 'Refreshing...'):
    Specifies the text shown in the pullDown panel displayed when the
    content is being refreshed.

- rtlEnabled (boolean; default False):
    Switches the UI component to a right-to-left representation.

- scrollByContent (boolean; default False):
    A Boolean value specifying whether or not an end-user can scroll
    the UI component content swiping it up or down. Applies only if
    useNative is False.

- scrollByThumb (boolean; default True):
    Specifies whether a user can scroll the content with the
    scrollbar. Applies only if useNative is False.

- showScrollbar (a value equal to: 'onScroll', 'onHover', 'always', 'never'; default 'onHover'):
    Specifies when the UI component shows the scrollbar.

- useNative (boolean; default False):
    Indicates whether to use native or simulated scrolling.

- width (number | string; optional):
    Specifies the UI component's width."""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, bounceEnabled=Component.UNDEFINED, direction=Component.UNDEFINED, disabled=Component.UNDEFINED, elementAttr=Component.UNDEFINED, height=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onPullDown=Component.UNDEFINED, onReachBottom=Component.UNDEFINED, onScroll=Component.UNDEFINED, onUpdated=Component.UNDEFINED, pulledDownText=Component.UNDEFINED, pullingDownText=Component.UNDEFINED, reachBottomText=Component.UNDEFINED, refreshingText=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, scrollByContent=Component.UNDEFINED, scrollByThumb=Component.UNDEFINED, showScrollbar=Component.UNDEFINED, useNative=Component.UNDEFINED, width=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'bounceEnabled', 'direction', 'disabled', 'elementAttr', 'height', 'loading_state', 'pulledDownText', 'pullingDownText', 'reachBottomText', 'refreshingText', 'rtlEnabled', 'scrollByContent', 'scrollByThumb', 'showScrollbar', 'useNative', 'width']
        self._type = 'ScrollView'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'bounceEnabled', 'direction', 'disabled', 'elementAttr', 'height', 'loading_state', 'pulledDownText', 'pullingDownText', 'reachBottomText', 'refreshingText', 'rtlEnabled', 'scrollByContent', 'scrollByThumb', 'showScrollbar', 'useNative', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(ScrollView, self).__init__(children=children, **args)
