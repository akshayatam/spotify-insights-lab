-- 1. Most energetic explicit tracks released after 2020
SELECT name, artists, energy, valence, year
FROM spotify_tracks
WHERE explicit = true
  AND energy > 0.85
  AND year >= 2020
ORDER BY energy DESC
LIMIT 20;

-- 2. High tempo + high danceability tracks
SELECT name, artists, danceability, tempo
FROM spotify_tracks
WHERE danceability > 0.8 AND tempo > 120
ORDER BY tempo DESC
LIMIT 30;

-- 3. Track count per year
SELECT year, COUNT(*) AS track_count
FROM spotify_tracks
GROUP BY year
ORDER BY year;

-- 4. Valence by loudness group
SELECT
  FLOOR(loudness / 5) * 5 AS loudness_group,
  AVG(valence) AS avg_valence,
  COUNT(*) AS track_count
FROM spotify_tracks
GROUP BY loudness_group
ORDER BY loudness_group;