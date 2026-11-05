import pytest
from NrrdReader import NrrdReader
def test_reader_missing_file():
    with pytest.raises(FileNotFoundError):
        NrrdReader.load("data/does_not_exist.nrrd")