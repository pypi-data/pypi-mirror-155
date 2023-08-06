"""Library defining the interface to a test run object."""
from typing import Optional

import grpc
import pandas as pd
from google.protobuf.json_format import MessageToDict
from semver import VersionInfo

from rime_sdk.internal.backend import RIMEBackend
from rime_sdk.internal.protobuf_parser import parse_test_run_metadata
from rime_sdk.internal.test_helpers import get_batch_result_response
from rime_sdk.protos.test_run_results.test_run_results_pb2 import (
    GetTestRunRequest,
    GetTestRunResponse,
    ListTestCasesRequest,
    ListTestCasesResponse,
)
from rime_sdk.tests import TestBatch


class TestRun:
    """An interface for a RIME test run.

    Attributes:
        backend: RIMEBackend
            The RIME backend used to query about the test run.
        test_run_id: str
            The string identifier for the successfully completed test run.
    """

    def __init__(self, backend: RIMEBackend, test_run_id: str) -> None:
        """Create a new TestRun object.

        Arguments:
            backend: RIMEBackend
                The RIME backend used to query about the test run.
            test_run_id: str
                The string identifier for the successfully completed test run.
        """
        self._test_run_id = test_run_id
        self._backend = backend

    def get_result_df(self, version: Optional[str] = None) -> pd.DataFrame:
        """Retrieve high level summary information for a complete stress test run in a\
        single-row dataframe.

        This dataframe includes information such as model metrics on the reference and\
        evalulation datasets, overall RIME results such as severity across tests,\
        and high level metadata such as the project ID and model task.

        By concatenating these rows together, this allows you to build a table of test
        run results for sake of comparison. This only works on stress test jobs that
        have succeeded.

        Note: this does not work on <0.14.0 RIME test runs.

        Arguments:
            version: Optional[str] = None`
                Semantic version of the results to be returned.
                This allows users to pin the version of the results, which is helpful
                if you write any code on top of RIME data. If you upgrade the SDK and
                do not pin the version in your code, it may break because the output
                not guaranteed to be stable across versions.
                The latest output will be returned by default.

        Returns:
            A `pandas.DataFrame` object containing the test run result.
            There are a lot of columns, so it is worth viewing them with the `.columns`
            method to see what they are. Generally, these columns have information
            about the model and datasets as well as summary statistics like the number
            of failing test cases or number of high severity test cases.

        Example:

        .. code-block:: python

            # Wait until the job has finished, since this method only works on
            # succeeded jobs.
            job.get_status(verbose=True, wait_until_finish=True)
            # Dump the test cases in dataframe ``df``.
            # Pin the version to RIME version 0.14.0.
            df = job.get_test_run_result(version="0.14.0")
            # Print out the column names and types.
            print(df.columns)
        """
        if version and not VersionInfo.isvalid(version):
            raise ValueError(f"Invalid version string: {version}")

        with self._backend.get_test_run_results_stub() as results_reader:
            # Fetch test run metadata and return a dataframe of the single row.
            req = GetTestRunRequest(test_run_id=self._test_run_id)
            try:
                res: GetTestRunResponse = results_reader.GetTestRun(req)
                # Use utility funtion for converting Protobuf to a dataframe.
                return parse_test_run_metadata(res.test_run, version=version)
            except grpc.RpcError as e:
                raise ValueError(e)

    def get_test_cases_df(self, version: Optional[str] = None) -> pd.DataFrame:
        """Retrieve all the test cases for a completed stress test run in a dataframe.

        This gives you the ability to perform granular queries on test cases.
        For example, if you only care about subset performance tests and want to see
        the results on each feature, you can fetch all the test cases in a dataframe,
        then query on that dataframe by test type. This only works on stress test jobs
        that have succeeded.

        Note: this will not work for test runs run on RIME versions <0.14.0.

        Arguments:
            version: Optional[str] = None
                Semantic version of the results to be returned.
                This allows users to pin the version of the results, which is helpful
                if you write any code on top of RIME data. If you upgrade the SDK and
                do not pin the version in your code, it may break because the output
                not guaranteed to be stable across versions.
                The latest output will be returned by default.

        Returns:
            A ``pandas.DataFrame`` object containing the test case results.
            Here is a selected list of columns in the output:
            1. ``test_run_id``: ID of the parent test run.
            2. ``features``: List of features that the test case ran on.
            3. ``test_batch_type``: Type of test that was run (e.g. Subset AUC,\
                Must be Int, etc.).
            4. ``status``: Status of the test case (e.g. Pass, Fail, Skip, etc.).
            5. ``severity``: Metric that denotes the severity of the failure of\
                the test.

        Example:

        .. code-block:: python

            # Wait until the job has finished, since this method only works on
            # SUCCEEDED jobs.
            job.get_status(verbose=True, wait_until_finish=True)
            # Dump the test cases in dataframe ``df``.
            # Pin the version to RIME version 0.14.0.
            df = job.get_test_cases_result(version="0.14.0")
            # Print out the column names and types.
            print(df.columns)
        """
        if version and not VersionInfo.isvalid(version):
            raise ValueError(f"Invalid version string: {version}")

        with self._backend.get_test_run_results_stub() as results_reader:
            all_test_cases = []
            # Iterate through the pages of test cases and break at the last page.
            page_token = ""
            previous_token = ""
            while True:
                tc_req = ListTestCasesRequest(
                    test_run_id=self._test_run_id, page_token=page_token, page_size=20,
                )
                try:
                    res: ListTestCasesResponse = results_reader.ListTestCases(tc_req)
                    tc_dicts = [
                        MessageToDict(
                            tc,
                            including_default_value_fields=True,
                            preserving_proto_field_name=True,
                        )
                        for tc in res.test_cases
                    ]
                    # Concatenate the list of test case dictionaries.
                    all_test_cases += tc_dicts
                    previous_token = page_token
                    # Advance to the next page of test cases.
                    page_token = res.next_page_token
                except grpc.RpcError as e:
                    raise ValueError(e)
                # we've reached the last page of test cases.
                if page_token == previous_token:
                    break

            # Drop selected columns from test cases dataframe.
            columns_to_drop = ["importance_score"]
            return pd.DataFrame(all_test_cases).drop(columns=columns_to_drop)

    def get_test_batch(
        self, test_type: str, version: Optional[str] = None
    ) -> TestBatch:
        """Obtain the corresponding test batch."""
        if version and not VersionInfo.isvalid(version):
            raise ValueError(f"Invalid version string: {version}")
        test_batch_obj = TestBatch(self._backend, self._test_run_id, test_type)
        # check that test batch exists by sending a request
        get_batch_result_response(self._backend, self._test_run_id, test_type)
        return test_batch_obj
