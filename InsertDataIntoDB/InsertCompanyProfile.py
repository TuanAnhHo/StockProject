## Insert data into COMPANY_PROFILE in postgresql database
## Notes: If the company profile of input symbol have already existed in database =>> raise Error existing profile

from sqlalchemy import create_engine
from CrawlFunction.GetAuthInfoFuncton import ReadConfigFile
from psycopg2 import OperationalError
from CrawlCompanyInfo import CrawlCompanyProfile

import psycopg2


class InsertCompanyProfile:
    
    def __init__(self,symbol:str):
        self.conn = self.ConnectPostgres()
        self.cursor = self.conn.cursor()
        self.symbol = symbol
        self.existing_symbol_list = self.ExistingCompanyProfile()
    
    
    ## Connect to Postgresql
    def ConnectPostgres(self):
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # read connection parameters
            params = ReadConfigFile("Authorization.ini","Postgresql")

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)
            
            # create a cursor
            cur = conn.cursor()
            
            # execute a statement
            print('PostgreSQL database version:')
            cur.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = cur.fetchone()
            print("Successfully connect to Postgresql")
            print(db_version)

        except OperationalError as e:
            raise e
        
        return conn


    def ExistingCompanyProfile(self) -> list:
        
        ## Get cursor connection
        cursor = self.cursor
        
        ## Get existing symbol in company_profile table
        GetExistingSymbol = """
            SELECT DISTINCT SYMBOL 
            FROM PUBLIC.COMPANY_PROFILE CP 
        """
        
        cursor.execute(GetExistingSymbol)
        existing_symbol_list = [i[0] for i in cursor]
        
        return existing_symbol_list

        
    def InsertDataFunction(self):
        
        if self.symbol in self.existing_symbol_list:
            raise ValueError("Your Input Symbol have already existed. Please try another symbol!")
        
        ## Get connection and change to cursor
        cursor = self.cursor

        ## Company profile data 
        print("Get Company profile of {symbol} symbol".format(symbol=self.symbol))
        data = CrawlCompanyProfile(self.symbol)

        ## Get columns name to insert data into table
        columns_list = data.keys()
        columns = ', '.join(x for x in columns_list)

        ## Get value to insert data into table
        values = tuple(data.values())

        InsertDataScripts = """
                INSERT INTO public.{table_name} ({columns})
                VALUES {values}
            """.format(table_name="company_profile", columns=columns, values=values)
        
        InsertDataScripts = InsertDataScripts.replace("None", "NULL")
        
        print("Insert profile of {symbol} symbol into table {table_name} in Postgresql".format(symbol=self.symbol, table_name="company_profile"))
        
        try:
            cursor.execute(InsertDataScripts)
            self.conn.commit()
            print("Inserted Successfully")
            print("Close connection")
            self.conn.close()
        
        except psycopg2.errors.UniqueViolation as e:
            print("Failed to insert data")
            raise e 

        return InsertDataScripts


A = InsertCompanyProfile("ACB").InsertDataFunction()
print(A)