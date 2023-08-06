import pytest
from gwlab_viterbi_python import ViterbiJob, FileReference, FileReferenceList
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
def txt():
    return FileReferenceList([
        FileReference(
            path='atoms/188-0/sfts_used.txt',
            file_size='1',
            download_token='test_token_7',
            job_id='id'
        ),
    ])


@pytest.fixture
def full(ini, candidates, extra, txt):
    return ini + candidates + extra + txt


@pytest.fixture
def mock_viterbi_job(mocker):
    def viterbi_job(methods={}):
        config_dict = {f'{key}.return_value': value for key, value in methods.items()}
        return ViterbiJob(
            client=mocker.Mock(**config_dict),
            job_id='test_id',
            name='TestName',
            description='Test description',
            user='Test User',
            job_status={
                'name': 'Completed',
                'date': '2021-12-02'
            },
        )

    return viterbi_job


@pytest.fixture
def mock_viterbi_job_files(mock_viterbi_job, full):
    return mock_viterbi_job({'_get_files_by_job_id': (full, False)})


def test_viterbi_job_full_file_list(mock_viterbi_job_files, full):
    viterbi_job = mock_viterbi_job_files
    assert viterbi_job.get_full_file_list() == full

    viterbi_job.client._get_files_by_job_id.assert_called_once()


def test_viterbi_job_equality(mocker):
    job_data = {
        "client": mocker.Mock(),
        "job_id": 1,
        "name": "test_name",
        "description": "test description",
        "user": "Test User",
        "job_status": {
            "name": "Completed",
            "date": "2021-01-01"
        }
    }
    job_data_changed_id = {**job_data, "job_id": 2}
    job_data_changed_name = {**job_data, "name": "testing_name"}
    job_data_changed_user = {**job_data, "user": "Testing User"}

    assert ViterbiJob(**job_data) == ViterbiJob(**job_data)
    assert ViterbiJob(**job_data) != ViterbiJob(**job_data_changed_id)
    assert ViterbiJob(**job_data) != ViterbiJob(**job_data_changed_name)
    assert ViterbiJob(**job_data) != ViterbiJob(**job_data_changed_user)


def test_viterbi_job_file_filters(mocker, mock_viterbi_job_files, full, ini, candidates):
    viterbi_job = mock_viterbi_job_files
    assert file_filters.sort_file_list(viterbi_job.get_ini_file_list()) == file_filters.sort_file_list(ini)
    assert file_filters.sort_file_list(viterbi_job.get_candidates_file_list()) == \
        file_filters.sort_file_list(candidates)

    assert viterbi_job.client._get_files_by_job_id.call_count == 2


def test_viterbi_job_file_filters_args(mocker, mock_viterbi_job):
    mocker.patch('gwlab_viterbi_python.viterbi_job.ViterbiJob.get_full_file_list')
    viterbi_job = mock_viterbi_job({
        'save_files_by_reference': None,
        'get_files_by_reference': None,
    })
    try:
        viterbi_job.get_ini_files()
        viterbi_job.save_ini_files(root_path='.', preserve_directory_structure=True)
        viterbi_job.get_candidates_files()
        viterbi_job.save_candidates_files(root_path='.', preserve_directory_structure=True)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")


def test_register_file_list_filter(mock_viterbi_job_files, txt):
    viterbi_job = mock_viterbi_job_files

    def get_txt_file(file_list):
        return [f for f in file_list if f.path.suffix == '.txt']

    assert getattr(viterbi_job, 'get_txt_file_list', None) is None
    assert getattr(viterbi_job, 'get_txt_files', None) is None
    assert getattr(viterbi_job, 'save_txt_files', None) is None

    ViterbiJob.register_file_list_filter('txt', get_txt_file)

    assert getattr(viterbi_job, 'get_txt_file_list', None) is not None
    assert getattr(viterbi_job, 'get_txt_files', None) is not None
    assert getattr(viterbi_job, 'save_txt_files', None) is not None

    assert viterbi_job.get_txt_file_list() == txt
