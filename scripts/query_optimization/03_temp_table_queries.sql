-- TEMP TABLE version: cache filtered energetic explicit songs
DROP TABLE IF EXISTS temp_explicit_energy;
CREATE TEMP TABLE temp_explicit_energy AS
SELECT * FROM spotify_tracks
WHERE explicit = true AND energy > 0.85 AND year >= 2020;

-- Use TEMP TABLE
SELECT name, artists, energy, valence, year
FROM temp_explicit_energy
ORDER BY energy DESC
LIMIT 20;

-- TEMP TABLE for high dance tracks
DROP TABLE IF EXISTS temp_dance_tempo;
CREATE TEMP TABLE temp_dance_tempo AS
SELECT * FROM spotify_tracks
WHERE danceability > 0.8 AND tempo > 120;

SELECT name, artists, danceability, tempo
FROM temp_dance_tempo
ORDER BY tempo DESC
LIMIT 30;

-- TEMP TABLE for loudness binning
DROP TABLE IF EXISTS temp_loudness;
CREATE TEMP TABLE temp_loudness AS
SELECT FLOOR(loudness / 5) * 5 AS loudness_group, valence
FROM spotify_tracks;

SELECT loudness_group, AVG(valence) AS avg_valence, COUNT(*) AS track_count
FROM temp_loudness
GROUP BY loudness_group
ORDER BY loudness_group;