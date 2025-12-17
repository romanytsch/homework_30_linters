import sqlite3

with sqlite3.connect("hw_3_database.db") as conn:
    cursor = conn.cursor()

    print("1. Количество записей в каждой таблице:")
    counts_query = """
    SELECT 'table_1' AS table_name, COUNT(*) AS row_count FROM table_1
    UNION ALL
    SELECT 'table_2' AS table_name, COUNT(*) AS row_count FROM table_2
    UNION ALL
    SELECT 'table_3' AS table_name, COUNT(*) AS row_count FROM table_3
    """
    cursor.execute(counts_query)
    for table, count in cursor.fetchall():
        print(f"{table}: {count} записей")
    print()

    print("2. Уникальных записей в table_1:")
    unique_query = """
    SELECT COUNT(*) AS unique_count
    FROM (SELECT id, value FROM table_1 GROUP BY id, value HAVING COUNT(*) = 1)
    """
    cursor.execute(unique_query)
    unique_count = cursor.fetchone()[0]
    print(f"   {unique_count} уникальных записей")
    print()

    print("3. Записей table_1, встречающихся в table_2:")
    common12_query = """
    SELECT COUNT(*) FROM (
            SELECT id, value FROM table_1
            INTERSECT
            SELECT id, value FROM table_2
        )
    """
    cursor.execute(common12_query)
    common12_count = cursor.fetchone()[0]
    print(f"   {common12_count} общих записей")
    print()

    print("4. Записей table_1, встречающихся в table_2 И table_3:")
    common123_query = """
    SELECT COUNT(*) FROM (
            SELECT id, value FROM table_1
            INTERSECT
            SELECT id, value FROM table_2
            INTERSECT
            SELECT id, value FROM table_3
        )
    """
    cursor.execute(common123_query)
    common123_count = cursor.fetchone()[0]
    print(f"   {common123_count} общих записей")