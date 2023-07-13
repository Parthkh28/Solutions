import json
import sqlite3

# Load the JSON data
with open('nested_data.json') as file:
    data = json.load(file)

# Connect to the database
conn = sqlite3.connect('orchestra.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Orchestra (
        id INTEGER PRIMARY KEY,
        name TEXT,
        founded_year INTEGER,
        city TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Concert (
        id INTEGER PRIMARY KEY,
        orchestra_id INTEGER,
        date TEXT,
        location TEXT,
        FOREIGN KEY (orchestra_id) REFERENCES Orchestra(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Work (
        id INTEGER PRIMARY KEY,
        composer TEXT,
        title TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS ConcertWork (
        id INTEGER PRIMARY KEY,
        concert_id INTEGER,
        work_id INTEGER,
        duration INTEGER,
        FOREIGN KEY (concert_id) REFERENCES Concert(id),
        FOREIGN KEY (work_id) REFERENCES Work(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Artist (
        id INTEGER PRIMARY KEY,
        name TEXT,
        instrument TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS ConcertArtist (
        id INTEGER PRIMARY KEY,
        concert_id INTEGER,
        artist_id INTEGER,
        FOREIGN KEY (concert_id) REFERENCES Concert(id),
        FOREIGN KEY (artist_id) REFERENCES Artist(id)
    )
''')

# Extract and transform the data
orchestras = data['orchestras']
concerts = data['concerts']
works = data['works']
artists = data['artists']

# Insert data into the Orchestra table
for orchestra in orchestras:
    cursor.execute('INSERT INTO Orchestra (id, name, founded_year, city) VALUES (?, ?, ?, ?)',
                   (orchestra['id'], orchestra['name'], orchestra['foundedYear'], orchestra['city']))

# Insert data into the Concert table
for concert in concerts:
    cursor.execute('INSERT INTO Concert (id, orchestra_id, date, location) VALUES (?, ?, ?, ?)',
                   (concert['id'], concert['orchestraId'], concert['date'], concert['location']))

# Insert data into the Work table
for work in works:
    cursor.execute('INSERT INTO Work (id, composer, title) VALUES (?, ?, ?)',
                   (work['id'], work['composer'], work['title']))

# Insert data into the ConcertWork table
for concert_work in data['concertWorks']:
    cursor.execute('INSERT INTO ConcertWork (id, concert_id, work_id, duration) VALUES (?, ?, ?, ?)',
                   (concert_work['id'], concert_work['concertId'], concert_work['workId'], concert_work['duration']))

# Insert data into the Artist table
for artist in artists:
    cursor.execute('INSERT INTO Artist (id, name, instrument) VALUES (?, ?, ?)',
                   (artist['id'], artist['name'], artist['instrument']))

# Insert data into the ConcertArtist table
for concert_artist in data['concertArtists']:
    cursor.execute('INSERT INTO ConcertArtist (id, concert_id, artist_id) VALUES (?, ?, ?)',
                   (concert_artist['id'], concert_artist['concertId'], concert_artist['artistId']))

# Commit the changes and close the connection
conn.commit()
conn.close()
