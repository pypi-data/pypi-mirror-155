# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Tabs(Component):
    """A Tabs component.


Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- accessKey (string; optional):
    Specifies the shortcut key that sets focus on the UI component.

- dataSource (string | list of strings | list of dicts | dict; optional):
    Binds the UI component to data.

- disabled (boolean; default False):
    Specifies whether the UI component responds to user interaction.

- elementAttr (dict; optional):
    Specifies the global attributes to be attached to the UI
    component's container element.

- focusStateEnabled (boolean; default True):
    Specifies whether the UI component can be focused using keyboard
    navigation.

- height (number | string; default 'auto'):
    Specifies the UI component's height.

- hint (string; optional):
    Specifies text for a hint that appears when a user pauses on the
    UI component.

- hoverStateEnabled (boolean; default True):
    Specifies whether the UI component changes its state when a user
    pauses on it.

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

- keyExpr (string; optional):
    Specifies the key property that provides key values to access data
    items. Each key value must be unique.

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

- noDataText (string; default 'No data to display'):
    The text or HTML markup displayed by the UI component if the item
    collection is empty.

- onItemClick (string; optional):
    A function that is executed when a collection item is clicked or
    tapped.

- repaintChangesOnly (boolean; default False):
    Specifies whether to repaint only those elements whose data
    changed.

- rtlEnabled (boolean; default False):
    Switches the UI component to a right-to-left representation.

- scrollByContent (boolean; default False):
    Specifies whether or not an end-user can scroll tabs by swiping.

- scrollingEnabled (boolean; default True):
    Specifies whether or not an end-user can scroll tabs.

- selectedIndex (number; default 0):
    The index of the currently selected UI component item.

- selectedItem (dict; optional):
    The selected item object.

- selectedItemKeys (number; optional):
    Specifies an array of currently selected item keys.

- selectedItems (list of boolean | number | string | dict | lists; optional):
    An array of currently selected item objects.

- selectionMode (a value equal to: 'multiple', 'single'; default 'single'):
    Specifies whether the UI component enables an end-user to select
    only a single item or multiple items.

- showNavButtons (boolean; default True):
    Specifies whether navigation buttons should be available when tabs
    exceed the UI component's width.

- tabIndex (number; default 0):
    Specifies the number of the element when the Tab key is used for
    navigating.

- visible (boolean; default True):
    Specifies whether the UI component is visible.

- width (number | string; default 'auto'):
    Specifies the UI component's width."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, accessKey=Component.UNDEFINED, dataSource=Component.UNDEFINED, disabled=Component.UNDEFINED, elementAttr=Component.UNDEFINED, focusStateEnabled=Component.UNDEFINED, height=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, itemClick=Component.UNDEFINED, itemComponent=Component.UNDEFINED, itemHoldTimeout=Component.UNDEFINED, itemRender=Component.UNDEFINED, items=Component.UNDEFINED, itemTemplate=Component.UNDEFINED, keyExpr=Component.UNDEFINED, noDataText=Component.UNDEFINED, onContentReady=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onItemClick=Component.UNDEFINED, onItemContextMenu=Component.UNDEFINED, onItemHold=Component.UNDEFINED, onItemRendered=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onSelectionChanged=Component.UNDEFINED, repaintChangesOnly=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, scrollByContent=Component.UNDEFINED, scrollingEnabled=Component.UNDEFINED, selectedIndex=Component.UNDEFINED, selectedItem=Component.UNDEFINED, selectedItemKeys=Component.UNDEFINED, selectedItems=Component.UNDEFINED, selectionMode=Component.UNDEFINED, showNavButtons=Component.UNDEFINED, tabIndex=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'accessKey', 'dataSource', 'disabled', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'itemClick', 'itemComponent', 'itemHoldTimeout', 'itemRender', 'itemTemplate', 'items', 'keyExpr', 'loading_state', 'noDataText', 'onItemClick', 'repaintChangesOnly', 'rtlEnabled', 'scrollByContent', 'scrollingEnabled', 'selectedIndex', 'selectedItem', 'selectedItemKeys', 'selectedItems', 'selectionMode', 'showNavButtons', 'tabIndex', 'visible', 'width']
        self._type = 'Tabs'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'accessKey', 'dataSource', 'disabled', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'itemClick', 'itemComponent', 'itemHoldTimeout', 'itemRender', 'itemTemplate', 'items', 'keyExpr', 'loading_state', 'noDataText', 'onItemClick', 'repaintChangesOnly', 'rtlEnabled', 'scrollByContent', 'scrollingEnabled', 'selectedIndex', 'selectedItem', 'selectedItemKeys', 'selectedItems', 'selectionMode', 'showNavButtons', 'tabIndex', 'visible', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Tabs, self).__init__(**args)
