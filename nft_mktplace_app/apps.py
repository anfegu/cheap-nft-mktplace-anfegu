import os, dotenv, json
from django.apps import AppConfig
from web3 import Web3

dotenv.load_dotenv()

class NftMktplaceAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nft_mktplace_app'

def get_web3():
    print("Connecting to Blockchain node...")
    web3 =  Web3(Web3.HTTPProvider(os.environ.get("WEB3_PROVIDER_URI")))
    print("Connected to Blockchain node:", web3.eth.chain_id)
    return web3

def get_contract(json_file):
    contract_info_path = os.path.join(
        os.path.dirname(__file__), 
        'blockchain_services/contractsJSON', 
        json_file
    )
    return json.loads(open(contract_info_path).read())