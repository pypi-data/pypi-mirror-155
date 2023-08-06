def chunk_string_by_length(message: str, length: int):
    """
    Splits the message to length size of chunks
    http://stackoverflow.com/a/9475270
    """
    chunks = []
    message = message.replace("\n", " ")
    while message:
        chunks.append(message[:length])
        message = message[length:]
    return chunks


def ensurePrefix(text: str, prefix: str) -> str:
    if not text.startswith(prefix):
        return f"{prefix}{text}"
    return text


def ensurePostfix(text: str, postfix: str) -> str:
    if not text.endswith(postfix):
        return f"{text}{postfix}"
    return text


def snakefy_key(attr: str) -> str:
    """
    transform a key to snaky form:
        - CamelCase --> camel_case
        - camelCase --> camel_case
        - camel-case --> camel_case
        - camel_case == camel_case
    """
    from functools import reduce

    attr = attr.replace("-", "_")
    return reduce(lambda x, y: x + ("_" if y.isupper() else "") + y, attr).lower()
