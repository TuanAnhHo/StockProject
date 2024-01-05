import requests, pandas
from datetime import datetime

from AvailableStockSymbol import AvailableStock


## Function to fetch SSI API to get StockPrice of particular symbol in a range time
class CrawlStockPriceBySymbol:

    def __init__(self, symbol, from_date, to_date):
        self.symbol = symbol

        ## Using function ValidateRangeTime() to define start time and end time (both parameters are converted to seconds)
        self.RangeTimeConfig = self.ValidateRangeTime(from_date, to_date)

    ## Function to convert date string to seconds

    @staticmethod
    def ConvertDateToSeconds(input_date: str) -> int:
        return int(datetime.strptime(input_date, '%Y-%m-%d').timestamp()) + (
                    7 * 60 * 60)  ## Convert 7 hours to seconds to plus to input date because API response time default +7 hours

    def ValidateRangeTime(self, start_date: str, end_date: str) -> dict:
        from_date_converted = self.ConvertDateToSeconds(start_date)
        to_date_converted = self.ConvertDateToSeconds(end_date)

        if to_date_converted < from_date_converted:
            raise ValueError("Please import range time again beacause start date is greater end date")

        return {
            "from_date_convert": from_date_converted,
            "to_date_convert": to_date_converted,
        }

    def CrawlDataResponse(self):
        ## Set up URL base and Headers for API
        url_base = "https://iboard.ssi.com.vn/dchart/api/history?"
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36"
        }

        if self.symbol not in AvailableStock['symbol']:
            raise ValueError("The symbol is not availble. Please try another symbol")

        ## Call SSI API to get stock price and handle Error
        try:
            ## Note -- Response date concluded 7 fields: t: Time, c: ClosingPrice, o: OpenPrice, h: HighestPrice, l: LowerPrice, v: Volumn
            response = requests.get(
                url=url_base + "resolution=D&symbol={0}&from={1}&to={2}".format(self.symbol, self.RangeTimeConfig[
                    "from_date_convert"], self.RangeTimeConfig["to_date_convert"]),
                headers=headers
            )
            print("API Status Code " + str(response.status_code))

        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        return response.json()

    def ParseResponse(self):
        ## Parse response to Dataframe
        JsonResponse = self.CrawlDataResponse()

        if not JsonResponse.get('t'):
            print("There is no data")
            return None
        else:
            try:
                df_stock_data = pandas.DataFrame(JsonResponse)
                df_stock_data['t'] = df_stock_data['t'].apply(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d'))
                df_stock_data = df_stock_data.rename(columns={'t': 'StockDate',
                                                              'c': "ClosingPrice",
                                                              'o': 'OpeningPrice',
                                                              'h': 'HighestPrice',
                                                              'l': 'LowestPrice',
                                                              'v': 'Volumn'})

                return df_stock_data.drop(['s'], axis=1)

            except:
                raise ValueError("Failed to parse API response")
