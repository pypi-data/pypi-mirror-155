import psycopg

from logmgmt import logger


def save(cur, index, site):
    # Pass data to fill a query placeholders and let Psycopg perform
    # the correct conversion (no SQL injections!)
    cur.execute(
        'INSERT INTO "tranco_list" ("index", "site") VALUES (%s, %s)',
        (index, site))


with open('Resources/top-1m.csv') as my_file:
    testsite_array = my_file.readlines()
    with psycopg.connect(host="193.196.53.97", port=50000, dbname="Social-Login-Scans", user="westersm",
                         password="dfdW-FCiL@kEo3wcJjPx@mVj-") as conn:
        with conn.cursor() as cur:
            for trancoentry in testsite_array:
                splitted = trancoentry.split(",")
                save(cur, splitted[0], splitted[1].replace("\n", ""))
                if int(splitted[0]) % 100 == 0:
                    logger.info("Saved " + splitted[0])
        conn.commit()
    conn.close()
