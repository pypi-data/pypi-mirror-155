import sys
import os
import pyodbc
import ipaddress


# Class building connection strings to the model database
class RiskSpecStrConnector:
    _server_name: str
    _uid: str
    _pwd: str
    _ip: str
    _port: int
    _driver: str

    # Setting parameters for connecting to the SQL server
    def ConnectToServer(self,
                        server_name='.\RISKSPEC_PSA2012',
                        uid='sa',
                        pwd='82sbDiF%5_2&33d%hvTP!4',
                        ip='127.0.0.1',
                        port=1433) -> bool:

        if len(server_name) < 0:
            return False
        if port < 0 or port > 65535:
            return False

        self._server_name = server_name
        self._uid = uid
        self._pwd = pwd

        try:
            self._ip = ipaddress.ip_address(ip)
        except ValueError:
            return False

        self._port = port

    def AttachModelFromFile(self, file_path: str) -> str:
        dbname = os.path.basename(file_path).split('.')[0]
        params = self.GetConnectString(model_name='master')
        try:
            with pyodbc.connect(params) as cnxn:
                cnxn.autocommit = True
                with cnxn.cursor() as cursor:
                    cursor.execute(
                        f'''
                            USE [master];
                            EXEC sp_attach_db
                            @dbname={dbname},
                            @filename1 = '{file_path}';
                            ''')
        except pyodbc.Error as ex:
            print(f'pyodbc error: {ex.args[0]}', file=sys.stderr)
        return self.GetConnectString(dbname)

    def DetachModel(self, model_name: str):
        params = self.GetConnectString('master')
        try:
            with pyodbc.connect(params) as cnxn:
                cnxn.autocommit = True
                with cnxn.cursor() as cursor:
                    cursor.execute(
                        f'''
                                USE [master];
                                ALTER DATABASE [{model_name}] SET TRUSTWORTHY ON;
                                EXEC sp_detach_db @dbname={model_name};
                                ''')
        except pyodbc.Error as ex:
            print(f'pyodbc error: {ex.args[0]}', file=sys.stderr)

    # Detach all models connected to the SQL server
    def DetachAll(self):
        params = self.GetConnectString('master')
        for model_name in self.GetAvailableModels():
            try:
                with pyodbc.connect(params) as cnxn:
                    cnxn.autocommit = True
                    with cnxn.cursor() as cursor:
                        cursor.execute(
                            f'''
                                USE [master];
                                ALTER DATABASE [{model_name}] SET TRUSTWORTHY ON;
                                EXEC sp_detach_db @dbname={model_name};
                                ''')
            except pyodbc.Error as ex:
                print(f'pyodbc error: {ex.args[0]}', file=sys.stderr)

    # Get a list of all active models on the SQL server
    def GetAvailableModels(self) -> list:
        params = self.GetConnectString('master')
        try:
            with pyodbc.connect(params) as cnxn:
                with cnxn.cursor() as cursor:
                    cursor.execute(
                        '''
                        SELECT * FROM master.dbo.sysdatabases
                        WHERE name NOT IN ('master', 'tempdb', 'model', 'msdb')
                        ''')
                    rows = cursor.fetchall()
                    if len(rows) > 0:
                        return [r[0] for r in rows]
        except pyodbc.Error as ex:
            print(f'pyodbc error: {ex.args[0]}', file=sys.stderr)

    # Get model connection string
    def GetConnectString(self, model_name: str) -> str:
        if sys.platform == 'linux':
            # Удалённое подключение для Linux через FreeTDS и unixODBC
            return f'driver={{FreeTDS}};server={self._ip};port={self._port};database={model_name};uid={self._uid};pwd={self._pwd};'

        elif sys.platform == 'win32':
            # Локальное подключение для Windows со стандартным драйвером
            return f'DRIVER={{SQL Server}};SERVER={self._server_name};DATABASE={model_name};Uid={self._uid};Pwd={self._pwd};'
        else:
            raise Exception('OS not supported')


    # Get model connection string for console call
    def GetCMDConnectString(self, model_name: str) -> str:
        if sys.platform == 'linux':
            return f'mssql+pyodbc://{self._uid}:{self._pwd}@{self._ip}\{model_name}?driver=FreeTDS'
        elif sys.platform == 'win32':
            return f'mssql+pyodbc://{self._uid}:{self._pwd}@{self._server_name}/{model_name}?driver=SQL+Server+Native+Client+11.0'
        else:
            raise Exception('OS not supported')


def test():
    constr = RiskSpecStrConnector()
    constr.ConnectToServer(pwd='AsdfAsdf132009828')
    print(constr.GetConnectString('master'))
    try:
        with pyodbc.connect(constr.GetConnectString('master')) as cnxn:
            with cnxn.cursor() as cursor:
                rows = cursor.execute('SELECT @@version;')
                for row in rows:
                    print(row)
    except pyodbc.Error as ex:
        print(f'pyodbc error: {ex.args[0]}', file=sys.stderr)

    import sqlalchemy

    print(constr.GetCMDConnectString('master'))
    with sqlalchemy.create_engine(constr.GetCMDConnectString('master')) as engine:
        with engine.connect() as connection:
            rows = connection.execute("select @@version")
            for row in rows:
                print(row)


if __name__ == "__main__":
    test()
