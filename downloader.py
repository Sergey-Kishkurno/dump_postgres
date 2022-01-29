import psycopg2
import psycopg2.extensions

db_creds = {
    #  keywords matter - are predefined
    'host': 'localhost',
    'dbname': 'dshop',
    'user': 'pguser',
    'password': 'secret'
}


def download():

    query_table_names = "SELECT table_name FROM information_schema.tables " \
                        "WHERE table_schema='public' " \
                        "ORDER BY table_name"

    conn = psycopg2.connect(**db_creds)
    if not conn:
        print("Error connecting to DB")
        return None
    cursor = conn.cursor()

    result = None

    try:
        cursor.execute(query_table_names)
        result = cursor.fetchall()

    except psycopg2.Error as e:
        print(f"{type(e).__module__.removesuffix('.errors')}:{type(e).__name__}: {str(e).rstrip()}")
        if conn:
            conn.rollback()
    finally:
        cursor.close()

    db_tables = [x[0] for x in result]
    # print(db_tables)

    for table in db_tables:

        conn = psycopg2.connect(**db_creds)
        if not conn:
            print("Error connecting to DB")
            return None
        cursor = conn.cursor()

        query_for_a_table = f"SELECT * FROM {table}"

        try:
            cursor.execute(query_for_a_table)

            with open(file= table + '.csv', mode='w') as csv_file:
                cursor.copy_expert(f'COPY {table} TO STDOUT WITH HEADER CSV', csv_file)

        except psycopg2.Error as e:
            print(f"{type(e).__module__.removesuffix('.errors')}:{type(e).__name__}: {str(e).rstrip()}")
            if conn:
                conn.rollback()
        finally:
            cursor.close()


if __name__ == "__main__":
    download()


