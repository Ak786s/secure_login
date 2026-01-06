import mysql.connector

try:
    # Connect to MySQL (adjust your credentials)
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",   # your MySQL password
        database="secure_logins"    # optional, can remove to just test connection
    )
    
    if conn.is_connected():
        print("✅ MySQL Connector is working!")
        print("Connected to MySQL server version:", conn.get_server_info())
    
    conn.close()

except mysql.connector.Error as err:
    print("❌ Error:", err)
