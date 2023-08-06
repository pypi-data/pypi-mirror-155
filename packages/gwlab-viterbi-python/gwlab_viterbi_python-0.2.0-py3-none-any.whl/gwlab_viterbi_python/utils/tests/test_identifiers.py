import pytest
from pathlib import Path
from gwlab_viterbi_python.utils import identifiers


@pytest.fixture
def setup_paths():
    return {
        'ini': Path('test.ini'),
        'dir_ini': Path('this/is/a/test.ini'),

        'no_suffix': Path('this/is/a/test'),
        'ini_dir': Path('this/is/not/a/ini'),
        'dat_dir': Path('this/is/not/a/dat'),

        'candidates': Path('results_a0_phase_loglikes_scores.dat'),
        'dir_candidates': Path('this/is/results_a0_phase_loglikes_scores.dat'),
        'candidates_bad_ext': Path('this/is/results_a0_phase_loglikes_scores.png'),
        'candidates_bad_pattern': Path('results_a1_phase_loglikes_scores.dat'),
    }


@pytest.fixture
def setup_identifiers():
    return [
        (
            identifiers.ini_file,
            ['ini', 'dir_ini']
        ),
        (
            identifiers.candidates_file,
            ['candidates', 'dir_candidates']
        )
    ]


@pytest.fixture
def check_identifier(setup_paths):
    def _check_identifier(identifier, true_path_keys):
        true_paths = [value for key, value in setup_paths.items() if key in true_path_keys]
        false_paths = [value for key, value in setup_paths.items() if key not in true_path_keys]

        for path in true_paths:
            assert identifier(path) is True

        for path in false_paths:
            assert identifier(path) is False

    return _check_identifier


def test_identifiers(setup_identifiers, check_identifier):
    for identifier, true_path_keys in setup_identifiers:
        check_identifier(identifier, true_path_keys)
