import os
import uuid
import datetime
from dotenv import load_dotenv
import json

from google.cloud import bigquery
def call_bigquery(sector):
    # Currently for simplicity, keeping 1 record for each sector for prototype
    # In future we can have multiple records for each sector and take average or weighted average based
    client = bigquery.Client(project='igneous-fold-258210')
    table_ref = "igneous-fold-258210.aianalyst.Benchmark"

    # # To get exact column names from bigquery. Make it easy for debugging
    # query = f"SELECT * FROM `{table_ref}` LIMIT 1"
    # df = client.query(query).to_dataframe()
    # print(df.columns.tolist())
    # columns = ['Startup', '  Sector', 'Team_Quality', '  Market_Size', 'Traction', 'Financials', 'Product_Uniqueness', 'Competitive_Landscape', 'Business_Model_Clarity', 'Risk_Factors']
    
    # query = """SELECT COUNT(*) FROM `igneous-fold-258210.aianalyst.Benchmark` """
    # query = f""" SELECT * FROM `igneous-fold-258210.aianalyst.Benchmark` WHERE Sector = `Finance`"""
    # query = f""" SELECT * FROM `igneous-fold-258210.aianalyst.Benchmark`"""
    query = f""" SELECT * FROM `{table_ref}` WHERE `  Sector` = '{sector}'"""
    # print(query)
    

    query_job = client.query(query)  # API request
    benchmark_df = query_job.to_dataframe()
    return benchmark_df

# # test it with this code
# sector = "Finance"
# benchmark_df = call_bigquery(sector)
# print(benchmark_df)