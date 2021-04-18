import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE "staging_events" (
    "artist" VARCHAR(1000) NULL,
    "auth" VARCHAR(100) NULL,
    "firstName" VARCHAR(100) NULL,
    "gender" char(1) NULL,
    "itemInSession" INTEGER NULL,
    "lastName" VARCHAR(100) NULL,
    "length" DECIMAL(9,5) NULL,
    "level" VARCHAR(100) NULL,
    "location" VARCHAR(100) NULL,
    "method" VARCHAR(100) NULL,
    "page" VARCHAR(100) NULL,
    "registration" FLOAT NULL,
    "sessionId" VARCHAR(100) NULL,
    "song" VARCHAR(1000) NULL,
    "status" INTEGER NULL,
    "ts" BIGINT NULL,
    "userAgent" VARCHAR(1000) NULL,
    "userId"  INTEGER NULL);
""")

staging_songs_table_create = ("""
CREATE TABLE "staging_songs" (
    "artist_id" VARCHAR(50) NOT NULL,
    "artist_latitude" FLOAT NULL,
    "artist_location" VARCHAR(1000) NULL,
    "artist_longitude" FLOAT NULL,
    "artist_name" VARCHAR(1000) NOT NULL,
    "duration" FLOAT NOT NULL,
    "num_songs" INTEGER NOT NULL,
    "song_id" VARCHAR(50) NOT NULL,
    "title" VARCHAR(1000) NOT NULL,
    "year" INTEGER NOT NULL)
    diststyle all;
""")

songplay_table_create = ("""
CREATE TABLE "songplays" (
    "songplay_id" BIGINT IDENTITY (0,1) NOT NULL,
    "start_time" TIMESTAMP NULL REFERENCES time(ts),
    "user_id" INTEGER NOT NULL REFERENCES users(user_id) distkey,
    "level" VARCHAR(100) NULL, 
    "song_id" VARCHAR(50) NOT NULL REFERENCES songs(song_id), 
    "artist_id" VARCHAR(100) NOT NULL REFERENCES artists(artist_id) sortkey, 
    "session_id" VARCHAR(100) NULL, 
    "location" VARCHAR(1000) NULL,
    "user_agent" VARCHAR(1000) NULL);
""")

user_table_create = ("""
CREATE TABLE "users" (
    "user_id" INTEGER NOT NULL PRIMARY KEY,
    "firstName" VARCHAR(100) NULL,
    "lastName" VARCHAR(100) NULL,
    "gender" char(1) NULL,
    "level" VARCHAR(100) NULL)
    diststyle all;
""")

song_table_create = ("""
CREATE TABLE "songs" (
    "song_id" VARCHAR(50) NOT NULL PRIMARY KEY,
    "title" VARCHAR(1000) NOT NULL,    
    "artist_id" VARCHAR(50) REFERENCES artists(artist_id),
    "year" INTEGER NOT NULL,
    "duration" FLOAT NOT NULL)
    diststyle all;
""")

artist_table_create = ("""
CREATE TABLE "artists" (
    "artist_id" VARCHAR(100) NOT NULL PRIMARY KEY,
    "name" VARCHAR(1000) NOT NULL,
    "location" VARCHAR(1000) NULL,
    "artist_latitude" double precision NULL,
    "artist_longitude" double precision NULL)
    diststyle all;;
""")

time_table_create = ("""
CREATE TABLE "time" (
    "ts" TIMESTAMP NOT NULL PRIMARY KEY,
    "hour" INTEGER NOT NULL, 
    "day"  INTEGER NOT NULL, 
    "week"  INTEGER NOT NULL, 
    "month"  INTEGER NOT NULL, 
    "year"  INTEGER NOT NULL, 
    "weekday" INTEGER NULL)
    diststyle key distkey (ts);
""")

# STAGING TABLES
staging_events_copy = ("""
    COPY staging_events FROM 's3://udacity-dend/log_data/2018/11/2018-11'
    credentials 'aws_iam_role={}'
    json 'auto ignorecase'
""").format(*config['IAM_ROLE'].values())

staging_songs_copy = ("""
    COPY staging_songs FROM 's3://udacity-dend/song_data/A/'
    credentials 'aws_iam_role={}'
    json 'auto ignorecase'
""").format(*config['IAM_ROLE'].values())

# FINAL TABLES
songplay_table_insert = ("""
    INSERT INTO songplays (start_time,user_id,level,song_id,artist_id,session_id,location,user_agent)
    SELECT date_add('ms',se.ts,'1970-01-01'),se.userId,se.level,ss.song_id,ss.artist_id,se.sessionId,se.location,se.userAgent
    FROM staging_events se, staging_songs ss
    WHERE se.song = ss.title
    AND se.artist = ss.artist_name
    AND page='NextSong';
""")

user_table_insert = ("""
   INSERT INTO users(user_id,firstName,lastName,gender,level)
   SELECT userId,firstName,lastName,gender,level
   FROM staging_events
   WHERE staging_events.userId IS NOT NULL
   AND staging_events.userId NOT IN (SELECT DISTINCT user_id FROM users);   
""")

song_table_insert = ("""
   INSERT INTO songs(song_id,title,artist_id,year,duration)
   SELECT song_id,title,artist_id,year,duration
   FROM staging_songs
   WHERE song_id NOT IN (SELECT DISTINCT song_id FROM songs); 
""")

artist_table_insert = ("""
   INSERT INTO artists(artist_id,name,location,artist_latitude,artist_longitude)
   SELECT artist_id,artist_name,artist_location,artist_latitude,artist_longitude
   FROM staging_songs
   WHERE artist_id NOT IN (SELECT DISTINCT artist_id FROM artists);
""")

time_table_insert = ("""
   INSERT INTO time(ts,hour,day,week,month,year,weekday) 
   select date_add('ms',ts,'1970-01-01'),
          DATE_PART(h, date_add('ms',ts,'1970-01-01')),
          DATE_PART(d, date_add('ms',ts,'1970-01-01')),
          DATE_PART(w, date_add('ms',ts,'1970-01-01')),
          DATE_PART(m, date_add('ms',ts,'1970-01-01')),
          DATE_PART(y, date_add('ms',ts,'1970-01-01')),
          DATE_PART(dow, date_add('ms',ts,'1970-01-01'))
   FROM staging_events
   WHERE ts NOT IN (SELECT DISTINCT ts FROM time);
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, artist_table_create, song_table_create, time_table_create, songplay_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [user_table_insert,artist_table_insert, song_table_insert, time_table_insert, songplay_table_insert]
