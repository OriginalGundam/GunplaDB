#This is the code that actually inputs the information into the tables.
#In particular, this one is for the model kits and there are three statuses:
#Active - Standard retail release and can be found anywhere
#Limited - P-Bandai, Gundam Base exclusive, or other limited distributions.
#Discontinued - No longer produced or flat out retired with little chance of returning.

from database import get_connection


def seed_gunpla():

    db_connection = get_connection()
    db_cursor = db_connection.cursor()

    gunpla = [

        (
            "HGUC RX-78-2 Gundam Revive",
            "HGUC",
            "HG",
            False,
            False,
            "Active"
        ),

        (
            "RG RX-78-2 Gundam Ver. 2.0",
            "RG",
            "RG",
            False,
            False,
            "Active"
        ),

        (
            "HGUC RX-77-2 Guncannon Revive",
            "HGUC",
            "HG",
            False,
            False,
            "Active"
        ),

        (
            "HGUC RX-75-4 Guntank",
            "HGUC",
            "HG",
            False,
            False,
            "Active"
        )

    ]

    for kit in gunpla:

        db_cursor.execute("""

            INSERT INTO gunpla
            (name, grade, category,
            p_bandai, variant, status)

            VALUES (%s, %s, %s,
                    %s, %s, %s);

        """, kit)

    db_connection.commit()

    db_cursor.close()
    db_connection.close()

    print("Gunpla added successfully.")


if __name__ == "__main__":
    seed_gunpla()