from .strings import snakefy_key


def singleton(class_):
    """
    Class decorator for singleton pattern
    @see: https://stackoverflow.com/q/6760685
    """
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


class dotdict(dict):
    """
    @see: https://stackoverflow.com/a/23689767
    dot.notation access to dictionary attributes
    """

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def snakefy_dictionary_keys(input_dict: dict) -> dict:
    """
    transform all dictionary keys to snaky form:
        - CamelCase --> camel_case
        - camelCase --> camel_case
        - camel-case --> camel_case
    """
    output_dict = {}
    for attr, value in input_dict.items():
        output_dict[snakefy_key(attr)] = value
    return output_dict
