import pymysql.cursors
from clickhouse_driver import Client


def mysql2ch(mysql_config, ch_config, field_mapping, batch_size):
    '''
    dump mysql data into clickhouse
    mysql_config:
        host: mysql host
        user: mysql user
        password: mysql password
        database: mysql db
        table: convert from table
    ch_config:
        host: ch host
        database: ch db
        user: user
        password: password of user
        table: convert to table
    field_mapping:
        mysql_filed -> ch_field
    batch_size: import batch size
    '''
    if mysql_config.get('table', '') == '' or ch_config.get('table', '') == '':
        raise ValueError('Please provide clickhouse table and mysql table')

    if batch_size <= 0:
        raise ValueError('Please provide available batch size')

    # connect to mysql
    connection = pymysql.connect(host=mysql_config.get('host', '127.0.0.1'),
                                 user=mysql_config.get('user', 'root'),
                                 password=mysql_config.get('password', ''),
                                 database=mysql_config.get('database', ''),
                                 cursorclass=pymysql.cursors.DictCursor)

    # connect to clickhouse
    client = Client(host=ch_config.get('host', '127.0.0.1'),
                    database=ch_config.get('database'),
                    user=ch_config.get('user', 'default'),
                    password=ch_config.get('password', ''))

    has_more = True
    offset = 0
    while has_more:
        with connection.cursor() as cursor:
            table = mysql_config.get('table')
            # read a single line
            sql = "SELECT * FROM {} LIMIT {} OFFSET {}".format(
                table, batch_size, offset)
            cursor.execute(sql, ())
            result = cursor.fetchall()
            offset += batch_size

            # no more data
            if len(result) != batch_size:
                has_more = False

            # batch insert
            insert_datas = []
            for r in result:
                data = {}
                for mysql_field, ch_field in field_mapping.items():
                    # check if mysql field in mysql table
                    if mysql_field not in r:
                        raise ValueError(
                            'mysql field {} not in mysql table'.format(mysql_field))

                    data[ch_field] = r[mysql_field]
                insert_datas.append(data)

            # insert into clickhouse
            sql = 'INSERT INTO {}({}) VALUES'.format(
                ch_config.get('table'), ','.join(field_mapping.values()))
            client.execute(sql, insert_datas)
