from .utils import file_filters

from gwdc_python.jobs import JobBase
from gwdc_python.logger import create_logger

logger = create_logger(__name__)


class ViterbiJob(JobBase):
    """
    ViterbiJob class is useful for interacting with the Viterbi jobs returned from a call to the GWCloud API.
    It is primarily used to store job information and obtain files related to the job.

    Parameters
    ----------
    client : ~gwlab_viterbi_python.gwlab_viterbi.GWLabViterbi
        A reference to the GWLabViterbi object instance from which the ViterbiJob was created
    job_id : str
        The id of the Viterbi job, required to obtain the files associated with it
    name : str
        Job name
    description : str
        Job description
    user : str
        User that ran the job
    job_status : dict
        Status of job, should have 'name' and 'date' keys corresponding to the status code and when it was produced
    kwargs : dict, optional
        Extra arguments, stored in `other` attribute
    """

    FILE_LIST_FILTERS = {
        'ini': file_filters.ini_filter,
        'candidates': file_filters.candidates_filter
    }

    def __init__(self, client, job_id, name, description, user, job_status, **kwargs):
        super().__init__(client, job_id, name, description, user, job_status)
        self.other = kwargs
