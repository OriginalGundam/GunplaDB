# This section of code is made to create the tables.
from database import get_connection

def create_tables():
    #Setting up connections
    connection = get_connection()
    cursor = connection.cursor()
    
    #Tables for the gunpla:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gunpla (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            grade VARCHAR(50) NOT NULL,
            category VARCHAR(20) NOT NULL,
            p_bandai BOOLEAN DEFAULT FALSE,
            variant BOOLEAN DEFAULT FALSE,
            status VARCHAR(50)
        );
    """)
    
    #Tables for the stores:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stores (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            website TEXT,
            marketplace BOOLEAN DEFAULT FALSE,
            reliability VARCHAR(20)
        );
    """)
    
    #Tables for the price history:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id SERIAL PRIMARY KEY,

            gunpla_id INTEGER NOT NULL,
            store_id INTEGER NOT NULL,

            price DECIMAL(10,2) NOT NULL,

            availability VARCHAR(50),

            stock INTEGER,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            product_url TEXT,

            FOREIGN KEY (gunpla_id)
                REFERENCES gunpla(id)
                ON DELETE CASCADE,

            FOREIGN KEY (store_id)
                REFERENCES stores(id)
                ON DELETE CASCADE
        );
    """)
    
    #Saves any changes made:
    connection.commit()
    
    #End connection:
    cursor.close()
    connection.close()
    
    print("Database tables created succesfully.")

if __name__ == "__main__":
    create_tables()