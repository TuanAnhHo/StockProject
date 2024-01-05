from CrawlFunction import *
import json

A = CrawlCompanyInfoBySymbol("HPG")
print(json.dumps(A.CrawlCompanyInfo(), indent = 4, ensure_ascii=False))