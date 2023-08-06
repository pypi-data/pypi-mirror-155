from gwdc_python.files.identifiers import match_file_suffix, match_file_name


def ini_file(file_path):
    """Checks to see if the given file path points to an ini file

    Parameters
    ----------
    file_path : ~pathlib.Path
        File path to check

    Returns
    -------
    bool
        True if path points to a ini file, False otherwise
    """
    return match_file_suffix(file_path, 'ini')


def candidates_file(file_path):
    """Checks to see if the given file path points to the candidates file

    Parameters
    ----------
    file_path : ~pathlib.Path
        File path to check

    Returns
    -------
    bool
        True if path points to candidates file, False otherwise
    """
    return match_file_name(file_path, 'results_a0_phase_loglikes_scores.dat')
