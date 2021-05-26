import csv
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='example',
                             database='imdb',
                             cursorclass=pymysql.cursors.DictCursor)

# A ‘\N’ is used to denote that a particular field is missing or null for that title/name
emptyIdentifier = '\\N'

with open("title.akas.tsv") as f:
    rd = csv.reader(f, delimiter="\t", quotechar='"')
    idx = 0
    for row in rd:
        # ignore header
        if idx == 0:
            idx += 1
            continue
        idx += 1
        title_id = row[0]
        ordering = row[1]
        title = row[2]
        region = row[3]

        # handle missing data
        if region == emptyIdentifier:
            region = None
        language = row[4]
        if language == emptyIdentifier:
            language = None
        types = row[5]
        if types == emptyIdentifier:
            types = None
        attributes = row[6]
        if attributes == emptyIdentifier:
            attributes = None
        is_original_title = row[7]

        with connection.cursor() as cursor:
            # add a new line
            sql = "INSERT INTO title_akas (title_id, ordering, title, region, language, types, attributes, is_original_title) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (title_id, ordering, title, region,
                                 language, types, attributes, is_original_title))
            connection.commit()
