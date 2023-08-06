from gwdc_python.files.filters import filter_file_list
from . import identifiers


def ini_filter(file_list):
    """Takes an input file list and returns a subset of that file list containing:

    - Any ini file

    Parameters
    ----------
    file_list : .FileReferenceList
        A list of FileReference objects which will be filtered

    Returns
    -------
    .FileReferenceList
        Subset of the input FileReferenceList containing only the paths that match the above config file criteria
    """
    return filter_file_list(identifiers.ini_file, file_list)[0]


def candidates_filter(file_list):
    """Takes an input file list and returns a subset of that file list containing:

    - Any file named 'results_a0_phase_loglikes_scores.dat'

    Parameters
    ----------
    file_list : .FileReferenceList
        A list of FileReference objects which will be filtered

    Returns
    -------
    .FileReferenceList
        Subset of the input FileReferenceList containing only the paths that match the above config file criteria
    """
    return filter_file_list(identifiers.candidates_file, file_list)[0]


def sort_file_list(file_list):
    """Sorts a file list based on the 'path' key of the dicts. Primarily used for equality checks.

    Parameters
    ----------
    file_list : .FileReferenceList
        A list of FileReference objects which will be filtered

    Returns
    -------
    .FileReferenceList
        A FileReferenceList containing the same members as the input,
        sorted by the path attribute of the FileReference objects
    """
    return sorted(file_list, key=lambda f: f.path)
