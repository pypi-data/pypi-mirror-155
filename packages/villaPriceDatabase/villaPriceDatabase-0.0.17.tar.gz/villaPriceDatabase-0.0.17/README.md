# villa inventory database model
> serverless database to take control of products inventory


This file will become your README and also the index of your documentation.

## Install

`pip install villaInvDatabase`

## How to use

interact with a database hosted in dynamodb

```
import os
os.environ['DATABASE_TABLE_NAME'] = 'inventory-database-dev-manual'
os.environ['REGION'] = 'ap-southeast-1'
os.environ['INVENTORY_BUCKET_NAME'] = 'inventory-bucket-dev-manual'
os.environ['INPUT_BUCKET_NAME'] = 'input-bucket-dev-manual'
os.environ['DAX_ENDPOINT'] = 'longtermcluster.vuu7lr.clustercfg.dax.apse1.cache.amazonaws.com:8111'
try:
  with open(os.path.expanduser('~/.testbot')) as f: os.environ['SLACK'] =  f.read()
except:
  print('cant load slack key')
# os.environ['DAX_ENDPOINT'] = None
REGION = 'ap-southeast-1'
INVENTORY_BUCKET_NAME = os.environ['INVENTORY_BUCKET_NAME']
INPUT_BUCKET_NAME = os.environ['INPUT_BUCKET_NAME']
```

```
from villaInvDatabase.database import Database
```

```
sampleInput = [ 
  { 'ib_prcode': '0000009', 'ib_brcode': '1000', 'ib_cf_qty': '50', 'new_ib_vs_stock_cv': '27' },
  { 'ib_prcode': '0000002', 'ib_brcode': '1000', 'ib_cf_qty': '35', 'new_ib_vs_stock_cv': '33' }
              ]
```

```
from villaInvDatabase.database import Database
from s3bz.s3bz import S3
from pprint import pprint

import pickle, json, boto3, bz2, requests, validators, os, logging
```

```
%%time
#update
Database.dumpToS3(user=USER, pw = PW)
```

    CPU times: user 55.4 ms, sys: 0 ns, total: 55.4 ms
    Wall time: 1.09 s





    {'newDataSaved': False,
     'numberOfProducts': 0,
     'message': 'no changes to database'}



```
%%time
Database.splitBranches(bucket = INVENTORY_BUCKET_NAME, user=USER, pw=PW)
```

    CPU times: user 20.5 s, sys: 412 ms, total: 20.9 s
    Wall time: 25.6 s





    {'success': 32, 'failure': 0, 'errorMessage': []}



# Save using Standard

```
Database.updateLambdaInput(sampleInput)
```




    {'success': 0, 'failure': 0, 'failureMessage': []}



## Save using s3

```
inputKeyName = 'input-data-name'
saveResult = S3.save(key=inputKeyName, 
                     objectToSave = sampleInput , 
                     bucket = INPUT_BUCKET_NAME,
                     user = USER,
                     pw = PW,
                     accelerate = False)
logging.info('test input data saved to s3')
updateResult = Database.updateS3Input(
  inputBucketName=INPUT_BUCKET_NAME, key= inputKeyName,
  user = USER, pw = PW)

logging.info(f's3 save result is {saveResult} update result is {updateResult}')
```

## Query test

#### Product Query

```
sampleQueryInput = {
    'ib_prcode': '0000002'
}  
```

```
Database.singleProductQuery(sampleQueryInput)
```




    {"ib_prcode": "0000002", "1000": {"ib_cf_qty": 35, "new_ib_bs_stock_cv": 33, "lastUpdate": 1600567810.529301}, "1001": {"ib_cf_qty": 32, "new_ib_bs_stock_cv": 30, "lastUpdate": 1600567810.529316}, "1002": {"ib_cf_qty": 34, "new_ib_bs_stock_cv": 30, "lastUpdate": 1600567810.529318}, "lastUpdate": 1600567810.529318}



### Branch Query

