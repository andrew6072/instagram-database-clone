import random
import string
import numpy as np
import psycopg2 as ps

AMOUNT_USERS = 2


def fill_users():
    LOGIN = ['cat___', 'fox___', 'owl___', 'bear__', 'parrot', 'pen___', 'puma__', 'tiger_', 'lion__',
             'ostrich', 'sheep_', 'dog___', 'cow___', 'shrek_', 'shadow_fiend']
    EMAIL = ['@gmail.com', '@yandex.ru', '@mail.ru', '@mephi.ru', '@rambler.ru']
    CITY = ['moscow', 'spb']
    DISTRICT = ['leninsky', 'zheleznodorozhny', 'pervomaysky', 'central', 'kekus']
    METRO = ['china-town', 'park of culture', 'kolomenskoe', '1905 year street', 'teatralnaya',
             'sokol', 'kuznetskiy most', 'trubnaya', 'barrikadnaya', 'petrovskiy park']
    TYPE = ['single', 'company']
    letters = string.ascii_lowercase
    nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    query = 'INSERT INTO users(login, password, email, profile_photo, contact_phone,contact_information, balance, ' \
            'user_type) VALUES '
    for i in range(AMOUNT_USERS):
        l = random.choice(LOGIN) + str(i)
        p = ''.join(random.choice(letters) for _ in range(random.randint(10, 80)))
        e = l + random.choice(EMAIL)
        ph = '~/users/' + l
        n = '7' + ''.join(str(random.choice(nums)) for _ in range(9))
        c = random.choice(CITY)
        d = random.choice(DISTRICT)
        contact_inf = {'city': c, 'district': d}

        if c == 'moscow' or c == 'spb':
            contact_inf['metro'] = random.choice(METRO)

        cti = str(contact_inf).replace('\'', '\"')
        b = 0

        if random.randint(0, 100) < 25:
            b = random.randint(1, 10041)

        t = 'single'

        if random.randint(0, 100) > 80:
            t = 'company'

        query += f'(\'{l}\', \'{p}\', \'{e}\', \'{ph}\', \'{n}\', \'{cti}\', {b}, \'{t}\'), '

    query = query[:-2]
    query += ';'
    return query


def generate_timestamp():
    MONTHS = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    month = random.choice(MONTHS)
    if month == 'FEB':
        date = random.randint(1, 28)
    else:
        date = random.randint(1, 30)
    year = random.randint(2015, 2021)
    raw_hour = random.randint(0, 23)
    hour = ''
    if raw_hour < 10:
        hour = hour + '0'
        hour = hour + str(raw_hour)
    else:
        hour = str(raw_hour)

    raw_minute = random.randint(0, 59)
    minute = ''
    if raw_minute < 10:
        minute = minute + '0'
        minute = minute + str(raw_minute)
    else:
        minute = str(raw_minute)

    time_stamp = f'\'{date}-{month}-{year} {hour}:{minute}\''
    return time_stamp


def fill_Post():
    INT = ['Hello! ', 'HEllo. ', 'hello ', 'HeLlO ', 'Hi ', 'HI! ', 'hI. ', 'Here is my ', 'What a nice day ',
           'How are you guys? ', 'Good morning, ', 'Let me introduce to you ', 'Have a nice day ', 'Nice to meet you! ',
           'Say hi to my ', 'This is ', 'I have a ', 'Good night, ']
    CONT = ['my cat! ', 'my new puppy! ', 'the picture of nature! ', 'something ', 'my girl friend ', 'our group. ',
            'Happy classmates ', 'nice weather ', 'feeling sleepy ', 'a book ', 'my lover ', 'my dream ', 'a bike ',
            'a car ',
            'new book ', 'new ps5 ', 'my friend ', 'oh dear ', 'Santa Clause ', 'oops ']
    EMOJI = ['=(', '=)', ':3', ';)', '.-.', '-_-', '+_+', '=_=', ':P', 'KEK', ':/', 'o_0', 'UwU', '*v*']

    query = 'INSERT INTO Post(caption, user_id, post_type_id, posted_at) VALUES '

    for i in range(1200):
        caption = random.choice(INT) + random.choice(CONT)
        if random.randint(0, 1) == 1:
            caption += random.choice(EMOJI)
        posted_at = generate_timestamp()
        user_id = random.randint(1, 600)
        post_type_id = random.randint(1, 3)
        query += f'(\'{caption}\', {user_id}, {post_type_id}, TO_TIMESTAMP({posted_at}, \'DD MON YYYY HH24:MI\')), '
    query = query[:-2]
    query += ';'
    return query


