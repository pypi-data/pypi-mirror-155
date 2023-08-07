import os
from assembly_client.api.network_client import NetworkClient

DEFAULT_PATH = os.path.expanduser(
    "~/.symbiont/assembly-dev/dev-network/default/network-config.json"
)


def test_network_config():
    client = NetworkClient.from_network_config_file(DEFAULT_PATH, "foo")
    assert len(client.node_sessions) == 1
