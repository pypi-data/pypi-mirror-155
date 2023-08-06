import argparse
import datetime
import sys
import os

sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.utils.inventory.inventory import Data
from zeno_etl_libs.helper.aws.s3 import S3

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                    help="This is env(dev, stage, prod)")
parser.add_argument('-sd', '--start_date', default=None, type=str, required=False, help="Start date in IST")
parser.add_argument('-ed', '--end_date', default=None, type=str, required=False, help="End date in IST")
parser.add_argument('-s', '--csv_store_ids', default=None, type=str, required=False, help="CSV Store ids")

args, unknown = parser.parse_known_args()
env = args.env
start_date = args.start_date
end_date = args.end_date
csv_store_ids = args.csv_store_ids

# start_date = "2022-06-11"
# end_date = "2022-06-12"
# store_id = 240

os.environ['env'] = env
logger = get_logger()

db = DB()
db.open_connection()

s3 = S3(bucket_name=f"{env}-zeno-s3-db")

if not (start_date and end_date) or start_date == "NA" or end_date == "NA":
    """ if no dates given, then run for yesterday """
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    start_date = datetime.datetime.now() + datetime.timedelta(days=-1)
    start_date = start_date.strftime("%Y-%m-%d")

"""
Instructions to use(README):
    0. Make sure tables for both the dates (start and end) are present in public schema (eg: bills-1-mis-2022-06-11)
    1. set the start date and end date
    2. Set the store id if only one store changes are required, if all stores are required then don't set store id
    3. Data is uploaded to s3(prod-zeno-s3-db) inside "inventory/ledger/" folder (eg: s3://dev-zeno-s3-db/inventory/ledger/2022/06/11/240.csv)
    4. S3 Data can be queried using AWS Athena

Tables Required:
    inventory-1,invoice-items-1,invoices-1,customer-return-items-1,customer-returns-1,stock-transfer-items-1,
    stock-transfers-1,bill-items-1,bills-1,return-items-1,returns-to-dc-1,deleted-invoices,deleted-invoices-1,
    inventory-changes-1 

Improvements:
    1. use parquet format to store the data
        import pandas as pd
        df = pd.read_csv('example.csv')
        df.to_parquet('output.parquet')
    2. Filter the data where all the entries/columns are zero, basically no change in the inventory
    3. Try to run the code for multiple stores at a time, not just one
"""

store_filter = f""" where "store-id" in ({csv_store_ids}) """ if csv_store_ids else ""

""" get all the stores """
q = f"""
    select
        distinct "store-id" as "store-id"
    from
        "prod2-generico"."inventory-1" i
    {store_filter}
"""
stores = db.get_df(query=q)

""" this column order will be maintained across all csv files """
column_order = ["id", "barcode", "ptr", "o", "cr", "xin", "xout", "sold", "ret", "ar", "rr", "del", "c", "e"]

for store_id in stores['store-id']:
    logger.info(f"store id: {store_id}")
    data = Data(db=db, store_id=store_id, start_date=start_date, end_date=end_date)
    recon_df = data.concat()

    """ for testing the s3 part """
    # recon_df = pd.DataFrame(data=[[1,2,3,4,5,6,7,8,9,0,1,2,3,4]], columns=column_order)

    logger.info(f"store id: {store_id}")
    uri = s3.save_df_to_s3(df=recon_df[column_order],
                           file_name=f"inventory/ledger/{start_date.replace('-', '/')}/{store_id}.csv")

    logger.info(f"Uploaded successfully @ {uri}")
