# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Gallery(Component):
    """A Gallery component.


Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- accessKey (string; optional):
    Specifies the shortcut key that sets focus on the UI component.

- animationDuration (number; default 400):
    The time, in milliseconds, spent on slide animation.

- animationEnabled (boolean; default True):
    Specifies whether or not to animate the displayed item change.

- dataSource (dict | list of strings | list of dicts; optional):
    Binds the UI component to data.

- disabled (boolean; default False):
    Specifies whether the UI component responds to user interaction.

- elementAttr (dict; optional):
    Specifies the global attributes to be attached to the UI
    component's container element.

- focusStateEnabled (boolean; default True):
    Specifies whether the UI component can be focused using keyboard
    navigation.

- height (number | string; optional):
    Specifies the UI component's height.

- hint (string; optional):
    Specifies text for a hint that appears when a user pauses on the
    UI component.

- hoverStateEnabled (boolean; default False):
    Specifies whether the UI component changes its state when a user
    pauses on it.

- indicatorEnabled (boolean; default True):
    A Boolean value specifying whether or not to allow users to switch
    between items by clicking an indicator.

- initialItemWidth (number; optional):
    Specifies the width of an area used to display a single image.

- itemClick (dict; optional):
    Dash event.

- itemComponent (string | dict; optional):
    An alias for the itemTemplate property specified in React. Accepts
    a custom component.

- itemHoldTimeout (number; default 750):
    The time period in milliseconds before the onItemHold event is
    raised.

- itemRender (string; optional):
    An alias for the itemTemplate property specified in React. Accepts
    a rendering function.

- itemTemplate (string | dict; default 'item'):
    Specifies a custom template for items.

- items (list of strings | list of dicts; optional):
    An array of items displayed by the UI component.

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

- loop (boolean; default True):
    A Boolean value specifying whether or not to scroll back to the
    first item after the last item is swiped.

- noDataText (string; default 'No data to display'):
    The text or HTML markup displayed by the UI component if the item
    collection is empty.

- rtlEnabled (boolean; default False):
    Switches the UI component to a right-to-left representation.

- selectedIndex (number; default 0):
    The index of the currently active gallery item.

- selectedItem (dict; optional):
    The selected item object.

- selectionChanged (dict; optional):
    Dash event.

- showIndicator (boolean; default True):
    A Boolean value specifying whether or not to display an indicator
    that points to the selected gallery item.

- showNavButtons (boolean; default True):
    A Boolean value that specifies the availability of the \"Forward\"
    and \"Back\" navigation buttons.

- slideshowDelay (number; default 0):
    The time interval in milliseconds, after which the gallery
    switches to the next item.

- stretchImages (boolean; default False):
    Specifies if the UI component stretches images to fit the total
    gallery width.

- swipeEnabled (boolean; default True):
    A Boolean value specifying whether or not to allow users to switch
    between items by swiping.

- tabIndex (number; default 0):
    Specifies the number of the element when the Tab key is used for
    navigating.

- visible (boolean; default True):
    Specifies whether the UI component is visible.

- width (number | string; optional):
    Specifies the UI component's width.

- wrapAround (boolean; default False):
    Specifies whether or not to display parts of previous and next
    images along the sides of the current image."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, accessKey=Component.UNDEFINED, animationDuration=Component.UNDEFINED, animationEnabled=Component.UNDEFINED, dataSource=Component.UNDEFINED, disabled=Component.UNDEFINED, elementAttr=Component.UNDEFINED, focusStateEnabled=Component.UNDEFINED, height=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, indicatorEnabled=Component.UNDEFINED, initialItemWidth=Component.UNDEFINED, itemComponent=Component.UNDEFINED, itemHoldTimeout=Component.UNDEFINED, itemClick=Component.UNDEFINED, itemRender=Component.UNDEFINED, items=Component.UNDEFINED, itemTemplate=Component.UNDEFINED, loop=Component.UNDEFINED, noDataText=Component.UNDEFINED, onContentReady=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onItemClick=Component.UNDEFINED, onItemContextMenu=Component.UNDEFINED, onItemHold=Component.UNDEFINED, onItemRendered=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onSelectionChanged=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, selectedIndex=Component.UNDEFINED, selectedItem=Component.UNDEFINED, selectionChanged=Component.UNDEFINED, showIndicator=Component.UNDEFINED, showNavButtons=Component.UNDEFINED, slideshowDelay=Component.UNDEFINED, stretchImages=Component.UNDEFINED, swipeEnabled=Component.UNDEFINED, tabIndex=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, wrapAround=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'accessKey', 'animationDuration', 'animationEnabled', 'dataSource', 'disabled', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'indicatorEnabled', 'initialItemWidth', 'itemClick', 'itemComponent', 'itemHoldTimeout', 'itemRender', 'itemTemplate', 'items', 'loading_state', 'loop', 'noDataText', 'rtlEnabled', 'selectedIndex', 'selectedItem', 'selectionChanged', 'showIndicator', 'showNavButtons', 'slideshowDelay', 'stretchImages', 'swipeEnabled', 'tabIndex', 'visible', 'width', 'wrapAround']
        self._type = 'Gallery'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'accessKey', 'animationDuration', 'animationEnabled', 'dataSource', 'disabled', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'indicatorEnabled', 'initialItemWidth', 'itemClick', 'itemComponent', 'itemHoldTimeout', 'itemRender', 'itemTemplate', 'items', 'loading_state', 'loop', 'noDataText', 'rtlEnabled', 'selectedIndex', 'selectedItem', 'selectionChanged', 'showIndicator', 'showNavButtons', 'slideshowDelay', 'stretchImages', 'swipeEnabled', 'tabIndex', 'visible', 'width', 'wrapAround']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Gallery, self).__init__(**args)
