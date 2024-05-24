import psycopg2
import time

DB_HOST_ADDR = 'localhost'
DB_HOST_PORT = 5432

class EdgeDatabase:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._conn = psycopg2.connect(database="iot",
                                      host=host,
                                      port=port,
                                      user='postgres',
                                      password='iot')
    def _convertUid(self, uid):
        return ':'.join('{:02x}'.format(b) for b in uid)

    def _splitUid(self, uid):
        chunks = [uid[i:i+2] for i in range(0, len(uid), 2)]
        return ':'.join(chunks)

    def log(self, uid, device): #uid as bytes
        uidString = self._splitUid(uid)
        cur = self._conn.cursor()
        cur.execute("INSERT INTO access_log VALUES (%s, %s, %s)", (uidString, time.time()*1000, device))
        self._conn.commit()
        cur.close()

    def getLogs(self, amount=10):
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM access_log ORDER BY time DESC;")
        res = cur.fetchmany(amount)
        cur.close()
        return res

def test():
    testdb = EdgeDatabase(DB_HOST_ADDR, DB_HOST_PORT)
    testuid = "aabbcc"
    testdb.log(testuid, 60)
    print(testdb.getLogs(amount=1))

if __name__ == "__main__":
    print("Running DB Tests....")
    test()

