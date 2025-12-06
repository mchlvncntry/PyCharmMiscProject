#!/usr/bin/python3
# Week 12/01-12/07 Assignment: SQLite
import sqlite3

PATH_TO_DB = "/users/abrick/resources/art.db"

# Sort numerically when creation_date begins with digits.
# GLOB '[0-9]*' checks whether the field *starts with a number*,
# If the date is numeric, convert it to integer for proper chronological sorting.
# If not numeric, push it to the bottom by assigning the value 9999.'''
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
                    ELSE 9999     -- push non-numeric or missing dates to the end
                 END ASC;
    """)
    resulting_artworks = my_cursor.fetchall()

print(f"\nNumber of artworks found: {len(resulting_artworks)}")
print(f"Source: {PATH_TO_DB}\n")
print(f"Chronologically Ordered List of {len(resulting_artworks)} Artworks at CCSF Ocean Campus\n")
for i, (creation_date, title, artist, loc_desc) in enumerate(resulting_artworks, start=1):
    print(f"{i}.")
    print(f"   Creation Date:      {creation_date or 'Unknown'}")
    print(f"   Display Title:      {title or 'Untitled'}")
    print(f"   Artist:             {artist or 'Unknown Artist'}")
    print(f"   Location:           {loc_desc or 'No description'}")
    print()  # blank line between items
