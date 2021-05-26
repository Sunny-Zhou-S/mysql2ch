import mysql2ch

mysql_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'example',
    'database': 'imdb',
    'table': 'title_akas'
}

ch_config = {
    'host': '127.0.0.1',
    'database': 'imdb',
    'user': 'default',
    'table': 'title_akas'
}

field_mapping = {
    'title_id': 'titleID',
    'ordering': 'ordering',
    'title': 'title',
    'region': 'region',
    'language': 'language',
    'types': 'types',
    'attributes': 'attributes',
    'is_original_title': 'isOriginalTitle'
}

mysql2ch.mysql2ch(mysql_config, ch_config, field_mapping, 5)
print('import success!')
