# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DropDownButton(Component):
    """A DropDownButton component.


Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- accessKey (string; optional):
    Specifies the shortcut key that sets focus on the UI component.

- activeStateEnabled (boolean; default False):
    Specifies whether or not the UI component changes its state when
    interacting with a user.

- dataSource (string | list of strings | list of dicts | dict; optional):
    Provides data for the drop-down menu.

- deferRendering (boolean; default True):
    Specifies whether to wait until the drop-down menu is opened the
    first time to render its content.

- disabled (boolean; default False):
    Specifies whether the UI component responds to user interaction.

- displayExpr (string; default 'this'):
    Specifies the data field whose values should be displayed in the
    drop-down menu.

- dropDownContentComponent (string | dict; optional):
    An alias for the dropDownContentTemplate property specified in
    React. Accepts a custom component.

- dropDownContentRender (string; optional):
    An alias for the dropDownContentTemplate property specified in
    React. Accepts a rendering function.

- dropDownContentTemplate (string | dict; default 'content'):
    Specifies custom content for the drop-down field.

- dropDownOptions (dict; optional):
    Configures the drop-down field.

- elementAttr (dict; optional):
    Specifies the global attributes to be attached to the UI
    component's container element.

- focusStateEnabled (boolean; default True):
    Specifies whether users can use keyboard to focus the UI
    component.

- height (number | string; optional):
    Specifies the UI component's height.

- hint (string; optional):
    Specifies text for a hint that appears when a user pauses on the
    UI component.

- hoverStateEnabled (boolean; default True):
    Specifies whether the UI component changes its state when a user
    hovers the mouse pointer over it.

- icon (string; optional):
    Specifies the button's icon.

- itemComponent (string | dict; optional):
    An alias for the itemTemplate property specified in React. Accepts
    a custom component.

- itemRender (string; optional):
    An alias for the itemTemplate property specified in React. Accepts
    a rendering function.

- itemTemplate (string | dict; default 'item'):
    Specifies a custom template for drop-down menu items.

- items (list of strings | list of dicts; optional):
    Provides drop-down menu items.

- keyExpr (string; default 'this'):
    Specifies which data field provides keys used to distinguish
    between the selected drop-down menu items.

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
    Specifies text or HTML markup displayed in the drop-down menu when
    it does not contain any items.

- onItemClick (string; optional):
    A function that is executed when a drop-down menu item is clicked.

- onSelectionChanged (string; optional):
    A function that is executed when an item is selected or selection
    is canceled. In effect when useSelectMode is True.

- opened (boolean; default False):
    Specifies whether the drop-down menu is opened.

- rtlEnabled (boolean; default False):
    Switches the UI component to a right-to-left representation.

- selectedItem (string | number | dict; optional):
    Contains the selected item's data. Available when useSelectMode is
    True. Read only.

- selectedItemKey (string | number; default 1):
    Contains the selected item's key and allows you to specify the
    initially selected item. Applies when useSelectMode is True.

- showArrowIcon (boolean; default True):
    Specifies whether the arrow icon should be displayed.

- splitButton (boolean; default False):
    Specifies whether to split the button in two: one executes an
    action, the other opens and closes the drop-down menu.

- stylingMode (string; default 'text'):
    Specifies how the button is styled.

- tabIndex (number; default 0):
    Specifies the number of the element when the Tab key is used for
    navigating.

- text (string; default ''):
    Specifies the button's text. Applies only if useSelectMode is
    False.

- useSelectMode (boolean; default True):
    Specifies whether the UI component stores the selected drop-down
    menu item.

- visible (boolean; default True):
    Specifies whether the UI component is visible.

- width (number | string; optional):
    Specifies the UI component's width.

- wrapItemText (boolean; default False):
    Specifies whether text that exceeds the drop-down list width
    should be wrapped."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, accessKey=Component.UNDEFINED, activeStateEnabled=Component.UNDEFINED, dataSource=Component.UNDEFINED, deferRendering=Component.UNDEFINED, disabled=Component.UNDEFINED, displayExpr=Component.UNDEFINED, dropDownContentComponent=Component.UNDEFINED, dropDownContentRender=Component.UNDEFINED, dropDownContentTemplate=Component.UNDEFINED, dropDownOptions=Component.UNDEFINED, elementAttr=Component.UNDEFINED, focusStateEnabled=Component.UNDEFINED, height=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, icon=Component.UNDEFINED, itemComponent=Component.UNDEFINED, itemRender=Component.UNDEFINED, items=Component.UNDEFINED, itemTemplate=Component.UNDEFINED, keyExpr=Component.UNDEFINED, noDataText=Component.UNDEFINED, onButtonClick=Component.UNDEFINED, onContentReady=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onItemClick=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onSelectionChanged=Component.UNDEFINED, opened=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, selectedItem=Component.UNDEFINED, selectedItemKey=Component.UNDEFINED, showArrowIcon=Component.UNDEFINED, splitButton=Component.UNDEFINED, stylingMode=Component.UNDEFINED, tabIndex=Component.UNDEFINED, text=Component.UNDEFINED, useSelectMode=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, wrapItemText=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'accessKey', 'activeStateEnabled', 'dataSource', 'deferRendering', 'disabled', 'displayExpr', 'dropDownContentComponent', 'dropDownContentRender', 'dropDownContentTemplate', 'dropDownOptions', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'icon', 'itemComponent', 'itemRender', 'itemTemplate', 'items', 'keyExpr', 'loading_state', 'noDataText', 'onItemClick', 'onSelectionChanged', 'opened', 'rtlEnabled', 'selectedItem', 'selectedItemKey', 'showArrowIcon', 'splitButton', 'stylingMode', 'tabIndex', 'text', 'useSelectMode', 'visible', 'width', 'wrapItemText']
        self._type = 'DropDownButton'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'accessKey', 'activeStateEnabled', 'dataSource', 'deferRendering', 'disabled', 'displayExpr', 'dropDownContentComponent', 'dropDownContentRender', 'dropDownContentTemplate', 'dropDownOptions', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'icon', 'itemComponent', 'itemRender', 'itemTemplate', 'items', 'keyExpr', 'loading_state', 'noDataText', 'onItemClick', 'onSelectionChanged', 'opened', 'rtlEnabled', 'selectedItem', 'selectedItemKey', 'showArrowIcon', 'splitButton', 'stylingMode', 'tabIndex', 'text', 'useSelectMode', 'visible', 'width', 'wrapItemText']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DropDownButton, self).__init__(**args)
