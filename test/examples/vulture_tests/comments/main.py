"""
    the main function
"""


def main():  # vulture: ignore
    """
        the main
        function
    """
    return sub_main()


def sub_main():
    """
        pass
    """
    return 2


@property  # vulture: ignore
def other_main():  # vulture: ignore
    return sub_main()


@app.route("test")  # vulture: ignore
@app.my_route  # test
def test_other_main():  # vulture: ignore

    @my_app.route("test")  # vulture: ignore
    @my_app.test_route  # test
    def test():  # vulture: ignore
        pass
    return sub_main()


class Enum:  # vulture: ignore
    """
        Tests enum
    """
    A = 1
    B = 1
    C = 1
