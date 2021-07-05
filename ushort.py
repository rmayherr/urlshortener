import os
import sys
import configparser
import hashlib
import base64
import argparse as ap
import ibm_db
from random import sample
from datetime import datetime

def _shortening(_in):
    h = hashlib.new('md5')
    h.update(bytes(_in, 'utf-8'))
    _out = base64.urlsafe_b64encode(bytes(h.hexdigest(), 'utf-8')).decode()
    for i in ['=', '+', '/']:
        _out = _out.replace(i, '')
        _out = ''.join(sample(list(_out), 3) + list(_out))
    return _out[:7]


def connect_to_db():
    #Read db2 parameters from config file and connect to db2.
    #Return a connection object.
    try:
        filename = os.path.join(os.path.dirname(__file__), 'db.ini')
        cfg = configparser.ConfigParser()
        cfg.read(filename)
        con_str = 'DATABASE=' + cfg['DEFAULT']['database'] + \
                  ';HOSTNAME=' + cfg['DEFAULT']['hostname'] + \
                  ';PORT=' + cfg['DEFAULT']['port'] + \
                  ';PROTOCOL=' + cfg['DEFAULT']['protocol'] + \
                 ';UID=' + cfg['DEFAULT']['uid'] + \
                ';PWD=' + cfg['DEFAULT']['pwd'] #+ \
                #';SSLServerCertificate=' + cfg['DEFAULT']['certificate'] + \
                #';SECURITY=SSL'
        con = ibm_db.connect(con_str, '', '')
    except Exception as e:
        print('Error occured!')
        print(f'{e} {ibm_db.conn_errormsg()}')
        sys.exit(1)
    else:
        return con


def _insert_sql(sql, params):
    #Insert data into db2
    try:
        con = connect_to_db()
        stmt = ibm_db.prepare(con, sql)
        o = ibm_db.execute_many(stmt, tuple(params))
        ibm_db.free_stmt(stmt)
        ibm_db.close(con)
    except Exception as e:
        print('Error occured!')
        print(f'{e} {ibm_db.stmt_error()} {ibm_db.stmt_errormsg()}')
        sys.exit(1)


def _query_sql(sql, params):
    #Select query from db2
    out=[]
    try:
        con = connect_to_db()
        stmt = ibm_db.prepare(con, sql)
        ibm_db.execute(stmt, tuple([params]))
        result = ibm_db.fetch_tuple(stmt)
        while result:
            out.append(result)
            result = ibm_db.fetch_tuple(stmt)
        return out
    except Exception as e:
        print(f'{e} {ibm_db.stmt_error()} {ibm_db.stmt_errormsg()}')
        sys.exit(1)


if __name__ == '__main__':
    """
    params = []
    _surl = _shortening("https://mail.notes.na.collabserv.com/data3/126/22298986.nsf/iNotes/Proxy")
    if not _query_sql("select * from ushort.urls where shorturl = ? ", _surl):
        params.append((_surl, 'https://mail.notes.na.collabserv.com/data3/126/22298986.nsf/iNotes/Proxy'))
        _insert_sql("insert into ushort.urls (shorturl, origurl) values(?, ?)", params) 
    """
    parser = ap.ArgumentParser("URL shortener application.")
    parser.add_argument('-u', nargs='+', help='url name that you want to be shortened.')
    args = parser.parse_args()
    _filename = vars(args)
    if _filename['u']:
        #print(f"{_shortening(_out['u'][0])}")
        _arr = list()
        try:
            with open(_filename['u'][0],"r") as f:
                for line in f:
                    for i in range(3):
                        longurl = line.strip()
                        shorturl = _shortening(longurl)
                        if _query_sql("select shorturl from ushort.urls where shorturl = ?", shorturl):
                            break
                    _arr.append((shorturl, longurl, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            _insert_sql("insert into ushort.urls (shorturl, origurl, creation_date) values(?, ?, ?)", _arr)
            os.remove(_filename['u'][0])
        except FileNotFoundError:
            print('File', _filename['u'][0],'not found.') 
    else:
        sys.exit(1)
