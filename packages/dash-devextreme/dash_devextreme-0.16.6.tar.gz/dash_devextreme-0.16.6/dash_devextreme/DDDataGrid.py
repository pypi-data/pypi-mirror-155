# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DDDataGrid(Component):
    """A DDDataGrid component.


Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- accessKey (string; optional):
    Specifies the shortcut key that sets focus on the UI component.

- activeStateEnabled (boolean; default False):
    Specifies whether or not the UI component changes its state when
    interacting with a user.

- addDroppedRow (dict; optional):
    Dash event.

- allowColumnReordering (boolean; default False):
    Specifies whether a user can reorder columns.

- allowColumnResizing (boolean; default False):
    Specifies whether a user can resize columns.

- autoNavigateToFocusedRow (boolean; default True):
    Automatically scrolls to the focused row when the focusedRowKey is
    changed.

- cacheEnabled (boolean; default True):
    Specifies whether data should be cached.

- cellClick (dict; optional):
    Dash event.

- cellHintEnabled (boolean; default True):
    Enables a hint that appears when a user hovers the mouse pointer
    over a cell with truncated content.

- columnAutoWidth (boolean; default False):
    Specifies whether columns should adjust their widths to the
    content.

- columnChooser (dict; optional):
    Configures the column chooser.

- columnFixing (dict; optional):
    Configures column fixing.

- columnHidingEnabled (boolean; default False):
    Specifies whether the UI component should hide columns to adapt to
    the screen or container size. Ignored if allowColumnResizing is
    True and columnResizingMode is \"widget\".

- columnMinWidth (number; optional):
    Specifies the minimum width of columns.

- columnResizingMode (a value equal to: 'nextColumn', 'widget'; default 'nextColumn'):
    Specifies how the UI component resizes columns. Applies only if
    allowColumnResizing is True.

- columnWidth (number; optional):
    Specifies the width for all data columns. Has a lower priority
    than the column.width property.

- columns (list of dicts; optional):
    An array of grid columns.

- columnsUpdateOption (dict; optional):
    Dash option to update column options.

- dataSource (dict | list of dicts; optional):
    Binds the UI component to data.

- dateSerializationFormat (string; optional):
    Specifies the format in which date-time values should be sent to
    the server. Use it only if you do not specify the dataSource at
    design time.

- defaultSelectedRowKeys (list of boolean | number | string | dict | lists; optional):
    Allows you to select rows or determine which rows are selected.

- disabled (boolean; default False):
    Specifies whether the UI component responds to user interaction.

- dragClone (dict; optional):
    Dash event.

- dragRemove (dict; optional):
    Dash event.

- dragStart (dict; optional):
    Dash event.

- dropAdd (dict; optional):
    Dash event.

- editing (dict; optional):
    Configures editing.

- elementAttr (dict; optional):
    Specifies the global attributes to be attached to the UI
    component's container element.

- errorRowEnabled (boolean; default True):
    Indicates whether to show the error row.

- export (dict; optional):
    Configures client-side exporting.

- filterBuilder (dict; optional):
    Configures the integrated filter builder.

- filterBuilderPopup (dict; optional):
    Configures the popup in which the integrated filter builder is
    shown.

- filterPanel (dict; optional):
    Configures the filter panel.

- filterRow (dict; optional):
    Configures the filter row.

- filterSyncEnabled (boolean; optional):
    Specifies whether to synchronize the filter row, header filter,
    and filter builder. The synchronized filter expression is stored
    in the filterValue property.

- filterValue (dict | list; optional):
    Specifies a filter expression.

- focusStateEnabled (boolean; default False):
    Specifies whether the UI component can be focused using keyboard
    navigation.

- focusedColumnIndex (number; default -1):
    The index of the column that contains the focused data cell. This
    index is taken from the columns array.

- focusedRowEnabled (boolean; default False):
    Specifies whether the focused row feature is enabled.

- focusedRowIndex (number; default -1):
    Specifies or indicates the focused data row's index. Use this
    property when focusedRowEnabled is True.

- focusedRowKey (boolean | number | string | dict | list; optional):
    Specifies initially or currently focused grid row's key. Use it
    when focusedRowEnabled is True.

- groupPanel (dict; optional):
    Configures the group panel.

- grouping (dict; optional):
    Configures grouping.

- headerFilter (dict; optional):
    Configures the header filter feature.

- height (number | string; optional):
    Specifies the UI component's height.

- highlightChanges (boolean; default False):
    Specifies whether to highlight rows and cells with edited data.
    repaintChangesOnly should be True.

- hint (string; optional):
    Specifies text for a hint that appears when a user pauses on the
    UI component.

- hoverStateEnabled (boolean; default False):
    Specifies whether to highlight rows when a user moves the mouse
    pointer over them.

- keyExpr (string | list of strings; optional):
    Specifies the key property (or properties) that provide(s) key
    values to access data items. Each key value must be unique. This
    property applies only if data is a simple array.

- keyboardNavigation (dict; optional):
    Configures keyboard navigation.

- loadPanel (dict; optional):
    Configures the load panel.

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

- masterDetail (dict; optional):
    Allows you to build a master-detail interface in the grid.

- noDataText (string; default 'No data'):
    Specifies text shown when the UI component does not display any
    data.

- onCellClick (string; optional):
    A function that is executed when a cell is clicked or tapped.
    Executed before onRowClick.

- onRowClick (string; optional):
    A function that is executed when a row is clicked or tapped.

- pager (dict; optional):
    Configures the pager.

- paging (dict; optional):
    Configures paging.

- remoteOperations (boolean | dict; optional):
    Notifies the DataGrid of the server's data processing operations.

- removeDroppedRow (dict; optional):
    Dash event.

- renderAsync (boolean; default False):
    Specifies whether to render the filter row, command columns, and
    columns with showEditorAlways set to True after other elements.

- repaintChangesOnly (boolean; default False):
    Specifies whether to repaint only those cells whose data changed.

- rowAlternationEnabled (boolean; default False):
    Specifies whether rows should be shaded differently.

- rowClick (dict; optional):
    Dash event.

- rowComponent (string; optional):
    An alias for the rowTemplate property specified in React. Accepts
    a custom component.

- rowDblClick (dict; optional):
    Dash event.

- rowDragging (dict; optional):
    Configures row reordering using drag and drop gestures.

- rowRemoved (dict; optional):
    Dash event.

- rowRemoving (dict; optional):
    Dash event.

- rowTemplate (string; optional):
    An alias for the rowTemplate property specified in React. Accepts
    a rendering function.

- rowUpdated (dict; optional):
    Dash event.

- rowUpdating (dict; optional):
    Dash event.

- rtlEnabled (boolean; default False):
    Switches the UI component to a right-to-left representation.

- scrolling (dict; optional):
    Configures scrolling.

- searchPanel (dict; optional):
    Configures the search panel.

- selectedRowKeys (list of boolean | number | string | dict | lists; optional):
    Allows you to select rows or determine which rows are selected.
    Applies only if selection.deferred is False.

- selection (dict; optional):
    Configures runtime selection.

- selectionFilter (list; optional):
    Specifies filters for the rows that must be selected initially.
    Applies only if selection.deferred is True.

- showBorders (boolean; default False):
    Specifies whether the outer borders of the UI component are
    visible.

- showColumnHeaders (boolean; default True):
    Specifies whether column headers are visible.

- showColumnLines (boolean; default True):
    Specifies whether vertical lines that separate one column from
    another are visible.

- showRowLines (boolean; default False):
    Specifies whether horizontal lines that separate one row from
    another are visible.

- sortByGroupSummaryInfo (list of dicts; optional):
    Allows you to sort groups according to the values of group summary
    items.

- sorting (dict; optional):
    Configures runtime sorting.

- stateStoring (dict; optional):
    Configures state storing.

- summary (dict; optional):
    Specifies the properties of the grid summary.

- tabIndex (number; default 0):
    Specifies the number of the element when the Tab key is used for
    navigating.

- twoWayBindingEnabled (boolean; default True):
    Specifies whether to enable two-way data binding.

- visible (boolean; default True):
    Specifies whether the UI component is visible.

- width (number | string; optional):
    Specifies the UI component's width.

- wordWrapEnabled (boolean; default False):
    Specifies whether text that does not fit into a column should be
    wrapped."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, accessKey=Component.UNDEFINED, activeStateEnabled=Component.UNDEFINED, addDroppedRow=Component.UNDEFINED, allowColumnReordering=Component.UNDEFINED, allowColumnResizing=Component.UNDEFINED, autoNavigateToFocusedRow=Component.UNDEFINED, cacheEnabled=Component.UNDEFINED, cellClick=Component.UNDEFINED, cellHintEnabled=Component.UNDEFINED, columnAutoWidth=Component.UNDEFINED, columnChooser=Component.UNDEFINED, columnFixing=Component.UNDEFINED, columnHidingEnabled=Component.UNDEFINED, columnMinWidth=Component.UNDEFINED, columnResizingMode=Component.UNDEFINED, columns=Component.UNDEFINED, columnsUpdateOption=Component.UNDEFINED, columnWidth=Component.UNDEFINED, customizeColumns=Component.UNDEFINED, dataSource=Component.UNDEFINED, dateSerializationFormat=Component.UNDEFINED, defaultSelectedRowKeys=Component.UNDEFINED, disabled=Component.UNDEFINED, dragClone=Component.UNDEFINED, dragRemove=Component.UNDEFINED, dragStart=Component.UNDEFINED, dropAdd=Component.UNDEFINED, editing=Component.UNDEFINED, elementAttr=Component.UNDEFINED, errorRowEnabled=Component.UNDEFINED, export=Component.UNDEFINED, filterBuilder=Component.UNDEFINED, filterBuilderPopup=Component.UNDEFINED, filterPanel=Component.UNDEFINED, filterRow=Component.UNDEFINED, filterSyncEnabled=Component.UNDEFINED, filterValue=Component.UNDEFINED, focusedColumnIndex=Component.UNDEFINED, focusedRowEnabled=Component.UNDEFINED, focusedRowIndex=Component.UNDEFINED, focusedRowKey=Component.UNDEFINED, focusStateEnabled=Component.UNDEFINED, grouping=Component.UNDEFINED, groupPanel=Component.UNDEFINED, headerFilter=Component.UNDEFINED, height=Component.UNDEFINED, highlightChanges=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, keyboardNavigation=Component.UNDEFINED, keyExpr=Component.UNDEFINED, loadPanel=Component.UNDEFINED, masterDetail=Component.UNDEFINED, noDataText=Component.UNDEFINED, onAdaptiveDetailRowPreparing=Component.UNDEFINED, onCellClick=Component.UNDEFINED, onCellDblClick=Component.UNDEFINED, onCellHoverChanged=Component.UNDEFINED, onCellPrepared=Component.UNDEFINED, onContentReady=Component.UNDEFINED, onContextMenuPreparing=Component.UNDEFINED, onDataErrorOccurred=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onEditCanceled=Component.UNDEFINED, onEditCanceling=Component.UNDEFINED, onEditingStart=Component.UNDEFINED, onEditorPrepared=Component.UNDEFINED, onEditorPreparing=Component.UNDEFINED, onExporting=Component.UNDEFINED, onFocusedCellChanged=Component.UNDEFINED, onFocusedCellChanging=Component.UNDEFINED, onFocusedRowChanged=Component.UNDEFINED, onFocusedRowChanging=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onInitNewRow=Component.UNDEFINED, onKeyDown=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onRowClick=Component.UNDEFINED, onRowCollapsed=Component.UNDEFINED, onRowCollapsing=Component.UNDEFINED, onRowDblClick=Component.UNDEFINED, onRowExpanded=Component.UNDEFINED, onRowExpanding=Component.UNDEFINED, onRowInserted=Component.UNDEFINED, onRowInserting=Component.UNDEFINED, onRowPrepared=Component.UNDEFINED, onRowRemoved=Component.UNDEFINED, onRowRemoving=Component.UNDEFINED, onRowUpdated=Component.UNDEFINED, onRowUpdating=Component.UNDEFINED, onRowValidating=Component.UNDEFINED, onSaved=Component.UNDEFINED, onSaving=Component.UNDEFINED, onSelectionChanged=Component.UNDEFINED, onToolbarPreparing=Component.UNDEFINED, pager=Component.UNDEFINED, paging=Component.UNDEFINED, remoteOperations=Component.UNDEFINED, removeDroppedRow=Component.UNDEFINED, renderAsync=Component.UNDEFINED, repaintChangesOnly=Component.UNDEFINED, rowAlternationEnabled=Component.UNDEFINED, rowClick=Component.UNDEFINED, rowDblClick=Component.UNDEFINED, rowRemoved=Component.UNDEFINED, rowRemoving=Component.UNDEFINED, rowUpdated=Component.UNDEFINED, rowUpdating=Component.UNDEFINED, rowComponent=Component.UNDEFINED, rowDragging=Component.UNDEFINED, rowTemplate=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, scrolling=Component.UNDEFINED, searchPanel=Component.UNDEFINED, selectedRowKeys=Component.UNDEFINED, selection=Component.UNDEFINED, selectionFilter=Component.UNDEFINED, showBorders=Component.UNDEFINED, showColumnHeaders=Component.UNDEFINED, showColumnLines=Component.UNDEFINED, showRowLines=Component.UNDEFINED, sortByGroupSummaryInfo=Component.UNDEFINED, sorting=Component.UNDEFINED, stateStoring=Component.UNDEFINED, summary=Component.UNDEFINED, tabIndex=Component.UNDEFINED, twoWayBindingEnabled=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, wordWrapEnabled=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'accessKey', 'activeStateEnabled', 'addDroppedRow', 'allowColumnReordering', 'allowColumnResizing', 'autoNavigateToFocusedRow', 'cacheEnabled', 'cellClick', 'cellHintEnabled', 'columnAutoWidth', 'columnChooser', 'columnFixing', 'columnHidingEnabled', 'columnMinWidth', 'columnResizingMode', 'columnWidth', 'columns', 'columnsUpdateOption', 'dataSource', 'dateSerializationFormat', 'defaultSelectedRowKeys', 'disabled', 'dragClone', 'dragRemove', 'dragStart', 'dropAdd', 'editing', 'elementAttr', 'errorRowEnabled', 'export', 'filterBuilder', 'filterBuilderPopup', 'filterPanel', 'filterRow', 'filterSyncEnabled', 'filterValue', 'focusStateEnabled', 'focusedColumnIndex', 'focusedRowEnabled', 'focusedRowIndex', 'focusedRowKey', 'groupPanel', 'grouping', 'headerFilter', 'height', 'highlightChanges', 'hint', 'hoverStateEnabled', 'keyExpr', 'keyboardNavigation', 'loadPanel', 'loading_state', 'masterDetail', 'noDataText', 'onCellClick', 'onRowClick', 'pager', 'paging', 'remoteOperations', 'removeDroppedRow', 'renderAsync', 'repaintChangesOnly', 'rowAlternationEnabled', 'rowClick', 'rowComponent', 'rowDblClick', 'rowDragging', 'rowRemoved', 'rowRemoving', 'rowTemplate', 'rowUpdated', 'rowUpdating', 'rtlEnabled', 'scrolling', 'searchPanel', 'selectedRowKeys', 'selection', 'selectionFilter', 'showBorders', 'showColumnHeaders', 'showColumnLines', 'showRowLines', 'sortByGroupSummaryInfo', 'sorting', 'stateStoring', 'summary', 'tabIndex', 'twoWayBindingEnabled', 'visible', 'width', 'wordWrapEnabled']
        self._type = 'DDDataGrid'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'accessKey', 'activeStateEnabled', 'addDroppedRow', 'allowColumnReordering', 'allowColumnResizing', 'autoNavigateToFocusedRow', 'cacheEnabled', 'cellClick', 'cellHintEnabled', 'columnAutoWidth', 'columnChooser', 'columnFixing', 'columnHidingEnabled', 'columnMinWidth', 'columnResizingMode', 'columnWidth', 'columns', 'columnsUpdateOption', 'dataSource', 'dateSerializationFormat', 'defaultSelectedRowKeys', 'disabled', 'dragClone', 'dragRemove', 'dragStart', 'dropAdd', 'editing', 'elementAttr', 'errorRowEnabled', 'export', 'filterBuilder', 'filterBuilderPopup', 'filterPanel', 'filterRow', 'filterSyncEnabled', 'filterValue', 'focusStateEnabled', 'focusedColumnIndex', 'focusedRowEnabled', 'focusedRowIndex', 'focusedRowKey', 'groupPanel', 'grouping', 'headerFilter', 'height', 'highlightChanges', 'hint', 'hoverStateEnabled', 'keyExpr', 'keyboardNavigation', 'loadPanel', 'loading_state', 'masterDetail', 'noDataText', 'onCellClick', 'onRowClick', 'pager', 'paging', 'remoteOperations', 'removeDroppedRow', 'renderAsync', 'repaintChangesOnly', 'rowAlternationEnabled', 'rowClick', 'rowComponent', 'rowDblClick', 'rowDragging', 'rowRemoved', 'rowRemoving', 'rowTemplate', 'rowUpdated', 'rowUpdating', 'rtlEnabled', 'scrolling', 'searchPanel', 'selectedRowKeys', 'selection', 'selectionFilter', 'showBorders', 'showColumnHeaders', 'showColumnLines', 'showRowLines', 'sortByGroupSummaryInfo', 'sorting', 'stateStoring', 'summary', 'tabIndex', 'twoWayBindingEnabled', 'visible', 'width', 'wordWrapEnabled']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DDDataGrid, self).__init__(**args)
