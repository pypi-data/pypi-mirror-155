"""Library defining the interface to a test batch object."""

import pandas as pd

from rime_sdk.internal.backend import RIMEBackend
from rime_sdk.internal.protobuf_parser import parse_test_batch_result
from rime_sdk.internal.test_helpers import get_batch_result_response


class TestBatch:
    """An interface for a test batch in a RIME test run.

    Attributes:
        backend: RIMEBackend
            The RIME backend used to query about the test run.
        test_run_id: str
            The string identifier for the successfully completed test run.
        test_type: str
            The unique identifer for the test type e.g. unseen_categorical.
    """

    def __init__(self, backend: RIMEBackend, test_run_id: str, test_type: str) -> None:
        """Contains information about a TestBatch.

        Args:
            backend: RIMEBackend
                The RIME backend used to query about the status of the job.
            test_run_id: str
                The identifier for the test run this test batch belong to.
            test_type: str
                The identifier for the test type this batch represents.
        """
        self._backend = backend
        self._test_run_id = test_run_id
        self._test_type = test_type

    def summary(self) -> pd.Series:
        """Obtain the test batch summary as a Pandas Series.

        columns:
            1. Test Batch Name
            2. Category
            3. Severity
            4. Number of Test Cases
            5. Number of Passed Test Cases
            6. Number of Failed Test Cases
            7. Test Pass Rate
            8. Failing Features
            9. Duration
        """
        res = get_batch_result_response(
            self._backend, self._test_run_id, self._test_type
        )
        return parse_test_batch_result(res.test_batch)
