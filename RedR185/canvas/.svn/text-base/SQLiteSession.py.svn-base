## SQLiteSession.  Implimentation of sqlite functions for Red-R.  
import redREnviron, sqlite3, os, time, cPickle
import redRi18n
# def _(a):
    # return a
_ = redRi18n.Coreget_()
class SQLiteHandler:
    def __init__(self, defaultDB = None):
        if defaultDB:
            self.dataBase = defaultDB
        else:
            self.dataBase = 'local|temp.db'
            
    def getDatabase(self, dataBase = None):
        if not dataBase:
            dataBase = self.dataBase
        if 'local|' in dataBase:  # convert the database if the local name is present.
            database = os.path.join(redREnviron.directoryNames['tempDir'], dataBase.split('|')[1])
        else:
            database = dataBase
        return database
        
    def execute(self, query, parameters = None, database = None):
        conn = sqlite3.connect(self.getDatabase(database))
        cursor = conn.cursor()
        response = []
        try:
            if parameters:
                cursor.execute(query, parameters)
            else:
                cursor.execute(query)
            for row in cursor:
                response.append(row)
        except Exception as inst:
            import redRLog
            redRLog.logException(inst)
            #pass
        finally:
            #import redRLog
            #redRLog.logException(query)
            conn.commit()
            conn.close()
            return response
    def getColumnNames(self, table, database = None):
        if not database:
            database = self.dataBase
        response = self.execute('PRAGMA table_info('+table+')', database = database)
        
        colnames = []
        for row in response:
            colnames.append(unicode(row[1]))
            
        return colnames
        
    def setTable(self, table, colNames, database = None, force = False):
        if not database:
            database = self.dataBase
        if force:
            self.execute('DROP TABLE IF EXISTS '+table, database = database)
        try:
            self.execute("CREATE TABLE "+table+" "+colNames, database = database)
        except Exception as inst:
            redRLog.log(redRLog.REDRCORE, redRLog.ERROR, inst)
    def getTableNames(self, database = None):
        
        response = self.execute('SELECT * FROM SQLITE_MASTER WHERE type="table" OR type ="view"', database = database)
        info = []
        for row in response:  # collect the info for all of the tables and the views.
            info.append(unicode(row[1])+', '+ unicode(row[0]))
            #print row
        return info
        
    def newTableName(self):
        return 'AutoTable_'+unicode(time.time()).replace('.', '_')
    def newIDName(self):
        return 'AutoID_'+unicode(time.time()).replace('.', '_')
    def dictToTable(self, dictionary, tableName = None, database = None):
        if not database:
            database = self.dataBase
        if not tableName:
            tableName = self.newTableName()
        self.setTable(tableName, '("Name" text, "Data" text)', database = database, force = True)
        for name in dictionary.keys():
            self.execute("insert into "+tableName+" values (?,?)", parameters = (cPickle.dumps(name), cPickle.dumps(dictionary[name])), database = database)
        return tableName
        
    def tableToDict(self, tableName, dataBase = None):
        if not dataBase:
            dataBase = self.dataBase
        response = self.execute('select * from '+tableName, database = dataBase)
        newDict = {}
        for row in response:
            newDict[cPickle.loads(unicode(row[0]))] = cPickle.loads(unicode(row[1]))
            
        return newDict
        
    def saveObject(self, object):
        tableName = 'SavedObjects'
        dataBase = 'local|SavedObjects.db'
        self.setTable(tableName, '("ID" key, "Data" text)', database = dataBase)
        newID = self.newIDName()
        self.execute('insert into SavedObjects values (?,?)', parameters = (newID, cPickle.dumps(object)), database = dataBase)
        return newID
        
    def setObject(self, oldID):
        #print oldID
        tableName = 'SavedObjects'
        dataBase = 'local|SavedObjects.db'
        response = self.execute('select * from SavedObjects where ID = ?', parameters = (oldID,), database = dataBase)
        self.execute('DELETE FROM '+tableName+' WHERE ID = ?', parameters = (oldID, ), database = dataBase) ## delete the ref
        #print unicode(response) 
        return cPickle.loads(unicode(response[0][1]))