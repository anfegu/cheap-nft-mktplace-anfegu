# Backend Cheap NFT Marketplace App

This project is a simple Back-end NFT Marketplace app implemented using Django to manage listings, bids, and trade settlements via a Settler contract.

## Table of Contents
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [API Endpoints](#api-endpoints)
  - [Trade Settlement](#trade-settlement)
- [Project Structure](#project-structure)
  - [Model](#model)
- [Postman Simulation](#postman-simulation)

## Getting Started

### Prerequisites
- Python
- Django
- Django Rest Framework
- Web3 (for blockchain integration)
- Sepolia Network tools

### Installation

1. Clone the repository:

   git clone https://github.com/anfegu/cheap-nft-mktplace-anfegu.git

2. Navigate to the project directory

	cd nft-mktplace-app

3. Create a virtual environment and activate it (optional but recommended):

	python -m venv myenvsource
 	myenv/bin/activate  
	# On Linux/macOS# Or for Windows: myenv\Scripts\activate

4. Copy the .env_sample file to the .env file	:

	cp .env_sample .env

5. Install project dependencies:

	pip install -r requirements.txt

6. Migrate the database:

	python manage.py migrate

7. Run the development server:

	python manage.py runserver

## Usage

### API Endpoints
Use the following API endpoints to interact with the NFT Marketplace:

- List NFTs: `/api/nfttokens/`
- Create Listings: `/api/listings/`
- Place Bids: `/api/bids/`
- Settle Trades (finishAuction): `/settle_trade/`
- Mint MockNFT721: `/mint_nft/`
- Mint MockERC20: `/mint_erc20/`

#### Trade Settlement

To settle a trade using the Settler contract, you need to make a POST request to the `/settle_trade/` endpoint with the required data, including auction data, bidder signature, and owner signature.

##### Example JSON Payload:

```json
{
"auction_data": {
 "collectionAddress": "0xYourCollectionAddress",
"erc20Address": "0xYourERC20Address",
"tokenId": 12345,
 "bid": 1000
 },
"bidder_signature": "0xYourBidderSignature",
"owner_signature": "0xYourOwnerSignature"
}

## Project Structure

The project is structured as follows:

- `nft_marketplace_project/`: Django project directory.
- `nft_marketplace_app/`: Django app directory containing models, serializers, views, and URLs.
- `blockchain_services/settler_integration.py`: Module for Settler contract integration.
- `blockchain_services/mintERC20.py`: Module for Mint MockERC20 Fungible Token, contract integration.
- `blockchain_services/mintNFT.py`: Module for Mint MockERC721 NFT, contract integration.

### Model

| Model | Fields | Description |
|---|---|---|
| NFTToken | id, name, description | A model to represent an NFT token. |
| Listing | id, token, seller, price, is_auction, start_time, end_time, current_highest_bid | A model to represent a listing for an NFT token. |
| Bid | id, listing, bidder, amount | A model to represent a bid on an NFT token listing. |
| Transaction | id, listing, buyer, amount, settled | A model to represent a transaction for an NFT token purchase. |


## Cheap NFT Marketplace API - Postman Simulation.

This repository contains a Postman collection for testing an NFT marketplace API.

### Import the Collection

To get started, import the `nft-marketplace.postman_collection.json` file into Postman:

1. Click the import button to open the import modal.
2. Select the Files tab and choose the collection file.
3. The collection will be added to your Postman workspace.

### Configure Environment Variables

The collection depends on some environment variables for values like API keys:

1. In Postman, select the cog icon in the top right to open settings.
2. Go to the Environments tab and click Add.
3. Create a new environment titled "NFT Marketplace Testing".
4. Add the following variables:
    * user_a_private_key - Private key for User A's wallet
    * user_b_private_key - Private key for User B's wallet
5. Save the environment.

### Run the Collection

With the environment configured, you can run the full collection:

1. Expand the NFT Marketplace collection on the left sidebar.
2. Click the Run button at the top to open the collection runner.
3. Select the "NFT Marketplace Testing" environment.
4. Click Run NFT Marketplace to execute all requests sequentially.

This will call endpoints like minting an NFT, creating a listing, placing bids, and settling trades end-to-end.

The test results and response data can be viewed for each request in the collection runner.
