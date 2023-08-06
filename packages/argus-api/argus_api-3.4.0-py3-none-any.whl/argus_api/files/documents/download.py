from typing import TYPE_CHECKING, Optional, Union, List
from pathlib import Path
from argus_api.session import get_session

if TYPE_CHECKING:
    from argus_api.session import ArgusAPISession


def download_document(
    document: Union[str, int],
    destination_file: Optional[Union[str, Path]] = None,
    customer: Optional[Union[str, int]] = None,
    verify: Optional[bool] = None,
    proxies: Optional[dict] = None,
    apiKey: Optional[str] = None,
    authentication: Optional[dict] = None,
    server_url: Optional[str] = None,
    api_session: Optional["ArgusAPISession"] = None,
) -> bytes:
    """Download a document.

    returns the content of the document as bytes. If ``destination_path`` is set to a
    path, the sample will be written to the file at that location.

    :param document: path or ID of the document to download. If an ID is
      provided, it must be passend as an ``int``.
    :param destination_file: if set, write the document to the file at the path this
      points to.
    :param customer: ID or shortname of the customer whose space the document will be
       downloaded from. Ignored if the destnation folder is provided as an ID, otherwise
       defaults to the current user's customer.
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

    if isinstance(document, str):
        doc_path = f"document/path/content/{document.lstrip('/')}"
    else:
        doc_path = f"document/{document}/content"
    route = "/documents/v1/{doc_path}".format(
        doc_path=doc_path
    )

    query_parameters = None
    if not isinstance(document, int):
        if customer is not None:
            query_parameters = {"customer":  customer}

    response = session.get(
        route,
        params=query_parameters,
        verify=verify,
        apiKey=apiKey,
        authentication=authentication,
        server_url=server_url,
        proxies=proxies,
    )

    data = response.content

    if destination_file:
        destination_file = Path(destination_file)
        destination_file.write_bytes(data)

    return data
