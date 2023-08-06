import pytest
from gwlab_viterbi_python import FileReference, FileReferenceList
from gwlab_viterbi_python.utils import file_filters


@pytest.fixture
def ini():
    return FileReferenceList([
        FileReference(
            path='arbitrary/dir/test1.ini',
            file_size='1',
            download_token='test_token_1',
            job_id='id'
        ),
        FileReference(
            path='arbitrary/dir/test2.ini',
            file_size='1',
            download_token='test_token_2',
            job_id='id'
        ),
    ])


@pytest.fixture
def candidates():
    return FileReferenceList([
        FileReference(
            path='results_a0_phase_loglikes_scores.dat',
            file_size='1',
            download_token='test_token_3',
            job_id='id'
        ),
    ])


@pytest.fixture
def extra():
    return FileReferenceList([
        FileReference(
            path='extra/ini.png',
            file_size='1',
            download_token='test_token_4',
            job_id='id'
        ),
        FileReference(
            path='extra_scores.dat',
            file_size='1',
            download_token='test_token_5',
            job_id='id'
        ),
        FileReference(
            path='an/arbitrary.extra',
            file_size='1',
            download_token='test_token_6',
            job_id='id'
        ),
    ])


@pytest.fixture
def full(ini, candidates, extra):
    return ini + candidates + extra


def test_ini_file_filter(full, ini):
    sub_list = file_filters.ini_filter(full)
    assert file_filters.sort_file_list(sub_list) == file_filters.sort_file_list(ini)


def test_candidates_file_filter(full, candidates):
    sub_list = file_filters.candidates_filter(full)
    assert file_filters.sort_file_list(sub_list) == file_filters.sort_file_list(candidates)
