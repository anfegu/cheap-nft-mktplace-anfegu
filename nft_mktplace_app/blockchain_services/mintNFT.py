from ..apps import get_web3, get_contract
def mint_erc721_token(private_key):
    try:   
        if private_key:
            # Initiate the contract instance and connect to the blockchain
            CONTRACT_ABI = get_contract("NFT.json")["abi"]
            CONTRACT_ADDRESS = get_contract("NFT.json")["address"]

            web3 = get_web3()

            nft_contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
            account_address = web3.eth.account.from_key(private_key).address
        
            chain_id = web3.eth.chain_id
            gas_price = web3.eth.gas_price
            nonce = web3.eth.get_transaction_count(account_address)

            # Approve the contract
            approval_function = nft_contract.functions.setApprovalForAll(account_address, True).build_transaction(
                {
                    'chainId': chain_id,
                    'gas': 2000000,
                    'gasPrice': gas_price,
                    'nonce': nonce,
                }
            )
            signed_approval_transaction = web3.eth.account.sign_transaction(approval_function, private_key)
            tx_hash_approval = web3.eth.send_raw_transaction(signed_approval_transaction.rawTransaction)
            print("Approval transaction hash:", tx_hash_approval.hex())
            
            # Mint the NFT
            mint_function = nft_contract.functions.mint(account_address)
            mint_transaction = mint_function.build_transaction(
                {
                    'chainId': chain_id,
                    'gas': 2000000,
                    'gasPrice': gas_price * 2,
                    'nonce': nonce + 1,
                }
            )
            signed_mint_transaction = web3.eth.account.sign_transaction(mint_transaction, private_key)
            tx_hash_mint = web3.eth.send_raw_transaction(signed_mint_transaction.rawTransaction)
            print("Mint Transaction hash:", tx_hash_mint.hex())

            # Retrieve the NFT token ID
            receipt = web3.eth.wait_for_transaction_receipt(tx_hash_mint, timeout=120)
            if receipt is not None:
                balance = nft_contract.functions.balanceOf(account_address).call()
                token_id = nft_contract.functions.tokenOfOwnerByIndex(account_address, balance - 1).call()
            else:
                token_id = None
            return token_id
        else:
            return None
    except Exception as e:
        print("Error:", str(e))
        return None