def fill_Reaction():
    query = 'INSERT INTO Reaction(reacted_at, user_id, post_id) VALUES '
    for user_id in range(1, 601):
        reacted_at = generate_timestamp()
        for post_id in range(36229, 37429):
            if random.randint(0, 100) > 66:
                query += f'(TO_TIMESTAMP({reacted_at}, \'DD MON YYYY HH24:MI\'), {user_id}, {post_id}), '
    query = query[:-2]
    query += ';'
    return query


def fill_Post_media():
    DISK = ['C:/', 'D:/', 'E:/', 'F:/', 'http://www.var.com/', 'http://www.google_picture.com/', 'http://www.wiki.com/',
            'http://www.example.ru/', 'http://www.facebook.com/', 'http://www.instagram.com/',
            'http://www.nothing.com/',
            'http://www.pages.com/', 'http://www.example.com/', 'User/']
    FOLDER = ['Pictures/', 'Forum/', 'Home/', 'Desktop/', 'something/', 'another/', 'apilibrary/', 'TravelBrochure',
              'Newsletters/', 'January/', 'February/', 'utilities/', 'folder1/']
    FILE_NAME = ['MorbiNon', 'NuncProin', 'Est', 'AliquetUltricesErat', 'Dapibus', 'FeugiatNon', 'Elementum',
                 'OrciLuctusEt', 'CongueRisus'
                                 'AnteIpsumPrimis', 'RutrumAt', 'ProinLeoOdio', 'Felis', 'Adipiscing', 'TurpisInteger',
                 'EuOrci', 'VivamusTortor', 'TempusVelPede']
    FILE_FORMAT = ['.jpeg', '.jpg', '.png', '.gif', '.tiff', '.psd', '.pdf', '.eps', '.ai', '.indd', '.raw',
                   '.mp4', '.mov', '.wmv', '.avchd', '.flv', '.f4v', '.swf', '.mkv', '.mpeg']
    query = 'INSERT INTO Post_media(media_file_path, longtitude, latitude, post_id, filter_id) VALUES '

    for i in range(40000):
        media_file_path = (random.choice(DISK) + random.choice(FOLDER) + random.choice(FILE_NAME) +
                           random.choice(FILE_FORMAT))
        longitude = str(np.random.uniform(-180, 180))
        latitude = str(np.random.uniform(-90, 90))
        post_id = random.randint(36229, 37428)
        filter_id = random.randint(1, 15)
        query += f'(\'{media_file_path}\', \'{longitude}\', \'{latitude}\', {post_id}, {filter_id}), '
    query = query[:-2]
    query += ';'
    return query


def fill_Post_media_User_tag():
    query = 'INSERT INTO Post_media_User_tag(post_media_id, user_id, x_coordinate, y_coordinate) VALUES '
    for i in range(2000):
        post_media_id = random.randint(1, 2402)
        user_id = random.randint(1, 600)
        x_coordinate = random.randint(1, 1000)
        y_coordinate = random.randint(1, 1000)
        query += f'({post_media_id}, {user_id}, {x_coordinate}, {y_coordinate}), '
    query = query[:-2]
    query += ';'
    return query


def fill_Effect_Post_media():
    query = 'INSERT INTO Effect_Post_media(effect_id, post_media_id) VALUES '
    for post_media_id in range(1, 2042):
        for effect_id in range(1, 21):
            if random.randint(0, 100) <= 10:
                query += f'({effect_id}, {post_media_id}), '
    query = query[:-2]
    query += ';'
    return query


