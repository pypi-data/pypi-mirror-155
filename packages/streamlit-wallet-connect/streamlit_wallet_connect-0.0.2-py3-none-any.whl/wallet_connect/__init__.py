import streamlit.components.v1 as components
import streamlit as st
import os

# from ocean_lib.ocean.ocean import Ocean
# from ocean_lib.config import Config
# from ocean_lib.web3_internal.wallet import Wallet
# from ocean_lib.web3_internal.constants import ZERO_ADDRESS
# from ocean_lib.common.agreements.service_types import ServiceTypes
# from ocean_lib.web3_internal.currency import pretty_ether_and_wei
# from ocean_lib.models.compute_input import ComputeInput
# from ocean_lib.models.btoken import BToken #BToken is ERC20
# from ocean_lib.web3_internal.currency import to_wei
# from ocean_lib.example_config import ExampleConfig

# d = {
#     'network' : 'https://rinkeby.infura.io/v3/d163c48816434b0bbb3ac3925d6c6c80',
#     'BLOCK_CONFIRMATIONS': 0,
#    'metadataCacheUri' : 'https://aquarius.oceanprotocol.com',
#    'providerUri' : 'https://provider.rinkeby.oceanprotocol.com',
#    'PROVIDER_ADDRESS': '0x00bd138abd70e2f00903268f3db08f2d25677c9e',
#    'downloads.path': 'consume-downloads',
# }

parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "frontend/build")
_wallet_connect = components.declare_component("wallet_connect", path=build_dir)

reconnect = _wallet_connect(label="k", default='d',key='ke')
# ocean = Ocean(d)
# OCEAN_token = BToken(ocean.web3, ocean.OCEAN_address)
# _DATA_URL = "https://drive.google.com/file/d/1d01VQ1plsB8ZIO5VF0LKV2MxdNQjvoCW/view?usp=sharing"

def get_button(label, key=None):
    return _wallet_connect(label=label, default="not", key=key)

def connect(label, show_status=False, key=None):
    wallet_button = get_button(label="wallet", key="wallet")
    if show_status:
        st.write(f"Wallet {wallet_button} connected.")
    return wallet_button