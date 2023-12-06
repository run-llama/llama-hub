import pytest

from llama_hub.docstring_walker.base import DocstringWalker
from llama_index import Document


SOME_CLASS_WITH_DOCSTRING = """
'''Basic module with a class definition'''

class Person:

    '''Basic class to represent a person
    '''

    def __init__(self, name: str, surname: str, age: int):
        self.name = name
        self.surname = surname
        self.age = age


    @property
    def full_name(self) -> str:
        '''A property for getting person fullname

        Returns
        -------
        str
            Full name: concatencation of name and surname
        '''
        return self.name + ' ' + self.surname
    

    def greet(self, other: str) -> str:
        '''Greeting function for a person

        Parameters
        ----------
        other : str
            Other person name.

        Returns
        -------
        str
            Greeting string.
        '''
        return 'Hello ' + other + ' , my name is ' + self.full_name
"""

MALFORMED_FILE = """
def addtwo(a, b):
    return a + b kasdlkjas
"""


SOME_FUNCTION = """
def add_numbers(a, b):
    return a+b
"""


def test_reading_module_with_class(mocker):
    # Given
    mocker.patch("os.path.exists", return_value=True)
    walker = DocstringWalker()
    mocker.patch(
        "os.walk",
        return_value=[
            ("somepath", "", ["somefile1.py"]),
        ],
    )
    mocker.patch.object(
        walker, "read_module_text", return_value=SOME_CLASS_WITH_DOCSTRING
    )

    # When
    docs = walker.load_data("somepath")

    # Then
    assert len(docs) == 1
    assert isinstance(docs[0], Document)
    assert docs[0].text.startswith("Module name: somefile")
    assert docs[0].text.endswith("Greeting string.\n")


def test_dont_fail_on_malformed_file(mocker):
    # Given
    mocker.patch("os.path.exists", return_value=True)
    walker = DocstringWalker()

    mocker.patch(
        "os.walk",
        return_value=[
            ("somepath", "", ["somefile.py"]),
        ],
    )
    mocker.patch.object(walker, "read_module_text", return_value=MALFORMED_FILE)

    # When
    docs = walker.load_data("somepath", fail_on_malformed_files=False)

    # Then
    assert len(docs) == 0


def test_fail_on_malformed_file(mocker):
    # Given
    mocker.patch("os.path.exists", return_value=True)
    walker = DocstringWalker()

    mocker.patch(
        "os.walk",
        return_value=[
            ("somepath", "", ["somefile.py"]),
        ],
    )
    mocker.patch.object(walker, "read_module_text", return_value=MALFORMED_FILE)

    # Then
    with pytest.raises(SyntaxError):
        walker.load_data("somepath", fail_on_malformed_files=True)


def test_reading_multiple_modules(mocker):
    # Given
    mocker.patch("os.path.exists", return_value=True)
    walker = DocstringWalker()
    mocker.patch(
        "os.walk",
        return_value=[
            ("somepath", "", ["somefile1.py", "somefile2.py"]),
        ],
    )
    mocker.patch.object(
        walker, "read_module_text", return_value=SOME_CLASS_WITH_DOCSTRING
    )

    # When
    docs = walker.load_data("somepath")

    # Then
    assert len(docs) == 2
    assert isinstance(docs[0], Document)
    assert all([doc.text.startswith("Module name: somefile") for doc in docs])
    assert all([doc.text.endswith("Greeting string.\n") for doc in docs])
