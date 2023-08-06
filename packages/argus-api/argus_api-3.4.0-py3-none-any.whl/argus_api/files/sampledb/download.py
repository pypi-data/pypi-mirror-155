from typing import TYPE_CHECKING, Optional, Union
from pathlib import Path
from argus_api.session import get_session

if TYPE_CHECKING:
    from argus_api.session import ArgusAPISession


def download_sample(
    sha256: str,
    destination_file: Optional[Union[str, Path]] = None,
    verify: Optional[bool] = None,
    proxies: Optional[dict] = None,
    apiKey: Optional[str] = None,
    authentication: Optional[dict] = None,
    server_url: Optional[str] = None,
    api_session: Optional["ArgusAPISession"] = None,
) -> bytes:
    """download a new sample file. (INTERNAL)

    returns the content of the sample as bytes. If ``destination_path`` is set to a
    path, the sample will be written to the file at that location.

    :param sha256: sha256 of the sample
    :param destination_file: if set, write the sample to the file at the path this
      points to.
    :param verify: path to a certificate bundle or boolean indicating whether SSL
      verification should be performed.
    :param apiKey: Argus API key.
    :param authentication: authentication override
    :param server_url: API base URL override
    :param api_session: session to use for this request. If not set, the global session will be used.
    :raises AuthenticationFailedException: on 401
    :raises AccessDeniedException: on 403
    :raises AnErrorOccurredException: on 404
    :raises ValidationErrorException: on 412
    :raises ArgusException: on other status codes

    :returns: content of the sample as bytes
    """

    route = "/sampledb/v2/sample/{sha256}/raw".format(sha256=sha256)

    session = api_session or get_session()

    response = session.get(
        route,
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
