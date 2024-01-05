import requests
from AvailableStockSymbol import AvailableStock
from GetAuthInfoFuncton import ReadConfigFile


# Function to crawl company profile from FireAnt
class CrawlCompanyInfoBySymbol:

    def __init__(self, symbol: str) -> None:
        self.symbol = symbol

    def CrawlCompanyInfo(self):

        if self.symbol not in AvailableStock['symbol']:
            raise ValueError("The symbol is not availble. Please try another symbol")

        # Open "AuthorizationInfo.json" to get Authorization Information
        request_url = "https://restv2.fireant.vn/symbols/{symbol}/profile".format(symbol=self.symbol)
        # Using ReadConfigFile function to get Authorization information of FireAnt
        headers = ReadConfigFile("/Users/anhho/Desktop/DataEngineer/CrawlStockData/CrawlFunction/Authorization.ini",
                                 "FireAnt")

        try:
            response = requests.get(request_url, headers=headers)
            print("API Status Code " + str(response.status_code))
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        CompanyProfile = response.json()
        ListCrawlKeys = ['institutionID', 'symbol', 'icbCode', 'companyName', 'shortName', 'internationalName', 'phone',
                         'employees', 'branches', 'establishmentDate', 'charterCapital', 'dateOfListing',
                         'exchange', 'listingVolume', 'stateOwnership', 'foreignOwnership', 'otherOwnership'
                         ]

        CompanyProfileDict = {str(i): CompanyProfile[i] for i in ListCrawlKeys}
        CompanyProfileDict['overview'] = CompanyProfile['overview'].replace('\r\n', '')

        return CompanyProfileDict

