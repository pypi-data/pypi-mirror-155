from typing import TYPE_CHECKING, Optional, Union, List
from pathlib import Path
from argus_api.session import get_session
from argus_api.files.sampledb.challenge import generate_challenge_token

if TYPE_CHECKING:
    from argus_api.session import ArgusAPISession


def upload_sample(
    data: Union[bytes, Path],
    json: bool = True,
    verify: Optional[bool] = None,
    proxies: Optional[dict] = None,
    apiKey: Optional[str] = None,
    authentication: Optional[dict] = None,
    server_url: Optional[str] = None,
    api_session: Optional["ArgusAPISession"] = None,
) -> dict:
    """Upload a new sample file. (INTERNAL)

    :param data: sample data. Can be provided raw bytes or a :class:`pathlib.Path`
      object pointing to the sample's location.
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
    :raises AnErrorOccurredException: on 404
    :raises ValidationErrorException: on 412
    :raises ArgusException: on other status codes

    :returns: API response as a dict or response object if the ``json`` parameter was
      set to ``False``.
    """

    route = "/sampledb/v2/sample".format()

    session = api_session or get_session()

    if isinstance(data, Path):
        data = data.read_bytes()

    response = session.post(
        route,
        data=data,
        verify=verify,
        apiKey=apiKey,
        authentication=authentication,
        server_url=server_url,
        proxies=proxies,
    )
    return response.json() if json else response


def add_submission(
    sha256: str,
    data: Union[bytes, Path],
    fileName: str,
    user_agent_name: str,
    user_agent_version: str,
    customer: Optional[Union[str, int]] = None,
    observedTimestamp: Optional[int] = None,
    mimeType: Optional[str] = None,
    metaData: Optional[dict] = None,
    acl: Optional[List[Union[str, int]]] = None,
    tlp: Optional[str] = None,
    json: bool = True,
    verify: Optional[bool] = None,
    proxies: Optional[dict] = None,
    apiKey: Optional[str] = None,
    authentication: Optional[dict] = None,
    server_url: Optional[str] = None,
    api_session: Optional["ArgusAPISession"] = None,
) -> dict:
    """Add a new sample submission. The required challenge token will be generated
    automatically. (INTERNAL)

    :param sha256: sha256 hash of the sample to add the submission for
    :param data: sample data. Can be provided raw bytes or a :class:`pathlib.Path`
      object pointing to the sample's location.
    :param fileName: The filename of the sample
    :param user_agent_name: name of the user agent
    :param user_agent_version: version of the user agent
    :param customer: The shortname or ID of customer the submission belongs to. Default value is the currernt user's customer.
    :param observedTimestamp: The timestamp of when the sample was observed. Defaults to the current time
    :param mimeType: The sample mime type (default application/octet-stream)
    :param metaData: Meta data about the sample
    :param acl: List of user IDs or shortnames that are given explicit access to the submission
    :param tlp: TLP color of the submission. Defaults to amber.
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
    :raises AnErrorOccurredException: on 404
    :raises ValidationErrorException: on 412
    :raises ArgusException: on other status codes

    :returns: API response as a dict or response object if the ``json`` parameter was
      set to ``False``.
    """

    route = "/sampledb/v2/sample/{sha256}/submission".format(
        sha256=sha256,
    )

    session = api_session or get_session()

    body = {
        "fileName": fileName,
        "userAgent": {
            "name": user_agent_name,
            "version": user_agent_version,
        },
    }
    if customer:
        body["customer"] = customer
    if observedTimestamp:
        body["observedTimestamp"] = customer
    if mimeType:
        body["mimeType"] = customer
    if metaData:
        body["metaData"] = customer
    if acl:
        body["acl"] = customer
    if tlp:
        body["tlp"] = customer

    body["challengeToken"] = generate_challenge_token(
        sha256=sha256,
        data=data,
        verify=verify,
        proxies=proxies,
        apiKey=apiKey,
        authentication=authentication,
        server_url=server_url,
        api_session=api_session,
    )

    response = session.post(
        route,
        json=body,
        verify=verify,
        apiKey=apiKey,
        authentication=authentication,
        server_url=server_url,
        proxies=proxies, stream=True
    )
    return response.json() if json else response
