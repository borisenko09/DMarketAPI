import requests
import json
from datetime import datetime
from nacl.signing import SigningKey
from nacl.encoding import HexEncoder

class DMarketAPI:
    def __init__(self, public_key, secret_key):
        self.public_key = public_key
        self.secret_key = secret_key
        self.api_url = 'https://api.dmarket.com'
        self.session = requests.Session()
        self.session.verify = False

    def _generate_signature(self, method, url, params, body, timestamp):
        secret_key_bytes = bytes.fromhex(self.secret_key[:64])

        params_string = "&".join([f"{key}={value}" for key, value in sorted(params.items())]) if params else ""
        str_to_sign = f"{method.upper()}{url}{f'?{params_string}' if params_string else ''}{json.dumps(body) if body else ''}{timestamp}"

        sign_key = SigningKey(secret_key_bytes)
        signed = sign_key.sign(str_to_sign.encode())
        return signed.signature[:64].hex()

    def _send_request(self, method, endpoint, params={}, body=None):
        timestamp = int(datetime.now().timestamp())
        signature = self._generate_signature(method, endpoint, params, body, timestamp)

        headers = {
            'X-Api-Key': self.public_key,
            'X-Request-Sign': 'dmar ed25519 ' + signature,
            'X-Sign-Date': str(timestamp),
            'Content-Type': 'application/json'
        }

        url = self.api_url + endpoint
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, params=params)
        else:
            response = requests.post(url, headers=headers, json=body)

        return response.json()

    def get_user_profile(self):
        """
        Get general user profile information.

        :return: Response from the Dmarket API containing user profile information.
        """
        endpoint = '/account/v1/user'
        return self._send_request('GET', endpoint)
    def get_user_balance(self):
        """
        Get the current USD & DMC balance of the user.

        :return: Response from the Dmarket API containing user balance information.
        """
        endpoint = '/account/v1/balance'
        return self._send_request('GET', endpoint)
    def deposit_assets(self, deposit_request_body):
        """
        Transferring items from a 3rd party inventory to a Dmarket inventory.

        :param deposit_request_body: A dictionary that matches the marketplaceDepositAssetsRequest schema.
        :return: Response from the Dmarket API.
        """
        endpoint = '/marketplace-api/v1/deposit-assets'
        return self._send_request('POST', endpoint, body=deposit_request_body)
    def get_deposit_status(self, deposit_id):
        """
        Get information about current deposit transfers.

        :param deposit_id: Unique identifier of the deposit operation.
        :return: Response from the Dmarket API.
        """
        endpoint = f'/marketplace-api/v1/deposit-status/{deposit_id}'
        return self._send_request('GET', endpoint)
    def get_user_offers(self, params={}):
        """
        Get the list of offers of the current user for further management.

        :param params: Dictionary of query parameters including GameID, Status, SortType, 
                       BasicFilters (PriceFrom, PriceTo, Currency), Offset, Limit, Cursor.
        :return: Response from the Dmarket API.
        """
        endpoint = '/marketplace-api/v1/user-offers'
        return self._send_request('GET', endpoint, params=params)
    def create_offers(self, create_offers_request_body):
        """
        Batch offers creation. Locks the selected asset and creates a new offer in the market.

        :param create_offers_request_body: A dictionary that matches the 
                                           marketplaceCreateOffersRequest schema.
        :return: Response from the Dmarket API.
        """
        endpoint = '/marketplace-api/v1/user-offers/create'
        return self._send_request('POST', endpoint, body=create_offers_request_body)
    def edit_offers(self, edit_offers_request_body):
        """
        Change the sale price for existing offers.

        :param edit_offers_request_body: A dictionary that matches the 
                                         marketplaceEditOffersRequest schema.
        :return: Response from the Dmarket API.
        """
        endpoint = '/marketplace-api/v1/user-offers/edit'
        return self._send_request('POST', endpoint, body=edit_offers_request_body)
    def get_market_items(self, params):
        """
        Get the list of items available for purchase on DMarket.

        :param params: Dictionary of query parameters including gameId, title, limit, offset,
                       orderBy, orderDir, treeFilters, currency, priceFrom, priceTo, types, cursor.
        :return: Response from the Dmarket API.
        """
        endpoint = '/exchange/v1/market/items'
        return self._send_request('GET', endpoint, params=params)
    def delete_offers(self, manage_offers_request_body):
        """
        Remove offers from sale. Unlocks the item and removes it from the market.

        :param manage_offers_request_body: A dictionary that matches the 
                                           entity.ManageOffersRequest schema.
        :return: Response from the Dmarket API.
        """
        endpoint = '/exchange/v1/offers'
        return self._send_request('DELETE', endpoint, body=manage_offers_request_body)
    def get_user_inventory(self, params):
        """
        Get user inventory details. Merges both 3rd party and DMarket inventories.

        :param params: Dictionary of query parameters including GameID, BasicFilters (Title, 
                       InMarket, HasSteamLock, SteamLockDays, AssetID), SortType, Presentation,
                       Offset, Limit, Cursor.
        :return: Response from the Dmarket API.
        """
        endpoint = '/marketplace-api/v1/user-inventory'
        return self._send_request('GET', endpoint, params=params)
    def sync_user_inventory(self, sync_inventory_request_body):
        """
        Update DMarket inventory details to sync them with data from Steam.

        :param sync_inventory_request_body: A dictionary that matches the 
                                           marketplaceUserInventorySyncRequest schema.
        :return: Response from the Dmarket API.
        """
        endpoint = '/marketplace-api/v1/user-inventory/sync'
        return self._send_request('POST', endpoint, body=sync_inventory_request_body)
    def withdraw_assets(self, withdraw_assets_request_body):
        """
        Withdraw assets from DMarket inventory.

        :param withdraw_assets_request_body: A dictionary that matches the 
                                             entity.WithdrawAssetsRequest schema.
        :return: Response from the Dmarket API.
        """
        endpoint = '/exchange/v1/withdraw-assets'
        return self._send_request('POST', endpoint, body=withdraw_assets_request_body)
    def get_user_items(self, params):
        """
        Get user inventory details filtered by a certain game, including both DMarket-stored and 
        Steam-stored items (excluding items for sale).

        :param params: Dictionary of query parameters including gameId, title, limit, offset, 
                       orderBy, orderDir, treeFilters, currency, priceFrom, priceTo, classIds, cursor.
        :return: Response from the Dmarket API.
        """
        endpoint = '/exchange/v1/user/items'
        return self._send_request('GET', endpoint, params=params)
    def get_customized_fees(self, params):
        """
        Get the list of items with lower fees, updated daily.

        :param params: Dictionary of query parameters including gameId, offerType, limit, offset.
        :return: Response from the Dmarket API.
        """
        endpoint = '/exchange/v1/customized-fees'
        return self._send_request('GET', endpoint, params=params)
    def get_user_closed_offers(self, params):
        """
        Get the list of the user's closed sell offers.

        :param params: Dictionary of query parameters including Offset, Limit, OrderDir.
        :return: Response from the Dmarket API.
        """
        endpoint = '/marketplace-api/v1/user-offers/closed'
        return self._send_request('GET', endpoint, params=params)
    def get_offers_by_title(self, params):
        """
        Get the list of all offers for a single item title.

        :param params: Dictionary of query parameters including Title, Limit, Cursor.
        :return: Response from the Dmarket API.
        """
        endpoint = '/exchange/v1/offers-by-title'
        return self._send_request('GET', endpoint, params=params)
    def get_aggregated_prices(self, params):
        """
        Get the best market prices grouped by item market title.

        :param params: Dictionary of query parameters including Titles (array of strings), 
                       Limit, Offset.
        :return: Response from the Dmarket API.
        """
        endpoint = '/price-aggregator/v1/aggregated-prices'
        return self._send_request('GET', endpoint, params=params)
    def get_user_targets(self, params):
        """
        Get the list of user's targets on DMarket.

        :param params: Dictionary of query parameters including GameID, BasicFilters (PriceFrom, 
                       PriceTo, Currency, Title, TargetID, Status), SortType, Offset, Limit, Cursor.
        :return: Response from the Dmarket API.
        """
        endpoint = '/marketplace-api/v1/user-targets'
        return self._send_request('GET', endpoint, params=params)
    def get_user_closed_targets(self, params):
        """
        Get the list of the user's closed targets on DMarket.

        :param params: Dictionary of query parameters including Offset, Limit, OrderDir.
        :return: Response from the Dmarket API.
        """
        endpoint = '/marketplace-api/v1/user-targets/closed'
        return self._send_request('GET', endpoint, params=params)
    def create_targets(self, create_targets_request_body):
        """
        Create targets for buying items on DMarket.

        :param create_targets_request_body: A dictionary that matches the 
                                            marketplaceCreateTargetsRequest schema.
        :return: Response from the Dmarket API.
        """
        endpoint = '/marketplace-api/v1/user-targets/create'
        return self._send_request('POST', endpoint, body=create_targets_request_body)
    def delete_targets(self, delete_targets_request_body):
        """
        Remove user's buying targets on DMarket.

        :param delete_targets_request_body: A dictionary that matches the 
                                            marketplaceDeleteTargetsRequest schema.
        :return: Response from the Dmarket API.
        """
        endpoint = '/marketplace-api/v1/user-targets/delete'
        return self._send_request('POST', endpoint, body=delete_targets_request_body)
    def buy_offers(self, buy_offers_request_body):
        """
        Buy selected offers from the market.

        :param buy_offers_request_body: A dictionary that matches the 
                                        entity.OfferBuyRequest schema.
        :return: Response from the Dmarket API.
        """
        endpoint = '/exchange/v1/offers-buy'
        return self._send_request('PATCH', endpoint, body=buy_offers_request_body)
    def get_last_sales(self, params):
        """
        Get the item sales history for up to the last 12 months.

        :param params: Dictionary of query parameters including gameId, title, filters, 
                       txOperationType, limit, offset.
        :return: Response from the Dmarket API.
        """
        endpoint = '/trade-aggregator/v1/last-sales'
        return self._send_request('GET', endpoint, params=params)
    