def fill_Follower():
    query = 'INSERT INTO Follower(follower_id, followee_id) VALUES '
    for follower_id in range(1, 601):
        for followee_id in range(1, 601):
            if follower_id is not followee_id:
                if random.randint(0, 100) <= 10:
                    query += f'({follower_id}, {followee_id}), '
    query = query[:-2]
    query += ';'
    return query


def fill_Comment():
    INT = ['Hello! ', 'HEllo. ', 'hello ', 'HeLlO ', 'Hi ', 'HI! ', 'hI. ', 'Here is my ', 'What a nice day ',
           'How are you guys? ', 'Good morning, ', 'Let me introduce to you ', 'Have a nice day ', 'Nice to meet you! ',
           'Say hi to my ', 'This is ', 'I have a ', 'Good night, ']
    CONT = ['my cat! ', 'my new puppy! ', 'the picture of nature! ', 'something ', 'my girl friend ', 'our group. ',
            'Happy classmates ', 'nice weather ', 'feeling sleepy ', 'a book ', 'my lover ', 'my dream ', 'a bike ',
            'a car ',
            'new book ', 'new ps5 ', 'my friend ', 'oh dear ', 'Santa Clause ', 'oops ']
    EMOJI = ['=(', '=)', ':3', ';)', '.-.', '-_-', '+_+', '=_=', ':P', 'KEK', ':/', 'o_0', 'UwU', '*v*']
    query = 'INSERT INTO Comment(created_at, content, post_id, user_id) VALUES '
    for i in range(3600):
        created_at = generate_timestamp()
        content = random.choice(INT) + random.choice(CONT)
        if random.randint(0, 1) == 1:
            content += random.choice(EMOJI)
        post_id = random.randint(36229, 37428)
        user_id = random.randint(1, 600)
        query += f'(TO_TIMESTAMP({created_at}, \'DD MON YYYY HH24:MI\'), \'{content}\', {post_id}, {user_id}), '
    query = query[:-2]
    query += ';'
    return query


def fill_Reply():
    INT = ['Hello! ', 'HEllo. ', 'hello ', 'HeLlO ', 'Hi ', 'HI! ', 'hI. ', 'Here is my ', 'What a nice day ',
           'How are you guys? ', 'Good morning, ', 'Let me introduce to you ', 'Have a nice day ', 'Nice to meet you! ',
           'Say hi to my ', 'This is ', 'I have a ', 'Good night, ']
    CONT = ['my cat! ', 'my new puppy! ', 'the picture of nature! ', 'something ', 'my girl friend ', 'our group. ',
            'Happy classmates ', 'nice weather ', 'feeling sleepy ', 'a book ', 'my lover ', 'my dream ', 'a bike ',
            'a car ',
            'new book ', 'new ps5 ', 'my friend ', 'oh dear ', 'Santa Clause ', 'oops ']
    EMOJI = ['=(', '=)', ':3', ';)', '.-.', '-_-', '+_+', '=_=', ':P', 'KEK', ':/', 'o_0', 'UwU', '*v*']
    query = 'INSERT INTO Comment(created_at, content, post_id, user_id, parent_comment_id) VALUES '
    for i in range(1, 10801):
        created_at = generate_timestamp()
        content = random.choice(INT) + random.choice(CONT)
        if random.randint(0, 1) == 1:
            content += random.choice(EMOJI)
        # post_id = random.randint(36229, 37428)
        user_id = random.randint(1, 600)
        parent_comment_id = random.randint(14401, 18001 + i)
        query += f'(TO_TIMESTAMP({created_at}, \'DD MON YYYY HH24:MI\'), \'{content}\', (SELECT c.post_id FROM comment c WHERE c.comment_id = {parent_comment_id}), {user_id}, {parent_comment_id}), '
    query = query[:-2]
    query += ';'
    return query


def main():
    conn = ps.connect(database="instagram1",
                      user='postgres',
                      password='Icandoit2706')
    conn.autocommit = False
    cursor = conn.cursor()
    cursor.execute(fill_Post_media())
    conn.commit()
    cursor.close()
    conn.close()


main()

