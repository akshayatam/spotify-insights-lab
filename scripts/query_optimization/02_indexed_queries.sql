-- Add indexes to support optimized queries
CREATE INDEX IF NOT EXISTS idx_explicit_energy_year ON spotify_tracks(explicit, energy, year);
CREATE INDEX IF NOT EXISTS idx_danceability_tempo ON spotify_tracks(danceability, tempo);
CREATE INDEX IF NOT EXISTS idx_year ON spotify_tracks(year);
CREATE INDEX IF NOT EXISTS idx_loudness ON spotify_tracks(loudness);

-- Optimized versions of previous queries

-- 1. Optimized energetic explicit tracks
SELECT name, artists, energy, valence, year
FROM spotify_tracks
WHERE explicit = true
  AND energy > 0.85
  AND year >= 2020
ORDER BY energy DESC
LIMIT 20;

-- 2. Optimized danceability + tempo filter
SELECT name, artists, danceability, tempo
FROM spotify_tracks
WHERE danceability > 0.8 AND tempo > 120
ORDER BY tempo DESC
LIMIT 30;

-- 3. Optimized track count per year (uses idx_year)
SELECT year, COUNT(*) AS track_count
FROM spotify_tracks
GROUP BY year
ORDER BY year;

-- 4. Optimized loudness binning with index
SELECT
  FLOOR(loudness / 5) * 5 AS loudness_group,
  AVG(valence) AS avg_valence,
  COUNT(*) AS track_count
FROM spotify_tracks
GROUP BY loudness_group
ORDER BY loudness_group;