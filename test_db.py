# import psycopg

# from app.config import settings


# print("Attempting to connect to Neon...")


# try:
#     with psycopg.connect(
#         settings.DATABASE_URL
#     ) as connection:

#         with connection.cursor() as cursor:

#             cursor.execute("SELECT version();")

#             result = cursor.fetchone()

#             print("SUCCESS!")
#             print("Connected to Neon.")
#             print(result)


# except Exception as error:

#     print("CONNECTION FAILED!")
#     print(type(error).__name__)
#     print(error)