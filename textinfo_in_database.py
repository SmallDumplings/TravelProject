import sqlite3


def import_in_base(id, name):
    with open(name, encoding="utf-8") as f:
        con = sqlite3.connect("project_country")
        cur = con.cursor()
        _import_info_in_sqlite = """INSERT INTO coun_info (id, info) VALUES (?, ?)"""
        data_tuple = id, f.read()
        cur.execute(_import_info_in_sqlite, data_tuple)
        con.commit()
        con.close()


for i in range(1, 37):
    import_in_base(i, f"info_coun/info_{i}.txt")