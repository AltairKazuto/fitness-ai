import psycopg2
from psycopg2 import sql
from psycopg2 import extras
import time
from datetime import date
import bcrypt


# still being fixed
DB_CONFIG = {
    "host": "db.aeraqhjqallyybuttqpg.supabase.co",
    "database": "postgres",
    "user": "postgres",
    "password": "CS176_fitness176",
    "port": 5433
}


class DBConnector:
    def __init__(self):
        self.connection = None

    def connect(self, max_retries=5):
        for attempt in range(max_retries):
            try:
                # Use DSN parameters from the configuration dictionary
                self.connection = psycopg2.connect(**DB_CONFIG)
                print("Successfully connected to PostgreSQL database.")
                return True
            except psycopg2.Error as e:
                print(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    # Exponential backoff: 2^attempt seconds delay
                    wait_time = 2 ** attempt
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    print("Max retries reached. Could not connect to the database.")
                    return False
        return False

    def close(self):
        if self.connection:
            self.connection.close()
            print("PostgreSQL connection closed.")

    def init_db(self):
        """
        Initializes the database tables and constraints.
        Should be run once at app startup.
        """
        # Users table
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            UNIQUE(username)
        );
        """

        # Daily logs table
        create_daily_logs_table = """
        CREATE TABLE IF NOT EXISTS daily_logs (
            id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(user_id),
            log_date DATE NOT NULL,
            goal_points INT NOT NULL,
            earned_points INT NOT NULL DEFAULT 0,
            is_goal_met BOOLEAN NOT NULL DEFAULT FALSE,
            UNIQUE(user_id, log_date)
        );
        """

        # Execute table creation queries
        self.execute_query(create_users_table)
        self.execute_query(create_daily_logs_table)

        print("Database initialization complete.")

    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        """
        :param query: The SQL query string (should use %s placeholders).
        :param params: A tuple or list of parameters to substitute for placeholders.
        :param fetch_one: Boolean to fetch only one result row.
        :param fetch_all: Boolean to fetch all result rows.
        :return: None, a single row (tuple), or a list of rows (list of tuples).
        """
        if not self.connection:
            if not self.connect():
                return None
        
        try:
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute(query, params)

                # If the query modifies data
                if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP')):
                    self.connection.commit()

                    # If INSERT has RETURNING clause
                    if query.strip().upper().startswith('INSERT') and 'RETURNING' in query.upper():
                        return dict(cursor.fetchone()) if cursor.rowcount else None
                    # For UPDATE/DELETE, return number of affected rows
                    elif query.strip().upper().startswith(('UPDATE', 'DELETE')):
                        return cursor.rowcount

                # If fetching data
                if fetch_one:
                    return dict(cursor.fetchone()) if cursor.rowcount else None
                elif fetch_all:
                    return [dict(row) for row in cursor.fetchall()]

                # Default return for non-fetch queries without RETURNING
                return None
        
        except psycopg2.Error as e:
            print(f"Database error executing query: {e}")
            self.connection.rollback() 
            return None
        
    def signup(self, username, pw):
        hashed = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt())
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"        
        try:
            # fetch_one=True ensures it returns the inserted row
            user = self.execute_query(query, (username, hashed.decode('utf-8')), fetch_one=True)
            if user:
                print(f"User '{username}' registered successfully!")
                return user
            else:
                # Should not normally happen
                return False
        except psycopg2.IntegrityError:
            # Duplicate username or constraint violation
            if self.connection:
                self.connection.rollback()
            print("Signup failed: username already exists!")
            return False
        except psycopg2.Error as e:
            # Other database errors
            if self.connection:
                self.connection.rollback()
            print(f"Signup failed: {e}")
            return False
        
    def login(self, username, pw):
        """
        Authenticates a user and automatically creates a daily log with a goal.
        Goal starts at 1000 for the first log, then increases by 500 for each new day.
        """
        query = "SELECT * FROM users WHERE username = %s"
        user = self.execute_query(query, (username,), fetch_one=True)
        
        if user:
            stored_hash = user['password'].encode('utf-8')
            if bcrypt.checkpw(pw.encode('utf-8'), stored_hash):
                print(f"Login successful for user '{username}'!")
                
                today = date.today()
                log_check_query = """
                    SELECT * FROM daily_logs WHERE user_id = %s AND log_date = %s
                """
                log = self.execute_query(log_check_query, (user['user_id'], today), fetch_one=True)
                
                if not log:
                    # Get last goal_points
                    last_log_query = """
                        SELECT goal_points FROM daily_logs
                        WHERE user_id = %s
                        ORDER BY log_date DESC
                        LIMIT 1
                    """
                    last_log = self.execute_query(last_log_query, (user['user_id'],), fetch_one=True)

                    if last_log:
                        new_goal = last_log['goal_points'] + 500
                    else:
                        new_goal = 1000

                    # Insert new daily log
                    insert_log_query = """
                        INSERT INTO daily_logs 
                        (user_id, log_date, goal_points, earned_points, is_goal_met)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING id, user_id, log_date, goal_points, earned_points, is_goal_met
                    """
                    new_log = self.execute_query(
                        insert_log_query,
                        (user['user_id'], today, new_goal, 0, False),
                        fetch_one=True
                    )
                    print("Created new daily log for today:", new_log)

                return user['user_id']
            else:
                print("Login failed: Incorrect password.")
                return None
        else:
            print("Login failed: Username not found.")
            return None
        
    def add_points(self, id, points):
        """
        Adding points
        """
        query = "SELECT earned_points FROM daily_logs WHERE user_id = %s"
        current_score = self.execute_query(query, (id,), fetch_one=True)
        # user = self.execute_query(query, (username,), fetch_one=True)

        new_cmd = "UPDATE daily_logs SET earned_points = %s WHERE user_id = %s AND log_date = %s"
        update = self.execute_query(new_cmd, (current_score['earned_points'] + points, id, date.today()), fetch_one=True)
        print("updated:", update)
        
    
if __name__ == '__main__':

    # edit accordingly
    # this is just to test
    DB_CONFIG['host'] = 'localhost' 
    DB_CONFIG['user'] = 'postgres'
    DB_CONFIG['password'] = 'shaira'
    DB_CONFIG['port'] = 5433
    DB_CONFIG['database'] = 'workout_tracker'
    
    db = DBConnector()
    if db.connect():
        db.init_db() # initialize database if new app

        print(db.signup("macncheese2", "passpass"))
        print(db.login("macncheese2", "passpass"))
        the_user = db.login("macncheese", "passpass")
        db.add_points(the_user, 230)
        
        db.close()