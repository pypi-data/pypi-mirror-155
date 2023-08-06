"""Library defining the interface to a project."""
from typing import NamedTuple

import grpc

from rime_sdk.firewall import Firewall
from rime_sdk.internal.backend import RIMEBackend
from rime_sdk.protos.firewall.firewall_pb2 import (
    BatchMetadata,
    BinSize,
    ConvertIDsRequest,
    ConvertIDsResponse,
    CreateFirewallRequest,
    CreateFirewallResponse,
)
from rime_sdk.protos.firewall.firewall_pb2 import Firewall as FirewallProto
from rime_sdk.protos.firewall.firewall_pb2 import FirewallConvIDType
from rime_sdk.protos.project.project_pb2 import GetProjectRequest


class ProjectInfo(NamedTuple):
    """This object contains static information that describes a project."""

    project_id: str
    """How to refer to the project in the backend."""
    name: str
    """Name of the project."""
    description: str
    """Description of the project"""


class Project:
    """An interface to a RIME project.

    This object provides an interface for editing, updating, and deleting projects.

    Attributes:
        backend: RIMEBackend
            The RIME backend used to query about the status of the job.
        project_id: str
            The identifier for the RIME project that this object monitors.
    """

    def __init__(self, backend: RIMEBackend, project_id: str) -> None:
        """Contains information about a RIME Project.

        Args:
            backend: RIMEBackend
                The RIME backend used to query about the status of the job.
            project_id: str
                The identifier for the RIME project that this object monitors.
        """
        self._backend = backend
        self._project_id = project_id

    @property
    def project_id(self) -> str:
        """Return the id of this project."""
        return self._project_id

    @property
    def info(self) -> ProjectInfo:
        """Return information about this project."""
        project_req = GetProjectRequest(project_id=self._project_id)
        with self._backend.get_project_manager_stub() as project_manager:
            response = project_manager.GetProject(project_req)
        return ProjectInfo(
            self._project_id,
            response.project.project.name,
            response.project.project.description,
        )

    @property
    def name(self) -> str:
        """Return the name of this project."""
        return self.info.name

    @property
    def description(self) -> str:
        """Return the description of this project."""
        return self.info.description

    def create_firewall(self, name: str, bin_size: str, test_run_id: str) -> Firewall:
        """Create a Firewall for a given project.

        Args:
            name: str
                FW name.
            bin_size: str
                Bin size. Can be `year`, `month`, `week`, `day`, `hour`.
            test_run_id: str
                ID of the stress test run that firewall will be based on.

        Returns:
            A ``Firewall`` object.

        Raises:
            ValueError
                If the provided status_filters array has invalid values.
                If the request to the ModelTest service failed.

        Example:

        .. code-block:: python

            # Create FW based on foo stress test in project.
            firewall = project.create_firewall(
                "firewall name", 86400, "foo")
        """
        bin_size_proto = get_bin_size_proto(bin_size_str=bin_size)
        batch_metadata = BatchMetadata(bin_size=bin_size_proto)
        firewall = FirewallProto(
            name=name,
            stress_test_run_id=test_run_id,
            project_id=self._project_id,
            batch_metadata=batch_metadata,
        )
        req = CreateFirewallRequest(firewall=firewall)
        try:
            with self._backend.get_firewall_stub() as firewall_tester:
                res: CreateFirewallResponse = firewall_tester.CreateFirewall(req)
                return Firewall(self._backend, res.firewall_id)
        except grpc.RpcError as e:
            raise ValueError(e)

    def get_firewall(self) -> Firewall:
        """Get the active Firewall for a project if it exists.

        Query the backend for an active `Firewall` in this project which
        can be used to perform Firewall operations. If there is no active
        Firewall for the project, this call will error.

        Returns:
            A ``Firewall`` object.

        Raises:
            ValueError
                If the Firewall does not exist.

        Example:

        .. code-block:: python

            # Get FW if it exists.
            firewall = project.get_firewall()
        """
        src_type = FirewallConvIDType.FIREWALL_CONV_ID_TYPE_PROJECT_ID
        dst_type = FirewallConvIDType.FIREWALL_CONV_ID_TYPE_FIREWALL_ID
        req = ConvertIDsRequest(
            src_type=src_type, dst_type=dst_type, src_ids=[self._project_id]
        )
        try:
            with self._backend.get_firewall_stub() as firewall_tester:
                res: ConvertIDsResponse = firewall_tester.ConvertIDs(req)
                mapping = res.src_dst_id_mapping
                return Firewall(self._backend, mapping[self._project_id])
        except grpc.RpcError as e:
            raise ValueError(e)


def get_bin_size_proto(bin_size_str: str) -> BinSize:
    """Get bin size proto from string."""
    years = 0
    months = 0
    seconds = 0
    if bin_size_str == "year":
        years += 1
    elif bin_size_str == "month":
        months += 1
    elif bin_size_str == "week":
        seconds += 7 * 24 * 60 * 60
    elif bin_size_str == "day":
        seconds += 24 * 60 * 60
    elif bin_size_str == "hour":
        seconds += 60 * 60
    else:
        raise ValueError(
            f"Got unknown bin size ({bin_size_str}), "
            f"should be one of: `year`, `month`, `week`, `day`, `hour`"
        )
    return BinSize(years=years, months=months, seconds=seconds)
