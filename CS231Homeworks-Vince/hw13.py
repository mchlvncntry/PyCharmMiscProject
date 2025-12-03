#!/usr/bin/python3
# Week 12/01-12/07 Assignment: SQLite
import sqlite3

conn = sqlite3.connect("/users/abrick/resources/art.db")
cursor = conn.cursor()

# Query CCSF Ocean Campus artworks, chronologically ordered
cursor.execute("""
    SELECT 
        creation_date,
        display_title,
        artist,
        location_description
    FROM art
    WHERE
        LOWER(facility) LIKE '%ccsf%ocean campus%'
     OR LOWER(street_address_or_intersection) LIKE '%50%frida kahlo%'
     OR (
            CAST(latitude AS REAL)  BETWEEN 37.724 AND 37.728
        AND CAST(longitude  AS REAL) BETWEEN -122.452 AND -122.447
        )
    ORDER BY CAST(creation_date AS INTEGER) ASC;
""")

rows = cursor.fetchall()

# Print header row ONCE at the top
print("\nChronologically Ordered List of Artworks Installed on CCSF Ocean Campus\n")
print("Creation Date -- Title -- Artist -- Location")
print("-" * 80)

for creation_date, title, artist, loc_desc in rows:
    creation_date = creation_date if creation_date else "Unknown Date"
    title         = title if title else "Untitled"
    artist        = artist if artist else "Unknown Artist"
    loc_desc      = loc_desc if loc_desc else "No location description"

    print(f"{creation_date} -- {title} -- {artist} -- {loc_desc}")
print()
conn.close()
