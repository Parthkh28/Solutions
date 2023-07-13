-- Create the Orchestra table
CREATE TABLE IF NOT EXISTS Orchestra (
    id INTEGER PRIMARY KEY,
    name TEXT,
    founded_year INTEGER,
    city TEXT
);

-- Create the Concert table
CREATE TABLE IF NOT EXISTS Concert (
    id INTEGER PRIMARY KEY,
    orchestra_id INTEGER,
    date TEXT,
    location TEXT,
    FOREIGN KEY (orchestra_id) REFERENCES Orchestra(id)
);

-- Create the Work table
CREATE TABLE IF NOT EXISTS Work (
    id INTEGER PRIMARY KEY,
    composer TEXT,
    title TEXT
);

-- Create the ConcertWork table
CREATE TABLE IF NOT EXISTS ConcertWork (
    id INTEGER PRIMARY KEY,
    concert_id INTEGER,
    work_id INTEGER,
    duration INTEGER,
    FOREIGN KEY (concert_id) REFERENCES Concert(id),
    FOREIGN KEY (work_id) REFERENCES Work(id)
);

-- Create the Artist table
CREATE TABLE IF NOT EXISTS Artist (
    id INTEGER PRIMARY KEY,
    name TEXT,
    instrument TEXT
);

-- Create the ConcertArtist table
CREATE TABLE IF NOT EXISTS ConcertArtist (
    id INTEGER PRIMARY KEY,
    concert_id INTEGER,
    artist_id INTEGER,
    FOREIGN KEY (concert_id) REFERENCES Concert(id),
    FOREIGN KEY (artist_id) REFERENCES Artist(id)
);

-- Insert data into the Orchestra table
INSERT INTO Orchestra (id, name, founded_year, city)
SELECT id, name, foundedYear, city
FROM json_each(json_extract(json_data, '$.orchestras'));

-- Insert data into the Concert table
INSERT INTO Concert (id, orchestra_id, date, location)
SELECT id, orchestraId, date, location
FROM json_each(json_extract(json_data, '$.concerts'));

-- Insert data into the Work table
INSERT INTO Work (id, composer, title)
SELECT id, composer, title
FROM json_each(json_extract(json_data, '$.works'));

-- Insert data into the ConcertWork table
INSERT INTO ConcertWork (id, concert_id, work_id, duration)
SELECT id, concertId, workId, duration
FROM json_each(json_extract(json_data, '$.concertWorks'));

-- Insert data into the Artist table
INSERT INTO Artist (id, name, instrument)
SELECT id, name, instrument
FROM json_each(json_extract(json_data, '$.artists'));

-- Insert data into the ConcertArtist table
INSERT INTO ConcertArtist (id, concert_id, artist_id)
SELECT id, concertId, artistId
FROM json_each(json_extract(json_data, '$.concertArtists'));
