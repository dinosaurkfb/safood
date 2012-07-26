#coding=utf-8
from tornado.options import define, options

define('db_master_url', default = 'mysql://root:123456@127.0.0.1:3306/safood?charset=utf8', help = 'database master config')
define('db_slave_url', default = 'mysql://root:123456@127.0.0.1:3306/safood?charset=utf8', help = 'database slave config')

def get_db_config(): 
    return {
        'master': {
            'url': options.db_master_url,
            'echo': False,
            'connect_args' : {'unix_socket': '/tmp/mysql.sock'}
            },
        'slave': {
            'url': options.db_slave_url,
            'echo': False,
            'connect_args' : {'unix_socket': '/tmp/mysql.sock'}
            },
    }
