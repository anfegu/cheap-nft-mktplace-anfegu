from django.http import HttpResponse
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from nft_mktplace_app.blockchain_services.mintERC20 import mint_erc20_token
from nft_mktplace_app.blockchain_services.mintNFT import mint_erc721_token
from nft_mktplace_app.blockchain_services.settler_integration import settle_trade

from .models import NFTToken, Listing, Bid, Transaction
from .serializers import NFTTokenSerializer, ListingSerializer, BidSerializer, TransactionSerializer

def default_view(request):
    return HttpResponse("NFT Marketplace App is running!")

class NFTTokenViewSet(viewsets.ModelViewSet):
    queryset = NFTToken.objects.all()
    serializer_class = NFTTokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    def current_highest_bid(self, obj):
        return obj.current_highest_bid  if obj.is_auction else None

    current_highest_bid.short_description = 'Current Highest Bid'
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Additional logic for handling auctions or fixed-price listings can be added here
        
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check if the auction is still active
        listing_id = serializer.validated_data.get('listing').id
        try:
            listing = Listing.objects.get(id=listing_id)
        except Listing.DoesNotExist:
            return Response({'detail': 'Listing not found'}, status=status.HTTP_404_NOT_FOUND)

        if listing.is_auction and listing.end_time <= timezone.now():
            return Response({'detail': 'Auction has ended'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the bid amount is higher than the current highest bid
        bid_amount = serializer.validated_data.get('amount')
        if listing.is_auction and (listing.current_highest_bid is None or bid_amount > listing.current_highest_bid):
            listing.current_highest_bid = bid_amount
            listing.save()

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
    
        serializer.save()
    
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def settle_trade_view(request):
    try:
        auction_data = request.data.get('auctionData')
        bidder_signature = request.data.get('bidderSig')
        owner_signature = request.data.get('ownerApprovedSig')

        if not auction_data or not bidder_signature or not owner_signature:
            return Response({'error': 'Missing data in the request'}, status=status.HTTP_400_BAD_REQUEST)

        receipt = settle_trade(auction_data, bidder_signature, owner_signature)

        if receipt:
            return Response({'message': 'Trade settled successfully', 'receipt_hash': receipt}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Trade settlement failed'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def mint_erc721_token_view(request):
    try:
        private_key = request.data.get('private_key')

        if not private_key:
            return Response({'error': 'signature is required.'}, status=status.HTTP_400_BAD_REQUEST)

        token_id = mint_erc721_token(private_key)

        if token_id:
            return Response({'message': 'NFT minted successfully', 'nft_token_id': token_id}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'NFT minting failed'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def mint_erc20_token_view(request):
    try:
        private_key = request.data.get('private_key')
        amount = request.data.get('amount')

        if not private_key:
            return Response({'error': 'signature is required.'}, status=status.HTTP_400_BAD_REQUEST)

        balance_erc20_token = mint_erc20_token(private_key, amount)

        if balance_erc20_token:
            return Response({'message': 'TokenErc20 minted successfully', 'balance_erc20_token': balance_erc20_token}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'TokenErc20 minting failed'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    