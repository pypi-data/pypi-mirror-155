##########################
### nodes and networks ###
##########################

# a set of fixtures for managing and interacting with nodes, networks and associated low level kubernetes
# access.
#
### architectural themes
#
# * it is a conscious decision that each fixture either explicitly consumes output from another fixture,
#   or reads input directly from the pytest `request` fixture. as we already do a lot of input management
#   this way it is simplest to consistently use it for all our input management.
#
# * these fixtures are designed assuming a user can access the system at multiple levels, in some cases
#   they will want a fully built network and not think about anything, but in others they will want to
#   start with nothing more than a kubernetes context
#
# * abstraction by subclassing and not composition is used to enrich a set of nodes with kubernetes
#   functionality as it really truly is just nodes but with more functionality. using composition requires
#   a bunch of manual dispatch between the composed pieces that is undesirable
#
# * if users directly build their own network, they will want to build the various instances directly, so
#   the classes themselves must have high quality interfaces


from assembly_client.api import node_api_client
from assembly_client.api.network_client import NetworkClient
from _assembly.sdk import get_network_config

from assembly_client.api.job_management import Job, ContractErrorInJob
from assembly_client.api.types.error_types import ContractError


###############################
### user api and data model ###
###############################


class Nodes:
    """
    this is the raw set of nodes, and supports operations that one performs on nodes directly
    """

    def __init__(self, sessions, neo_key, neo_crt):
        # a simple dictionary of string node name to `NodeSession` from our http client
        self.sessions = sessions
        self.neo_key = neo_key
        self.neo_crt = neo_crt


#######################################
### fixture builder implementations ###
#######################################

### automatic postgres management

### network


class SyncNetworkClient(NetworkClient):
    def async_call(self, key_alias, contract_ref, function, kwargs):
        """
        calls the specified contract function on a node
        :param key_alias: key_alias to invoke as
        :param contract_ref: contract to call
        :param function: function to invoke
        :param kwargs: dictionary of arguments to the contract, will be json serialized
        :return: the result of the call as a value or job object
        """
        session = self.node_sessions[self.alias_locations[key_alias]]

        # if this clientside does not post, it'll be the value read, otherwise a job
        result = node_api_client.call(
            session,
            key_alias,
            contract_ref,
            function,
            kwargs,
            query_tx_index=self.query_tx_index,
        )
        self.query_tx_index = None

        if isinstance(result, Job):
            try:
                completed_job = result.start_waiting(timeout=self.timeout)
            except ContractErrorInJob as e:
                raise ContractError(e.msg, e.data)
            completed_job.network_client = self
            completed_job.sync_with(timeout=self.timeout)
            return completed_job.result["result"]
        return result


def network_fixture(sdk_args, cls=SyncNetworkClient):

    if sdk_args.network_name is not None:
        network_config = get_network_config(sdk_args.network_name)
    elif sdk_args.connection_file is not None:
        network_config = sdk_args.connection_file
    elif sdk_args.network_config is not None:
        network_config = sdk_args.network_config
    else:
        network_config = get_network_config("default")

    client = cls.from_network_config_file(
        network_config, sdk_args.contract_path, timeout=sdk_args.timeout
    )
    client.wait_for_ready()

    return client
