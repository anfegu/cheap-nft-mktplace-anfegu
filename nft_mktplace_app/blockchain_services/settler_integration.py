from collections import namedtuple
from sys import abiflags
from ..apps import get_web3, get_contract
from eth_account.messages import encode_defunct

AUCTION_DATA = namedtuple(
    "AuctionData", [
        "collectionAddress", 
        "erc20Address", 
        "tokenId", 
        "bid"
    ]
)

def settle_trade(auction_data, bidder_signature, owner_signature):
    """
    Initiate trade settlement using the Settler contract.

    :param auction_data: Auction data (tuple)
    :param bidder_signature: Bidder's cryptographic signature (bytes)
    :param owner_signature: Owner's cryptographic signature (bytes)
    :return: Transaction receipt or None
    """
    try:
        CONTRACT_ABI = get_contract("Settler.json")["abi"]
        CONTRACT_ADDRESS = get_contract("Settler.json")["address"]
        
        web3 = get_web3()

        auction_data_tuple = (
            auction_data["collectionAddress"], 
            auction_data["erc20Address"], 
            auction_data["tokenId"], 
            auction_data["bid"]
        )

        message_hash = web3.solidity_keccak( 
            ['address', 'address', 'uint256', 'uint256'], 
             auction_data_tuple          
        )
       
        bidder_sig = web3.eth.account.sign_message(encode_defunct(hexstr=message_hash.hex()), private_key=bidder_signature)
        owner_sig = web3.eth.account.sign_message(encode_defunct(hexstr=bidder_sig.signature.hex()), private_key=owner_signature)
        
        #auction_data = AUCTION_DATA(**auction_data)
        
        # Create a contract instance
        settler_contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
        
        # Finish the auction
        transaction = settler_contract.functions.finishAuction(
            auction_data_tuple,
            bidder_sig.signature,
            owner_sig.signature,
        ).build_transaction({
            'chainId': web3.eth.chain_id,
            'gas': 5000000,  
            'gasPrice': web3.eth.gas_price * 4,  
            'nonce': web3.eth.get_transaction_count(web3.eth.account.from_key(bidder_signature).address),
        })

        # Sign the transaction
        signed_transaction = web3.eth.account.sign_transaction(transaction, bidder_signature)

        # Send the transaction
        transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        return web3.eth.wait_for_transaction_receipt(transaction_hash, timeout=120)

    except Exception as e:
        print(f"Error settling trade: {str(e)}")
        return None
 

