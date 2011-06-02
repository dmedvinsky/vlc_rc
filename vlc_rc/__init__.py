import vlc_rc.interfaces


VERSION = (0, 0, 1)
INTERFACE_TELNET = 'telnet'


def interface(name):
    """
    Returns an interface by its name.
    Raises ``InvalidInterfaceException`` if there is no such interface.
    """
    return vlc_rc.interfaces.get_by_name(name)
