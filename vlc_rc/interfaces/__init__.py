class InvalidInterfaceException(Exception):
    pass


def get_by_name(name):
    """
    Returns an interface by its name.
    Raises ``InvalidInterfaceException`` if there is no such interface.
    """
    module_name = '%s.%s.%s' % ('vlc_rc', 'interfaces', name)
    try:
        module = __import__(module_name)
    except ImportError:
        raise InvalidInterfaceException
    try:
        module = getattr(module, 'interfaces')
        return getattr(module, name).Interface
    except AttributeError:
        raise InvalidInterfaceException
