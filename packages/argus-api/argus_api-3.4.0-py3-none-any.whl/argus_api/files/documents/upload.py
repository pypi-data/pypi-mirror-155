from typing import TYPE_CHECKING, Optional, Union
from pathlib import Path
from argus_api.session import get_session

if TYPE_CHECKING:
    from argus_api.session import ArgusAPISession


def upload_document(
    mime_type: str,
    data: Union[bytes, Path],
    folder: Union[str, int],
    name: str,
    customer: Optional[Union[str, int]] = None,
    accessMode: Optional[str] = None,
    overwriteExisting: bool = False,
    skipNotification: bool = False,
    createMissing: Optional[bool] = None,
    json: bool = True,
    verify: Optional[bool] = None,
    proxies: Optional[dict] = None,
    apiKey: Optional[str] = None,
    authentication: Optional[dict] = None,
    server_url: Optional[str] = None,
    api_session: Optional["ArgusAPISession"] = None,
) -> dict:
    """Upload a document to a folder.

    :param mime_type: MIME type of the document
    :param data: document data, either as raw bytes or a :class:`pathlib.Path` object.
      if a `pathlib.Path` object is provided, the file it is pointing to will be read.
    :param folder: folder ID or path to upload the document to. If using a folder ID, it
      must be passed as an int.
    :param name: file name of the document.
    :param customer: ID or shortname of the customer whose space the document will be
       uploaded to. Ignored if the destnation folder is provided as an ID, otherwise
       defaults to the current user's customer.
    :param str accessMode: Access mode to set on new document
    :param bool overwriteExisting: If true, overwrite existing document with the same name
    :param bool skipNotification: If true, skip notification to folder watchers
    :param createMissing: If set to ``True``, create any missing folders before
      adding the document. Will be ignored if the folder has been provided as an ID.
    :param json: return the response's body as a ``dict`` parsed from json. ``True`` by
      default. If set to false, the raw ``requests.Response`` object will be returned.
    :param verify: path to a certificate bundle or boolean indicating whether SSL
      verification should be performed.
    :param apiKey: Argus API key.
    :param authentication: authentication override
    :param server_url: API base URL override
    :param api_session: session to use for this request. If not set, the global session will be used.
    :raises AuthenticationFailedException: on 401
    :raises AccessDeniedException: on 403
    :raises ParentFolderNotFoundException: on 404
    :raises ValidationFailedException: on 412
    :raises ArgusException: on other status codes

    :returns: dictionary translated from JSON
    """

    session = api_session or get_session()

    if isinstance(folder, str):
        folder_path = f"document/path/{folder.lstrip('/')}"
    else:
        folder_path = f"folder/{folder}/documents"
    route = "/documents/v1/{folder_path}/{name}".format(
        folder_path=folder_path, name=name
    )

    headers = {"Content-Type": mime_type}

    query_parameters = {"overwriteExisting": overwriteExisting, "skipNotification": skipNotification}


    if not isinstance(folder, int):
        # parameters for folder-as-path
        if createMissing is not None :
            query_parameters["createMissing"] = createMissing
        if customer is not None:
            query_parameters["customer"] = customer

    if accessMode is not None:
        query_parameters.update({"accessMode": accessMode})

    if isinstance(data, Path):
        data = data.read_bytes()

    response = session.post(
        route,
        params=query_parameters,
        data=data,
        verify=verify,
        apiKey=apiKey,
        authentication=authentication,
        server_url=server_url,
        headers=headers,
        proxies=proxies,
    )
    return response.json() if json else response
