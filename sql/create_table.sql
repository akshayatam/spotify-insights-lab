-- Create table 
DROP TABLE IF EXISTS spotify_tracks;
CREATE TABLE spotify_tracks (
    id TEXT PRIMARY KEY,                          -- Spotify track ID
    name TEXT NOT NULL,                           -- Track name
    album TEXT NOT NULL,                          -- Album name
    artists TEXT NOT NULL,                        -- Artist(s) name(s)
    explicit BOOLEAN,                             -- Whether track is explicit
    danceability FLOAT,                           -- Audio feature
    energy FLOAT,                                 -- Audio feature
    loudness FLOAT,                               -- in decibels (dB)
    speechiness FLOAT,                            -- Audio feature
    acousticness FLOAT,                           -- Audio feature
    instrumentalness FLOAT,                       -- Audio feature
    liveness FLOAT,                               -- Live performance likelihood
    valence FLOAT,                                -- Musical positiveness
    tempo FLOAT,                                  -- BPM
    duration_min FLOAT,                           -- Duration in minutes
    year INTEGER,                                 -- Release year
    release_date DATE                             -- Release date
);
