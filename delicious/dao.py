import sqlite3

from util import log

class DAO(object):
    
    def __init__(self):
        log.debug(" opening database...")
        self.conn = sqlite3.connect("delicious.cache")
        c = self.conn.cursor()
        try:
            cache_version = c.execute('SELECT VALUE FROM PARAM WHERE KEY = ?', ("cache_version",)).fetchone()[0]
            log.debug("  database found, cache version : %s", cache_version)
        except sqlite3.OperationalError:
            self._create_db()
        finally:
            c.close()
        log.debug(" opening database...Ok")

    def _create_db(self):
        log.debug(" creating new database...")
        c = self.conn.cursor()
        try:
            c.executescript("""
            CREATE TABLE TAG(
                NAME TEXT,
                COUNT INTEGER,
                PRIMARY KEY(NAME)
            );
            
            CREATE TABLE POST(
                URL TEXT,
                TITLE TEXT,
                NOTES TEXT,
                TAG TEXT,
                HASH TEXT,
                META TEXT,
                TIMESTAMP TEXT,
                PRIMARY KEY(URL),
                FOREIGN KEY (TAG) REFERENCES TAG(NAME) ON DELETE CASCADE
            );
        
            CREATE TABLE PARAM(
                KEY,
                VALUE,
                PRIMARY KEY(KEY)
            );
        
            INSERT INTO PARAM(KEY, VALUE)
            VALUES (
                'cache_version',
                '0.1'
            );
            """)
        finally:
            c.close()
        log.debug(" creating new database...Ok")
        
    def get_param(self, param_name):
        log.debug("getting %s...", param_name)
        c = self.conn.cursor()
        try:
            last_sync = c.execute('SELECT VALUE FROM PARAM WHERE KEY = ?', (param_name,)).fetchone()
            if last_sync:
                last_sync = last_sync[0]
        finally:
            c.close()
        log.debug("getting %s...Ok", param_name)
        return last_sync
            
    def update_param(self, param_name, param_value):
        log.debug("updating %s with value %s...", param_name, param_value)
        c = self.conn.cursor()
        try:
            c.execute('INSERT OR REPLACE INTO PARAM(KEY, VALUE) VALUES(?, ?)', (param_name, param_value))
            self.conn.commit()
        finally:
            c.close() 
        log.debug("updating %s...Ok", param_name)
        
    def update_last_sync(self, last_sync):
        self.update_param("last_sync", last_sync)

    def get_last_sync(self):
        return self.get_param("last_sync")

    def update_last_update(self, last_update):
        self.update_param("last_update", last_update)

    def get_last_update(self):
        return self.get_param("last_update")          
        
    def update_tags(self, tags):
        log.debug("updating tags... : %s", tags)
        c = self.conn.cursor()
        try:
            c.executemany('INSERT OR REPLACE INTO TAG(NAME, COUNT) VALUES(:tag, :count)', tags)
            self.conn.commit()
        finally:
            c.close() 
        log.debug("updating tags...Ok")
        
    def update_posts(self, posts):       
        log.debug("updating posts... : %s", posts)
        c = self.conn.cursor()
        try:
            c.executemany("""INSERT OR REPLACE INTO POST(URL, 
                                                         TITLE, 
                                                         NOTES,
                                                         TAG,
                                                         HASH,
                                                         META,
                                                         TIMESTAMP) 
                                                VALUES(:href,
                                                       :description,
                                                       :extended,
                                                       :tag,
                                                       :hash,
                                                       :meta,
                                                       :time)""", posts)
            self.conn.commit()
        finally:
            c.close() 
        log.debug("updating posts...Ok")
