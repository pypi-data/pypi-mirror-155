import hashlib
from typing import TYPE_CHECKING, Optional, Union
from pathlib import Path
from argus_api.session import get_session

try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict

if TYPE_CHECKING:
    from argus_api.session import ArgusAPISession


class ChallengeToken(TypedDict):
    id: str
    sha256: str


def generate_challenge_token(
    sha256: str,
    data: Union[bytes, Path],
    verify: Optional[bool] = None,
    proxies: Optional[dict] = None,
    apiKey: Optional[str] = None,
    authentication: Optional[dict] = None,
    server_url: Optional[str] = None,
    api_session: Optional["ArgusAPISession"] = None,
) -> ChallengeToken:
    """ "Generate a challenge token for a sample

    :param sha256: sha256 of the sample
    :param data: sample data. Can be provided raw bytes or a :class:`pathlib.Path`
      object pointing to the sample's location.
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

    :returns: challenge token
    """

    route = "/sampledb/v2/sample/{sha256}/challenge".format(sha256=sha256)

    session = api_session or get_session()

    response = session.post(
        route,
        verify=verify,
        apiKey=apiKey,
        authentication=authentication,
        server_url=server_url,
        proxies=proxies,
    )

    challenge = response.json()["data"]

    offset = challenge["offset"]
    length = challenge["length"]

    if isinstance(data, Path):
        data = data.read_bytes()

    challenge_hash = hashlib.sha256(data[offset : offset + length])

    return {"id": challenge["id"], "sha256": challenge_hash.hexdigest()}
