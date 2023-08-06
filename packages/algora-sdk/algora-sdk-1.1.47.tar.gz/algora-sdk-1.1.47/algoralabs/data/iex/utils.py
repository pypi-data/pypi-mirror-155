from algoralabs.common.requests import __get_request, __async_get_request


def __build_url(extension: str) -> str:
    return f"data/datasets/query/iex/{extension}"


def __base_request(extension: str, **kwargs):
    """
    Base GET request for IEX

    :param extension: URI extension
    :param kwargs: request query params
    :return: response
    """
    return __get_request(endpoint=__build_url(extension), params=kwargs)


async def __async_base_request(extension: str, **kwargs):
    """
    Base GET request for IEX

    :param extension: URI extension
    :param kwargs: request query params
    :return: response
    """
    return await __async_get_request(endpoint=__build_url(extension), params=kwargs)