```
from s3bz.s3bz import Requests
branchURL = Database.branchQuery('1000', bucket = INVENTORY_BUCKET_NAME, user=USER, pw=PW)
print(branchURL)
next(iter(Requests.getContentFromUrl(branchURL).items()))
```

    https://inventory-bucket-dev-manual.s3-accelerate.amazonaws.com/1000?AWSAccessKeyId=ASIAVX4Z5TKDVIXEQMRN&Signature=4h8%2BCpX1qebIMFffYzj0gel%2Fp4I%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEIH%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLXNvdXRoZWFzdC0xIkcwRQIhAKLtSNdLUC1O0Hr5yduzO6d1H6xmshZEvnR26nUJV6vzAiAI25lYEFOu9rUo6hxLc7iPqKPshHE8A2iLbJVE0YLl1SrgAgi7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDM5NDkyMjkyNDY3OSIM99g2ugGfetoq3FQEKrQCoG4IWFWZ%2F8ZjqVONNOxcFk%2FmINH6ToaFTIApBxmfdudy0q1UohZA7FwZNaShO1a%2F%2BM9Yn6Xk6Cg8ideUpleKez5iXasrsfvcrcckRU9TIIcf5g44tcxv3KCCnReVFuKb9LkG8mdzts%2FlPUdiJZlfxSdP55%2F8eVUgDtek%2BelNw%2F9VlVrXNPbucV2EKNEI8pHhURrfv0Ps4frSgrsEe%2BU%2B4CiQnKxzArrzuQ2jp%2FT3MOFQIh%2BVmZJB0C5wHO2ua2Dz6lG5FtbEcXDtueDFAdo5PqvDVbArgIrRFo8n5peMaZuaCgNwNavxK8ZSAI9R5qJNReDE3xHSAeDpCNY8%2BedMy%2FL%2BhTl1lkXbAzT3VTH2lx5wg2WhLk93AKizXlUeMeaz7zi3tSgomfVG6c5jobWaGvi%2Bov8wu4ab%2FAU6vwGs0dOuHrq%2BVPsZ%2B6NNDa5PRNJi5MG33IDYmo2aR9LEAKozhxRg0L4%2FmRsI8EHvTOiTUGx4KHd59MWAW4ILKbdfIOe5oHd4eXkg1lhRftB1SxJvnhEh8q4mOx0XzbkIGA7mWzr7mph2yB1FiOtMe5p5DHI5FZSxVZrbgk3OWEwkaDdO3Z0Sx2wFSIGf95wQgCaUjHiM%2Fkog6D5w6uOBKonjp8YgTt1d0cv5%2FzreN9opzXY8pLJQiIo7gtfp4Bfcdg%3D%3D&Expires=1602668522





    ('0000009',
     {'ib_cf_qty': 50, 'new_ib_bs_stock_cv': 27, 'lastUpdate': 1602338504.869655})



### AllQuery

```
from s3bz.s3bz import Requests
branchURL = Database.allQuery(bucket = INVENTORY_BUCKET_NAME, user=USER, pw=PW)
print(branchURL)
next(iter(Requests.getContentFromUrl(branchURL).items()))
```

    https://inventory-bucket-dev-manual.s3-accelerate.amazonaws.com/allData?AWSAccessKeyId=ASIAVX4Z5TKDVIXEQMRN&Signature=QCt8qlDF%2Fd08ChwFSySX6T%2FKWpU%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEIH%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLXNvdXRoZWFzdC0xIkcwRQIhAKLtSNdLUC1O0Hr5yduzO6d1H6xmshZEvnR26nUJV6vzAiAI25lYEFOu9rUo6hxLc7iPqKPshHE8A2iLbJVE0YLl1SrgAgi7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDM5NDkyMjkyNDY3OSIM99g2ugGfetoq3FQEKrQCoG4IWFWZ%2F8ZjqVONNOxcFk%2FmINH6ToaFTIApBxmfdudy0q1UohZA7FwZNaShO1a%2F%2BM9Yn6Xk6Cg8ideUpleKez5iXasrsfvcrcckRU9TIIcf5g44tcxv3KCCnReVFuKb9LkG8mdzts%2FlPUdiJZlfxSdP55%2F8eVUgDtek%2BelNw%2F9VlVrXNPbucV2EKNEI8pHhURrfv0Ps4frSgrsEe%2BU%2B4CiQnKxzArrzuQ2jp%2FT3MOFQIh%2BVmZJB0C5wHO2ua2Dz6lG5FtbEcXDtueDFAdo5PqvDVbArgIrRFo8n5peMaZuaCgNwNavxK8ZSAI9R5qJNReDE3xHSAeDpCNY8%2BedMy%2FL%2BhTl1lkXbAzT3VTH2lx5wg2WhLk93AKizXlUeMeaz7zi3tSgomfVG6c5jobWaGvi%2Bov8wu4ab%2FAU6vwGs0dOuHrq%2BVPsZ%2B6NNDa5PRNJi5MG33IDYmo2aR9LEAKozhxRg0L4%2FmRsI8EHvTOiTUGx4KHd59MWAW4ILKbdfIOe5oHd4eXkg1lhRftB1SxJvnhEh8q4mOx0XzbkIGA7mWzr7mph2yB1FiOtMe5p5DHI5FZSxVZrbgk3OWEwkaDdO3Z0Sx2wFSIGf95wQgCaUjHiM%2Fkog6D5w6uOBKonjp8YgTt1d0cv5%2FzreN9opzXY8pLJQiIo7gtfp4Bfcdg%3D%3D&Expires=1602668522





    ('0000009',
     {'ib_prcode': '0000009',
      '1000': {'ib_cf_qty': 50,
       'new_ib_bs_stock_cv': 27,
       'lastUpdate': 1602338504.869655},
      'lastUpdate': 1602338504.869655})



```
costPer100ms = 0.0000016667
costPerMs = costPer100ms / 100
timePerCallS = 40
timePerCallMs = timePerCallS * 1000
costPerCall = costPerMs * timePerCallMs
callsPerDay = 60 * 24 /10
costPerDay = callsPerDay * costPerCall
```

```
costPerDay * 33
```




    3.16806336


