from sqlalchemy import create_engine, event
from sqlalchemy.engine.url import URL
from msal import ConfidentialClientApplication
import urllib
import struct
import subprocess
import pandas as pd
import logging

LOGGER = logging.getLogger(__name__)


def get_mysql_helper(host, user, port, database, password=None):
    engine_url = URL.create(
        drivername="mysql+pymysql", host=host, username=user, database=database, password=password, port=port
    )
    engine = create_engine(engine_url, connect_args={"ssl": {"ssl_check_hostname": False}}, pool_pre_ping=True)
    if not password:

        @event.listens_for(engine, "do_connect")  # https://docs.sqlalchemy.org/en/14/core/engines.html
        def provide_token(dialect, conn_rec, cargs, cparams):
            cmd = "az account get-access-token --resource-type oss-rdbms --output tsv --query accessToken"
            token = subprocess.run(cmd.split(" "), stdout=subprocess.PIPE).stdout.decode("utf-8")
            cparams["password"] = token

    return SQL_Helper(engine)


def get_sqlserver_helper(host, database, service_principal_id, service_principal_secret, tenant_id, 
                         port=1433, db_driver="ODBC Driver 17 for SQL Server", fast_execute_many=False, **kwargs):

    creds = ConfidentialClientApplication(
        client_id=service_principal_id,
        client_credential=service_principal_secret,
        authority=f"https://login.microsoftonline.com/{tenant_id}",
    )

    conn_str = urllib.parse.quote_plus(f"DRIVER={{{db_driver}}};SERVER={host},{port};DATABASE={database}")

    connect_args = {'ansi': False, 'TrustServerCertificate': 'yes', **kwargs}
    engine = create_engine( 
        url=URL.create("mssql+pyodbc", query={"odbc_connect": conn_str}), 
        connect_args=connect_args,
        fast_executemany=fast_execute_many, pool_pre_ping=True
    )

    @event.listens_for(engine, "do_connect")
    def provide_token(dialect, conn_rec, cargs, cparams):
        SQL_COPT_SS_ACCESS_TOKEN = 1256
        token = creds.acquire_token_for_client(scopes="https://database.windows.net//.default")
        token_bytes = token["access_token"].encode("utf-16-le")
        token_struct = struct.pack(f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)
        cparams["attrs_before"] = {SQL_COPT_SS_ACCESS_TOKEN: token_struct}

    return SQL_Helper(engine)


class SQL_Helper:
    def __init__(self, engine):
        """
        SQL helper constructor.

        Parameters:
            engine: sqlalchemy.engine.base.Engine instance
        """
        self._engine = engine

    def from_table(self, table, **kwargs):
        """
        Given a table name, returns a Pandas DataFrame.

        Parameters:
            table (string): table name
            **kwargs: additional keyword parameters passed to pd.read_sql_table

        Returns:
            result (pd.DataFrame): SQL table in pandas dataframe format
        """
        return pd.read_sql_table(table, self._engine, **kwargs)

    def from_file(self, filename, query_args={}, limit=None, **kwargs):
        """
        Read SQL query from .sql file into a Pandas DataFrame.

        Parameters:
            filename (string): path to file containing the SQL query
            query_args (dict): query string is formatted with those params: string.format(**query_args)
                               example: {'max_date': '2020-01-01'}
            limit (int): maximum number of results
            **kwargs: additional keyword parameters passed to pd.read_sql_query

        Returns:
            result (pd.DataFrame): query results in  Pandas DataFrame format
        """
        if (limit is not None) and (not isinstance(limit, int)):
            raise ValueError("Limit must be of type int")

        with open(filename, "r") as f:
            query_unformated = f.read().rstrip()
        query = query_unformated.format(**query_args)
        query = query if not limit else query.replace(";", f" LIMIT {limit};")
        return self.from_query(query, **kwargs)

    def from_query(self, query, **kwargs):
        """
        Read SQL query into a Pandas DataFrame.

        Parameters:
            query (string): query string
            **kwargs: additional keyword parameters passed to pd.read_sql_query

        Returns:
            result (pd.DataFrame): query results in  Pandas DataFrame format
        """
        return pd.read_sql_query(query, self._engine, **kwargs)

    def write_df(self, df, table_name, **kwargs):
        """
        Store Pandas Dataframe into SQL table

        Args:
            df (pd.DataFrame): data to write
            **kwargs: additional keyword parameters passed to df.to_sql
        """
        with self._engine.connect() as conn:
            trans = conn.begin()
            try:
                df.to_sql(table_name, conn, **kwargs)
                trans.commit()
            except Exception as ex:
                LOGGER.warning(str(ex))
                trans.rollback()
                raise ex
