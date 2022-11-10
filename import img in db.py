import sqlite3
def convertToBinaryData(name):
    with open(name, 'rb') as file:
        blobData = file.read()
    return blobData


def insertBLOB(name, photo):
    try:
        sqliteConnection = sqlite3.connect('project_country')
        cursor = sqliteConnection.cursor()
        sqlite_insert_blob_query = """ INSERT INTO coun_info_im
                                  (id, img) VALUES (?, ?)"""
        empPhoto = convertToBinaryData(photo)
        data_tuple = (name, empPhoto)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")

for i in range(1, 37):
    insertBLOB(i, f"img_coun/inim_{i}.png")

# загрузка картинок в базу данных