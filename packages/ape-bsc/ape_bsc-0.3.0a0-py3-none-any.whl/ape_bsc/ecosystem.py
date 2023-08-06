from ape.api.config import PluginConfig
from ape.api.networks import LOCAL_NETWORK_NAME
from ape_ethereum.ecosystem import Ethereum, NetworkConfig

NETWORKS = {
    # chain_id, network_id
    "mainnet": (56, 56),
    "testnet": (97, 97),
}


class BSCConfig(PluginConfig):
    mainnet: NetworkConfig = NetworkConfig(required_confirmations=1, block_time=3)  # type: ignore
    testnet: NetworkConfig = NetworkConfig(required_confirmations=1, block_time=3)  # type: ignore
    local: NetworkConfig = NetworkConfig(default_provider="test")  # type: ignore
    default_network: str = LOCAL_NETWORK_NAME


class BSC(Ethereum):
    @property
    def config(self) -> BSCConfig:  # type: ignore
        return self.config_manager.get_config("bsc")  # type: ignore
