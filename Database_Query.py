# import mysql.connector
# from mysql.connector import Error
# import datetime
#
#
#
# db_config = {
#     "host": "localhost",
#     "user": "root",
#     "password": "root",
#     "database": "face_recognition_det",
# }
#
# class FaceDatabase:
#     def __init__(self, id, name,date, cam_name, details):
#         self.id = id
#         self.name = name
#         self.date=date
#         self.cam_name = cam_name
#         self.details = details
#         self.db_config = db_config
#
#     def store_face_detection(self):
#         try:
#             connection = mysql.connector.connect(**self.db_config)
#             if connection.is_connected():
#                 cursor = connection.cursor()
#
#                 select_query = "SELECT * FROM facerecog WHERE name = %s"
#                 cursor.execute(select_query, (self.name,))
#                 result = cursor.fetchall()
#
#                 if len(result) > 0:
#                     update_query = "UPDATE facerecog SET came_name = %s, details = %s WHERE name = %s"
#                     cursor.execute(update_query, (self.came_name, self.details, self.name,))
#                 else:
#                     insert_query = "INSERT INTO facerecog (id, name, date, cam_name, details) VALUES (%s, %s, %s, %s)"
#                     cursor.execute(insert_query, (self.id, self.name,self.date ,self.cam_name, self.details,))
#
#                 connection.commit()
#                 print("Data inserted or updated successfully.")
#
#         except Error as e:
#             print(f"Error: {e}")
#
#         finally:
#             if connection.is_connected():
#                 cursor.close()
#                 connection.close()
#
#
# # db_config = {
# #     "host": "localhost",
# #     "user": "root",
# #     "password": "root",
# #     "database": "faces_details",
# # }
#
# # Example usage:
# id_value = 1
# name_value = "danush"
# cam_name_value = "Camera 1"
# details_value = b"{'dhanush': ['15:57:23', '15:57:24', '15:57:25', '15:57:26', '15:57:29']}"
# # db_config = db_config
#
#
# face_db = FaceDatabase(id_value, name_value, cam_name_value, details_value,db_config)
# face_db.store_face_detection()


# import mysql.connector
# from mysql.connector import Error
# import datetime
#
# db_config = {
#     "host": "localhost",
#     "user": "root",
#     "password": "root",
#     "database": "face_recognition_details",
# }
#
# class FaceDatabase:
#     def __init__(self, id, date, cam_name, details):
#         self.id = id
#         self.date = date
#         self.cam_name = cam_name
#         self.details = details
#         self.db_config = db_config
#
#     def store_face_detection(self):
#         try:
#             connection = mysql.connector.connect(**self.db_config)
#             if connection.is_connected():
#                 cursor = connection.cursor()
#
#                 select_query = "SELECT * FROM facerecog WHERE id = %s"
#                 cursor.execute(select_query, (self.id,))
#                 result = cursor.fetchall()
#
#                 if len(result) > 0:
#                     update_query = "UPDATE facerecog SET cam_name = %s, details = %s WHERE id = %s"
#                     cursor.execute(update_query, (self.cam_name, self.details, self.id,))
#                 else:
#                     insert_query = "INSERT INTO facerecog (id, date, cam_name, details) VALUES (%s, %s, %s, %s)"
#                     cursor.execute(insert_query, (self.id, self.date, self.cam_name, self.details,))
#
#                 connection.commit()
#                 print("Data inserted or updated successfully.")
#
#         except Error as e:
#             print(f"Error: {e}")
#
#         finally:
#             if connection.is_connected():
#                 cursor.close()
#                 connection.close()
#
# # Example usage:
# id_value = 2
# cam_name_value = "Camera 2"
# details_value = b"{'dhanush': ['16:58:23', '16:54:24', '17:54:25', '17:58:26', '17:58:29']}"
# date_value = datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
#
# face_db = FaceDatabase(id_value, date_value, cam_name_value, details_value)
# face_db.store_face_detection()

########################################################################################################################


import mysql.connector
from mysql.connector import Error
import datetime
import json

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "collision_det"
}

class FaceDatabase:
    def __init__(self):
        self.db_config = db_config

    def get_face_details(self, id):
        try:
            connection = mysql.connector.connect(**self.db_config)
            if connection.is_connected():
                cursor = connection.cursor()

                select_query = "SELECT details FROM collision_details WHERE id = %s"
                cursor.execute(select_query, (id,))
                result = cursor.fetchone()

                if result:
                    return result[0]

        except Error as e:
            print(f"Error: {e}")

        finally:    
            if connection.is_connected():
                cursor.close()
                connection.close()

        return None

    def update_difference(self, id, total_time_hours):
        try:
            connection = mysql.connector.connect(**self.db_config)
            if connection.is_connected():
                cursor = connection.cursor()

                update_query = "UPDATE collision_details SET difference = %s WHERE id = %s"
                cursor.execute(update_query, (total_time_hours, id))

                connection.commit()
                print("Total time difference in hours inserted successfully.")

        except Error as e:
            print(f"Error: {e}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
# Example usage:
face_db = FaceDatabase()

# IDs of the rows you want to compare
id_value_1 = 1
id_value_2 = 2

details_value_1 = face_db.get_face_details(id_value_1)
details_value_2 = face_db.get_face_details(id_value_2)

if details_value_1 and details_value_2:
    details_1 = eval(details_value_1.decode("utf-8"))
    details_2 = eval(details_value_2.decode("utf-8"))

    # Calculate total time difference in hours for corresponding indexes
    total_time_difference_seconds = 0

    for key in details_1:
        if key in details_2:
            for idx in range(min(len(details_1[key]), len(details_2[key]))):
                time_1 = datetime.datetime.strptime(details_1[key][idx], '%H:%M:%S')
                time_2 = datetime.datetime.strptime(details_2[key][idx], '%H:%M:%S')
                time_diff = abs((time_1 - time_2).total_seconds())

                # Accumulate time differences for each index
                total_time_difference_seconds += time_diff

    # Convert total time difference to hours
    total_time_difference_hours = total_time_difference_seconds / 3600  # 3600 seconds in an hour

    # Update the database with the total time difference in hours
    face_db.update_difference(id_value_1, total_time_difference_hours)
else:
    print("Failed to retrieve details for comparison.")