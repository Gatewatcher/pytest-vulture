"""
    the main function
"""
from .other import other


@property
def main():
    """
        the main
        function
    """
    other()
    return sub_main()


def sub_main():
    """
        pass
    """
    return 2
