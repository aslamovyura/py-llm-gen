import psycopg2

def test_connection():
    try:
        # Connect to the database using localhost and port 5433
        conn = psycopg2.connect(
            host="0.0.0.0",
            port=5433,
            database="equipment_db",
            user="postgres",
            password="StrongPassw@rd123"
        )
        
        # Create a cursor
        cur = conn.cursor()
        
        # Execute a test query
        cur.execute("SELECT 1")
        result = cur.fetchone()
        
        print("Connection successful!")
        print("Test query result:", result[0])
        
        # Close cursor and connection
        cur.close()
        conn.close()
            
    except Exception as e:
        print("Connection failed!")
        print(f"Error: {e}")

if __name__ == "__main__":
    test_connection() 