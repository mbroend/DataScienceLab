# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 10:19:25 2020
Module for simplifying basic SQL operations from python
@author: Mathias Brønd Sørensen
"""
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.sql import text as sa_text
from sqlalchemy.orm import Session, sessionmaker
import pandas as pd
import time
import urllib
import math
import os


class Connection:
    """
    Connection class for easy interfacing with SQL Server.
    Instanciate an object with the server and database 
    """
    def __init__(self, server, database, driver = "ODBC Driver 13 for SQL Server", systemuser=False):
        self.driver = driver
        self.server = server
        self.database = database
        if systemuser:
            # Get username and password from environment
            uid = os.environ.get('MSSQL_USERNAME')
            pwd = os.environ.get('MSSQL_PASSWORD')
            # Server must match DNS configuration for the system running the script
            DSN = self.server
            params = urllib.parse.quote("DSN={0};DATABASE={1};UID={2};PWD={3}".format(DSN, self.database, uid, pwd))
            self.engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params, poolclass= NullPool)
        else:
            params = urllib.parse.quote("DRIVER={0};SERVER={1};DATABASE={2};Trusted_Connection=yes".format(self.driver, self.server, self.database))
            self.engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params, poolclass= NullPool, fast_executemany=True)
    
    def insert(self,schema,table_name,dataframe):
        """
        Function for inserting (appending) data from dataframe into table on SQL server.
        
        INPUT:
            schema: The database schema \n
            table_name: The desired table name \n
            dataframe: The data used for dertermining datatypes and column names \n
        OUTPUT:
            None
        """
        tst = time.time()
        
        try:
            print('inserting rows pre')
            dataframe.to_sql(name = table_name, con = self.engine, schema = schema,
                             if_exists='append',index=False)#, method = 'multi')
            tdif = time.time()-tst
            print('--- Inserting rows:')
            print('--- On {0}: {1} rows inserted into {2}.{3}.{4} in {5} seconds'.format(self.server,dataframe.shape[0],self.database,schema,table_name,round(tdif,2)))
        except Exception as e:
            print('--- On {0}: Could not insert rows into {1}.{2}.{3}'.format(self.server,self.database,schema,table_name))
            print(e)
        return
    
    def replace(self,schema,table_name,dataframe):
        """
        Function for inserting (replacing) table on SQL server from a dataframe.
        Use with caution as existing data and datatype definitions will be replaced with whatever is present in dataframe.
        
        INPUT:
            schema: The database schema \n
            table_name: The desired table name \n
            dataframe: The data used for dertermining datatypes and column names \n
        OUTPUT:
            None
        """
        tst = time.time()
        try:
            dataframe.to_sql(table_name, self.engine, 
                             schema=schema, if_exists='replace',
                             index=False)#, method='multi')
            tdif = time.time()-tst
            print('--- Replacing table:')
            print('--- On {0}: {1} rows inserted into {2}.{3}.{4} in {5} seconds'.format(self.server,dataframe.shape[0],self.database,schema,table_name,round(tdif,2)))
        except Exception as e:
            print('--- On {0}: Could not replace table {1}.{2}.{3}'.format(self.server,self.database,schema,table_name))
            print(e)
    
    def read_table(self,schema,table_name):
        """
        Function for reading a table on SQL server into a dataframe.
        The function is case sensitive.
        
        INPUT:
            schema: The database schema \n
            table_name: The table name \n
        OUTPUT:
            dataframe: Pandas dataframe containing data from the table
        """
        tst = time.time()
        try:
            df = pd.read_sql_table(table_name = table_name, con = self.engine, 
                                   schema = schema)
            tdif = time.time()-tst
            print('--- On {0}: {1} rows read from {2}.{3} into dataframe in {4} seconds'.format(self.server,df.shape[0],schema,table_name,round(tdif,2)))
            return df
        except Exception as e:
            print('failed to read query')
            print(e)
        
    
    def read_sql(self,query):
        """
        Function for reading a resulting table from query on SQL server into a dataframe.
                
        INPUT:
            schema: The database schema \n
            table_name: The table name \n
        OUTPUT:
            dataframe: Pandas dataframe containing data from the table
        """
        tst = time.time()
        try:
            df = pd.read_sql(sql = query, con = self.engine)
            tdif = time.time()-tst
            print('--- On {0}: {1} rows read from query into dataframe in {2} seconds'.format(self.server,df.shape[0],round(tdif,2)))
            print('--- Query: '+ query)
            return df
        except Exception as e:
            print('failed to read query')
            print(e)
       
    def create(self,schema,table_name,dataframe,primary_key = []):
        """
        Function for creating table on SQL server from a dataframe. 
        Datatypes are adjusted to best practice in SQL SERVER.
        Strings are converted to NVARCHAR() with the max length rounded up to nearest 10.
        Requires column names of dataframe to be unique.
        
        INPUT:
            schema: The database schema \n
            table_name: The desired table name \n
            dataframe: The data used for dertermining datatypes and column names \n
            primary_key (OPTIONAL): If you wish the create statement to a include primary key provide it as a list
        OUTPUT:
            None
        """
        # Check if dataframe has 
        assert(len(tuple(dataframe.columns)) == len(set(dataframe.columns))), 'Dataframe contains duplicate column names.'
        
        datatypes = dataframe.dtypes
        sql = 'CREATE TABLE [' + schema + '].[' + table_name + '] ('
        for col,typ in datatypes.iteritems():
            
            if (typ == 'object'):
                
                if dataframe[col].dropna().map(len).shape[0] > 0:
                    # Round up to nearest 10
                    length = int(math.ceil(dataframe[col].dropna().map(len).max()/10.0))*10 
                    sql = sql + '\r\n [' + col + '] [NVARCHAR](' + str(length) + ') COLLATE Danish_Norwegian_CI_AS'
                else:
                    print('WARNING: {} contains 0 rows and length could not be determined'.format(col))
                    sql = sql + '\r\n [' + col + '] [NVARCHAR](???) COLLATE Danish_Norwegian_CI_AS'
            elif (typ == 'int64' or typ == 'int32'):
                if dataframe[col].max() > 2000000000: # max allowed in INT is 2,147,483,647, rounded down for buffer
                    sql = sql + '\r\n [' + col + '] [BIGINT]'
                else:
                    sql = sql + '\r\n [' + col + '] [INT]'
            elif (typ == 'float64' or 'float32'):
                sql = sql + '\r\n [' + col + '] [FLOAT]'
            elif typ == 'bool':
                sql = sql + '\r\n [' + col + '] [BIT]'
            else:
                print('Unknown datatype for column {}'.format(col))
            if col in primary_key:
                sql = sql + ' NOT NULL,'
            else:
                sql = sql + ' NULL,'
        
        sql = sql[:-1] # remove trailing comma                
        
        if len(primary_key) > 0:
            sql = sql + '\r\n CONSTRAINT [PK_' + schema + '_' + table_name + '] PRIMARY KEY CLUSTERED'
            sql = sql + '\r\n ('
            for i in primary_key:
                sql = sql + '[' + i + '] ASC,'
            sql = sql[:-1] + ') WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, DATA_COMPRESSION = ROW)'
        if schema == 'ext':
            sql = sql + '\r\n ) ON [Staging]'
        else:
            sql = sql + '\r\n ) ON [Standard]'
        print(sql)
    
    def truncate(self,schema,table_name, exec_sql):
        """
        Function for truncating table on SQL server. 
        
        INPUT:
            schema: The database schema \n
            table_name: The table name \n
            exec_sql : Toggle for printing/executing statement (1 = print, 0 = execute) \n
        OUTPUT:
            None
        """
        sql = "TRUNCATE TABLE {}.{}".format(schema,table_name)
        if exec_sql == 1:
            print(sql)
        elif exec_sql == 0:
            try:
                conn = self.engine.connect()
                conn.execute(sa_text(sql).execution_options(autocommit=True))
                conn.close()
                print('{}.{} was truncated'.format(schema,table_name))
            except Exception as e:
                print('Failed to truncate table')
                print(e)
    
    def execute_storedprocedure(self,schema,proc_name,params):
        '''
        Execute a storedprocedure
        '''
        sql_params = ''
        for name, value in params.items():
            if (isinstance(value, str) and value[:2]!='0x'):
                sql_param = "@{0}='{1}'".format(name, value)
            else:
                sql_param = "@{0}={1}".format(name, value)
            sql_params = sql_params + sql_param + ','
        sql_params = sql_params[:-1]
        #sql_params = ",".join(["@{0}={1}".format(name, value) for name, value in params.items()])
        sql_string = """
            DECLARE @return_value int;
            EXEC    @return_value = [{schema}].[{proc_name}] {params};
            SELECT 'Return Value' = @return_value;
        """.format(schema=schema, proc_name=proc_name, params=sql_params)
        Session = sessionmaker(bind=self.engine)
        session = Session()
        results = session.execute(sql_string).fetchall()        
        session.commit()
        session.close()
        return results
