#!/usr/bin/python3
# Week 12/01-12/07 Assignment: SQLite
import sqlite3

PATH_TO_DB = "/users/abrick/resources/art.db"

with sqlite3.connect(PATH_TO_DB) as my_conn:
    my_cursor = my_conn.cursor()
    my_cursor.execute("""
        SELECT creation_date, display_title, artist, location_description
        FROM art
        WHERE LOWER(facility) LIKE '%ccsf%ocean campus%'
           OR LOWER(street_address_or_intersection) LIKE '%50%frida kahlo%'
        ORDER BY CASE
                    WHEN creation_date GLOB '[0-9]*'
                        THEN CAST(creation_date AS INTEGER)
                    ELSE 9999
                 END ASC;
    """)
    resulting_artworks = my_cursor.fetchall()

print(f"\nNumber of artworks found: {len(resulting_artworks)}")
print(f"Source: {PATH_TO_DB}\n")

print(f"Chronologically Ordered List of {len(resulting_artworks)} Artworks at CCSF Ocean Campus\n")
print(f"{'Creation Date':<14} | {'Display Title':<42} | {'Artist':<28} | {'Location'}")
print("-" * 140)

for creation_date, title, artist, loc_desc in resulting_artworks:
    print(f"{creation_date or 'Unknown':<14} | "
          f"{title or 'Untitled':<42} | "
          f"{artist or 'Unknown Artist':<28} | "
          f"{loc_desc or 'No description'}")

print()
