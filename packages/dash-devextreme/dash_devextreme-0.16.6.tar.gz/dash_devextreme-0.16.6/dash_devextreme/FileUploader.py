# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class FileUploader(Component):
    """A FileUploader component.


Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- accept (string; default ''):
    Specifies a file type or several types accepted by the UI
    component.

- accessKey (string; optional):
    Specifies the shortcut key that sets focus on the UI component.

- activeStateEnabled (boolean; default False):
    Specifies whether or not the UI component changes its state when
    interacting with a user.

- allowCanceling (boolean; default True):
    Specifies if an end user can remove a file from the selection and
    interrupt uploading.

- allowedFileExtensions (list of strings; optional):
    Restricts file extensions that can be uploaded to the server.

- chunkSize (number; default 0):
    Specifies the chunk size in bytes. Applies only if uploadMode is
    \"instantly\" or \"useButtons\". Requires a server that can
    process file chunks.

- dialogTrigger (string | dash component; optional):
    Specifies the HTML element which invokes the file upload dialog.

- disabled (boolean; default False):
    Specifies whether the UI component responds to user interaction.

- dropZone (string | dash component; optional):
    Specifies the HTML element in which users can drag and drop files
    for upload.

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

- inputAttr (dict; optional):
    Specifies the attributes to be passed on to the underlying <input>
    element of the file type.

- invalidFileExtensionMessage (string; default 'File type is not allowed'):
    The text displayed when the extension of the file being uploaded
    is not an allowed file extension.

- invalidMaxFileSizeMessage (string; default 'File is too large'):
    The text displayed when the size of the file being uploaded is
    greater than the maxFileSize.

- invalidMinFileSizeMessage (string; default 'File is too small'):
    The text displayed when the size of the file being uploaded is
    less than the minFileSize.

- isValid (boolean; default True):
    Specifies or indicates whether the editor's value is valid.

- labelText (string; default 'or Drop file here'):
    Specifies the text displayed on the area to which an end-user can
    drop a file.

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

- maxFileSize (number; default 0):
    Specifies the maximum file size (in bytes) allowed for uploading.
    Applies only if uploadMode is \"instantly\" or \"useButtons\".

- minFileSize (number; default 0):
    Specifies the minimum file size (in bytes) allowed for uploading.
    Applies only if uploadMode is \"instantly\" or \"useButtons\".

- multiple (boolean; default False):
    Specifies whether the UI component enables an end-user to select a
    single file or multiple files.

- name (string; default 'files[]'):
    Specifies the value passed to the name attribute of the underlying
    input element. Required to access uploaded files on the server.

- progress (number; default 0):
    Gets the current progress in percentages.

- readOnly (boolean; default False):
    Specifies whether the editor is read-only.

- readyToUploadMessage (string; default 'Ready to upload'):
    The message displayed by the UI component when it is ready to
    upload the specified files.

- rtlEnabled (boolean; default False):
    Switches the UI component to a right-to-left representation.

- selectButtonText (string; default 'Select File'):
    The text displayed on the button that opens the file browser.

- showFileList (boolean; default True):
    Specifies whether or not the UI component displays the list of
    selected files.

- tabIndex (number; default 0):
    Specifies the number of the element when the Tab key is used for
    navigating.

- uploadAbortedMessage (string; default 'Upload cancelled'):
    The message displayed by the UI component when the file upload is
    cancelled.

- uploadButtonText (string; default 'Upload'):
    The text displayed on the button that starts uploading.

- uploadCustomData (dict; optional):
    Specifies custom data for the upload request.

- uploadFailedMessage (string; default 'Upload failed'):
    The message displayed by the UI component on uploading failure.

- uploadHeaders (dict; optional):
    Specifies headers for the upload request.

- uploadMethod (a value equal to: 'POST', 'PUT'; default 'POST'):
    Specifies the method for the upload request.

- uploadMode (a value equal to: 'instantly', 'useButtons', 'useForm'; default 'instantly'):
    Specifies how the UI component uploads files.

- uploadUrl (string; default '/'):
    Specifies a target Url for the upload request.

- uploadedMessage (string; default 'Uploaded'):
    The message displayed by the UI component when uploading is
    finished.

- validationError (dict; optional):
    Information on the broken validation rule. Contains the first item
    from the validationErrors array.

- validationErrors (list of dicts; optional):
    An array of the validation rules that failed.

- validationStatus (a value equal to: 'valid', 'invalid', 'pending'; default 'valid'):
    Indicates or specifies the current validation status.

- value (list; optional):
    Specifies a File instance representing the selected file.
    Read-only when uploadMode is \"useForm\".

- visible (boolean; default True):
    Specifies whether the UI component is visible.

- width (number | string; optional):
    Specifies the UI component's width."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, abortUpload=Component.UNDEFINED, accept=Component.UNDEFINED, accessKey=Component.UNDEFINED, activeStateEnabled=Component.UNDEFINED, allowCanceling=Component.UNDEFINED, allowedFileExtensions=Component.UNDEFINED, chunkSize=Component.UNDEFINED, dialogTrigger=Component.UNDEFINED, disabled=Component.UNDEFINED, dropZone=Component.UNDEFINED, elementAttr=Component.UNDEFINED, focusStateEnabled=Component.UNDEFINED, height=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, inputAttr=Component.UNDEFINED, invalidFileExtensionMessage=Component.UNDEFINED, invalidMaxFileSizeMessage=Component.UNDEFINED, invalidMinFileSizeMessage=Component.UNDEFINED, isValid=Component.UNDEFINED, labelText=Component.UNDEFINED, maxFileSize=Component.UNDEFINED, minFileSize=Component.UNDEFINED, multiple=Component.UNDEFINED, name=Component.UNDEFINED, onBeforeSend=Component.UNDEFINED, onContentReady=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onDropZoneEnter=Component.UNDEFINED, onDropZoneLeave=Component.UNDEFINED, onFilesUploaded=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, onProgress=Component.UNDEFINED, onUploadAborted=Component.UNDEFINED, onUploaded=Component.UNDEFINED, onUploadError=Component.UNDEFINED, onUploadStarted=Component.UNDEFINED, onValueChanged=Component.UNDEFINED, progress=Component.UNDEFINED, readOnly=Component.UNDEFINED, readyToUploadMessage=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, selectButtonText=Component.UNDEFINED, showFileList=Component.UNDEFINED, tabIndex=Component.UNDEFINED, uploadAbortedMessage=Component.UNDEFINED, uploadButtonText=Component.UNDEFINED, uploadChunk=Component.UNDEFINED, uploadCustomData=Component.UNDEFINED, uploadedMessage=Component.UNDEFINED, uploadFailedMessage=Component.UNDEFINED, uploadFile=Component.UNDEFINED, uploadHeaders=Component.UNDEFINED, uploadMethod=Component.UNDEFINED, uploadMode=Component.UNDEFINED, uploadUrl=Component.UNDEFINED, validationError=Component.UNDEFINED, validationErrors=Component.UNDEFINED, validationStatus=Component.UNDEFINED, value=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'accept', 'accessKey', 'activeStateEnabled', 'allowCanceling', 'allowedFileExtensions', 'chunkSize', 'dialogTrigger', 'disabled', 'dropZone', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'inputAttr', 'invalidFileExtensionMessage', 'invalidMaxFileSizeMessage', 'invalidMinFileSizeMessage', 'isValid', 'labelText', 'loading_state', 'maxFileSize', 'minFileSize', 'multiple', 'name', 'progress', 'readOnly', 'readyToUploadMessage', 'rtlEnabled', 'selectButtonText', 'showFileList', 'tabIndex', 'uploadAbortedMessage', 'uploadButtonText', 'uploadCustomData', 'uploadFailedMessage', 'uploadHeaders', 'uploadMethod', 'uploadMode', 'uploadUrl', 'uploadedMessage', 'validationError', 'validationErrors', 'validationStatus', 'value', 'visible', 'width']
        self._type = 'FileUploader'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'accept', 'accessKey', 'activeStateEnabled', 'allowCanceling', 'allowedFileExtensions', 'chunkSize', 'dialogTrigger', 'disabled', 'dropZone', 'elementAttr', 'focusStateEnabled', 'height', 'hint', 'hoverStateEnabled', 'inputAttr', 'invalidFileExtensionMessage', 'invalidMaxFileSizeMessage', 'invalidMinFileSizeMessage', 'isValid', 'labelText', 'loading_state', 'maxFileSize', 'minFileSize', 'multiple', 'name', 'progress', 'readOnly', 'readyToUploadMessage', 'rtlEnabled', 'selectButtonText', 'showFileList', 'tabIndex', 'uploadAbortedMessage', 'uploadButtonText', 'uploadCustomData', 'uploadFailedMessage', 'uploadHeaders', 'uploadMethod', 'uploadMode', 'uploadUrl', 'uploadedMessage', 'validationError', 'validationErrors', 'validationStatus', 'value', 'visible', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(FileUploader, self).__init__(**args)
