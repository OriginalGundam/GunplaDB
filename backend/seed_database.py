#Adds stores and starter kits to database

from database import get_connection


def seed_database():

    db_connection = get_connection()
    db_cursor = db_connection.cursor()

    stores = [

        ("USA Gundam Store",
        "https://www.usagundamstore.com",
        False,
        "Excellent"),

        ("HobbyLink Japan",
        "https://www.hlj.com",
        False,
        "Excellent"),

        ("P-Bandai US",
        "https://p-bandai.com/us",
        False,
        "Official"),

        ("Newtype",
        "https://newtype.us",
        False,
        "Excellent"),

        ("Gundam Planet",
        "https://www.gundamplanet.com",
        False,
        "Excellent"),

        ("Toy Arena",
        "https://toyarena.com",
        False,
        "Good"),

        ("BigBadToyStore",
        "https://www.bigbadtoystore.com",
        False,
        "Excellent"),

        ("Galactic Toys & Collectibles",
        "https://galactictoys.com",
        False,
        "Good"),

        ("Plaza Japan",
        "https://www.plazajapan.com",
        False,
        "Excellent"),

        ("Okini Land",
        "https://okini.land",
        False,
        "Good"),

        ("Animota",
        "https://animota.net",
        False,
        "Good"),

        ("Amazon",
        "https://www.amazon.com",
        True,
        "Marketplace"),

        ("eBay",
        "https://www.ebay.com",
        True,
        "Marketplace")
    ]


    for store in stores:

        db_cursor.execute("""
            INSERT INTO stores
            (name, website, marketplace, reliability)
            VALUES (%s, %s, %s, %s);
        """, store)


    db_connection.commit()

    db_cursor.close()
    db_connection.close()

    print("Stores added successfully.")


if __name__ == "__main__":
    seed_database()