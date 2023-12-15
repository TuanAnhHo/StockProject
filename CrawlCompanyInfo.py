import requests, json
from datetime import datetime
from AvailableStockSymbol import AvailableStock


## Function to crawl company profile from FireAnt
def CrawlCompanyProfile(symbol:str):
    
    if symbol not in AvailableStock['symbol']:
        raise ValueError("The symbol is not availble. Please try another symbol")
    
    ## Open "AuthorizationInfo.json" to get Authorization Information
    request_url = "https://restv2.fireant.vn/symbols/{symbol}/profile".format(symbol=symbol)
    
    with open("AuthorizationInfo.json", mode="r") as file:
        headers = json.load(file).get('FireAnt')
        
    try:
        response = requests.get(request_url, headers=headers)
        print("API Status Code " + str(response.status_code)) 
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    CompanyProfile = response.json()
    ListCrawlKeys= ['institutionID','symbol','icbCode','companyName','shortName','internationalName','phone', 
                    'employees','branches','establishmentDate','charterCapital','dateOfListing',
                    'exchange','listingVolume','stateOwnership', 'foreignOwnership', 'otherOwnership'
    ]
    
    CompanyProfileDict = {str(i): CompanyProfile[i] for i in ListCrawlKeys}
    CompanyProfileDict['overview'] = CompanyProfile['overview'].replace('\r\n','')
    
    return json.dumps(CompanyProfileDict, indent=4, ensure_ascii=False)


A = CrawlCompanyProfile("HPG")
print(A)