import sqlite3
import os


def your_ID():
    # Return your ID here e.g. return "12220346" #########################################################
    return "12244668"
    ######################################################################################################


class DeathNoteDatabase:
    def create_connection(self, db_file):
        """Create a database connection to the SQLite database"""
        connection = None
        try:
            connection = sqlite3.connect(db_file)
            connection.text_factory = str
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
        return connection

    def create_tables(self, connection):
        # Create tables for the Death Note database ###############################################
        sql_characters = """
        CREATE TABLE IF NOT EXISTS Characters (
            character_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT,
            affiliation TEXT,
            is_human BOOLEAN
        );
        """

        sql_deaths = """
        CREATE TABLE IF NOT EXISTS Deaths (
            death_id INTEGER PRIMARY KEY AUTOINCREMENT,
            character_id INTEGER,
            cause_of_death TEXT,
            death_date DATE,
            kira_involved BOOLEAN,
            FOREIGN KEY (character_id) REFERENCES Characters (character_id)
        );
        """

        sql_ownership = """
        CREATE TABLE IF NOT EXISTS Ownership (
            ownership_id INTEGER PRIMARY KEY AUTOINCREMENT,
            character_id INTEGER,
            note_id INTEGER,
            start_date DATE,
            end_date DATE,
            FOREIGN KEY (character_id) REFERENCES Characters (character_id),
            FOREIGN KEY (note_id) REFERENCES Notes (note_id)
        );
        """

        sql_notes = """
        CREATE TABLE IF NOT EXISTS Notes (
            note_id INTEGER PRIMARY KEY AUTOINCREMENT,
            origin TEXT,
            current_location TEXT,
            is_active BOOLEAN
        );
        """

        sql_events = """
        CREATE TABLE IF NOT EXISTS Events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT,
            event_date DATE,
            location TEXT,
            description TEXT
        );
        """

        self.execute_query(connection, sql_characters)
        self.execute_query(connection, sql_deaths)
        self.execute_query(connection, sql_ownership)
        self.execute_query(connection, sql_notes)
        self.execute_query(connection, sql_events)

    def insert_data(self, connection):
        # Insert query to populate the Characters, Notes, Deaths, Ownership, and Events tables ######
        sql_characters = """
        INSERT INTO Characters (name, role, affiliation, is_human)
        VALUES (?, ?, ?, ?);
        """
        characters_data = [
            ("Light Yagami", "Kira", "Task Force", True),
            ("L", "Detective", "Task Force", True),
            ("Ryuk", "Shinigami", "Shinigami Realm", False),
            ("Misa Amane", "Kira", "Task Force", True),
            ("Near", "Detective", "SPK", True),
            ("Mello", "Detective", "Mafia", True),
            ("Rem", "Shinigami", "Shinigami Realm", False),
            ("Soichiro Yagami", "Task Force", "Task Force", True),
            ("Matsuda", "Detective", "Task Force", True),
            ("Teru Mikami", "Kira", "Kira Follower", True),
        ]

        sql_notes = """
        INSERT INTO Notes (origin, current_location, is_active)
        VALUES (?, ?, ?);
        """
        notes_data = [
            ("Shinigami Realm", "With Light Yagami", True),
            ("Shinigami Realm", "With Misa Amane", True),
            ("Shinigami Realm", "With Teru Mikami", True),
        ]

        sql_deaths = """
        INSERT INTO Deaths (character_id, cause_of_death, death_date, kira_involved)
        VALUES (?, ?, ?, ?);
        """
        deaths_data = [
            (2, "Heart Attack", "2007-11-05", True),
            (6, "Burned", "2007-11-07", False),
            (8, "Shot", "2007-10-25", False),
        ]

        sql_ownership = """
        INSERT INTO Ownership (character_id, note_id, start_date, end_date)
        VALUES (?, ?, ?, ?);
        """
        ownership_data = [
            (1, 1, "2003-01-01", "2006-11-05"),
            (3, 2, "2003-01-01", None),
            (4, 2, "2003-01-15", "2007-10-25"),
            (10, 3, "2006-12-01", "2007-12-01"),
        ]

        sql_events = """
        INSERT INTO Events (event_name, event_date, location, description)
        VALUES (?, ?, ?, ?);
        """
        events_data = [
            (
                "Light Meets Ryuk",
                "2003-01-01",
                "Light's House",
                "Light Yagami meets Ryuk for the first time.",
            ),
            (
                "Task Force Formed",
                "2004-02-10",
                "Tokyo",
                "The Task Force is officially formed to capture Kira.",
            ),
            ("L's Death", "2007-11-05", "Task Force HQ", "L is killed by Kira."),
            (
                "Final Confrontation",
                "2007-12-28",
                "Yellow Box Warehouse",
                "Near confronts Light in the final showdown.",
            ),
        ]

        # Insert all data into tables ############################################################
        self.execute_many(connection, sql_characters, characters_data)
        self.execute_many(connection, sql_notes, notes_data)
        self.execute_many(connection, sql_deaths, deaths_data)
        self.execute_many(connection, sql_ownership, ownership_data)
        self.execute_many(connection, sql_events, events_data)

    # Write your SQL query for each task below ######################################################
    def select_characters_and_roles(self, connection):
        # Write select query to list all characters and their respective roles #######################
        sql = """
        SELECT name, role 
        FROM Characters;
        """
        return self.execute_read_query(connection, sql)

    def select_deaths_and_characters(self, connection):
        # Write join query to list all deaths with character names ##################################
        sql = """
        SELECT C.name, D.cause_of_death, D.death_date 
        FROM Deaths D
        JOIN Characters C ON C.character_id = D.character_id;
        """
        return self.execute_read_query(connection, sql)

    def select_shinigami_with_notes(self, connection):
        # Write join query to find all Shinigami who have owned a Death Note #########################
        sql = """
        SELECT DISTINCT C.name 
        FROM Ownership O
        JOIN Characters C ON C.character_id = O.character_id
        WHERE C.is_human = 0;
        """
        return self.execute_read_query(connection, sql)

    def select_characters_and_roles(self, connection):
        # Write select query to list all characters and their respective roles #######################
        sql = """
        SELECT name, role 
        FROM Characters;
        """
        return self.execute_read_query(connection, sql)

    def select_deaths_and_characters(self, connection):
        # Write join query to list all deaths with character names ##################################
        sql = """
        SELECT C.name, D.cause_of_death, D.death_date 
        FROM Deaths D
        JOIN Characters C ON C.character_id = D.character_id;
        """
        return self.execute_read_query(connection, sql)

    def select_shinigami_with_notes(self, connection):
        # Write join query to find all Shinigami who have owned a Death Note #########################
        sql = """
        SELECT DISTINCT C.name 
        FROM Ownership O
        JOIN Characters C ON C.character_id = O.character_id
        WHERE C.is_human = 0;
        """
        return self.execute_read_query(connection, sql)

    def select_events_after_ls_death(self, connection):
        # Write select query to list all events that occurred after L's death ########################
        sql = """
        SELECT event_name, event_date, location 
        FROM Events
        WHERE event_date > (SELECT death_date FROM Deaths WHERE character_id = (SELECT character_id FROM Characters WHERE name = 'L'));
        """
        return self.execute_read_query(connection, sql)

    def select_current_owners_of_notes(self, connection):
        # Write join query to find the current owner of each Death Note ##############################
        sql = """
        SELECT DISTINCT C.name, N.note_id
        FROM Ownership O
        JOIN Characters C ON O.character_id = C.character_id
        JOIN Notes N ON N.note_id = O.note_id
        WHERE O.end_date IS NULL;
        """
        return self.execute_read_query(connection, sql)

    def count_deaths_by_kira(self, connection):
        # Write a query to count the number of deaths caused by Kira #################################
        sql = """
        SELECT COUNT(*) 
        FROM Deaths 
        WHERE kira_involved = 1;
        """
        return self.execute_read_query(connection, sql)

    def select_task_force_members(self, connection):
        # Write a query to list all characters who have been affiliated with the "Task Force" ########
        sql = """
        SELECT name 
        FROM Characters 
        WHERE affiliation = 'Task Force';
        """
        return self.execute_read_query(connection, sql)

    def count_active_death_notes(self, connection):
        # Write a query to find the total number of Death Notes that have been active ################
        sql = """
        SELECT COUNT(*) 
        FROM Notes 
        WHERE is_active = 1;
        """
        return self.execute_read_query(connection, sql)

    def select_notes_and_owners(self, connection):
        # Write a query to find all Death Notes along with the names of their current and past owners #
        sql = """
        SELECT O.note_id, C.name, O.start_date, O.end_date 
        FROM Ownership O
        JOIN Characters C ON O.character_id = C.character_id;
        """
        return self.execute_read_query(connection, sql)

    def calculate_avg_ownership_duration(self, connection):
        # Write a query to calculate the average duration of ownership of a Death Note ###############
        sql = """
        SELECT AVG(CASE 
        WHEN end_date IS NOT NULL 
        THEN (julianday(end_date) - julianday(start_date))
        ELSE (julianday('2024-10-17 07:02:14.75') - julianday(start_date))
        END) AS average_duration
        FROM Ownership;
        """
        return self.execute_read_query(connection, sql)

    def count_deaths_per_character(self, connection):
        # Write a query to list the characters and the number of deaths they are associated with #####
        sql = """
        SELECT C.name, COUNT(D.death_id) AS death_count 
        FROM Characters C
        LEFT JOIN Deaths D ON C.character_id = D.character_id
        GROUP BY C.character_id
        ORDER BY C.name ASC;
        """
        return self.execute_read_query(connection, sql)

    def select_characters_without_events(self, connection):
        # Write a query to find characters who were never involved in any events #####################
        sql = """
        SELECT C.name 
        FROM Characters C
        WHERE C.name NOT IN (
        SELECT DISTINCT C2.name
        FROM Characters C2
        INNER JOIN Events E
        ON E.event_name LIKE '%' || C2.name || '%'
        OR E.description LIKE '%' || C2.name || '%'
        );
        """

        return self.execute_read_query(connection, sql)

    def union_characters_and_events(self, connection):
        # Write a query to get all characters along with the events they were part of using a UNION ##
        sql = """
        SELECT E.event_name 
        FROM Events E
        JOIN Characters C ON E.event_name LIKE '%' || C.name || '%' 
        OR E.event_name LIKE '%Task Force%'
        UNION
        SELECT C.name 
        FROM Characters C;
        """
        return self.execute_read_query(connection, sql)

    def count_ownership_per_character(self, connection):
        # Write a query to list the number of times each character was an owner of a Death Note ######
        sql = """
        SELECT C.name, COUNT(O.note_id) AS ownership_count 
        FROM Characters C
        LEFT JOIN Ownership O ON C.character_id = O.character_id
        GROUP BY C.character_id
        HAVING COUNT(O.note_id) > 0;
        """
        return self.execute_read_query(connection, sql)

    def count_characters_per_note(self, connection):
        # Write a query to get a list of all Death Notes and the number of characters who owned them #
        sql = """
        SELECT N.note_id, COUNT(O.character_id) AS owner_count 
        FROM Notes N
        LEFT JOIN Ownership O ON N.note_id = O.note_id
        GROUP BY N.note_id;
        """
        return self.execute_read_query(connection, sql)

    def select_tokyo_events_with_characters(self, connection):
        # Write a query to list all events that took place in "Tokyo" along with character names #####
        sql = """
        SELECT E.event_name, C.name 
        FROM Events E
        JOIN Characters C ON E.description LIKE '%' || C.name || '%'
        WHERE E.location = 'Tokyo';
        """
        return self.execute_read_query(connection, sql)

    def select_characters_without_ownership(self, connection):
        # Write a query to find the characters who have never owned a Death Note #####################
        sql = """
        SELECT C.name 
        FROM Characters C
        WHERE C.character_id NOT IN (
            SELECT DISTINCT character_id 
            FROM Ownership
        );
        """
        return self.execute_read_query(connection, sql)

    def most_frequent_note_owner(self, connection):
        # Write a complex query to find which character has owned the most Death Notes ##############
        sql = """
        SELECT C.name, COUNT(O.note_id) AS ownership_count 
        FROM Ownership O
        JOIN Characters C ON O.character_id = C.character_id
        GROUP BY O.character_id
        ORDER BY ownership_count DESC 
        LIMIT 1;
        """
        return self.execute_read_query(connection, sql)

    def select_non_kira_deaths(self, connection):
        # Write a query to find all deaths that were not caused by Kira #############################
        sql = """
        SELECT C.name, D.cause_of_death
        FROM Deaths D
        JOIN Characters C ON C.character_id = D.character_id
        WHERE D.kira_involved = 0;
        """
        return self.execute_read_query(connection, sql)

    def select_characters_before_and_after_ls_death(self, connection):
        # Write a query to list all characters who were involved in events before and after L's death
        sql = """
        WITH L_death_event AS (
            SELECT event_date
            FROM Events
            WHERE event_name = "L's Death"
        ),
        events_before_after AS (
            SELECT *
            FROM Events
            WHERE event_date < (SELECT event_date FROM L_death_event)
            OR event_date > (SELECT event_date FROM L_death_event)
        )
        SELECT DISTINCT c.name
        FROM Characters c
        JOIN events_before_after e
        ON (e.event_name LIKE '%' || c.name || '%'
        OR e.description LIKE '%' || c.name || '%')
        WHERE c.name != "L";
        """
        return self.execute_read_query(connection, sql)

    #################################################################################################################
    ####### XXXXXXXXXXX !!!DO NOT MODIFY THIS SECTION!!! XXXXXXXXXXX ######################
    #################################################################################################################

    def execute_query(self, connection, sql):
        """Execute a write query (INSERT, UPDATE, DELETE) and return a success message"""
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            connection.commit()
            return f"Query executed successfully. Rows affected: {cursor.rowcount}"
        except sqlite3.Error as e:
            return f"Error occurred: {e}"

    def execute_many(self, connection, sql, data):
        """Execute multiple insertions into a table"""
        cursor = connection.cursor()
        try:
            cursor.executemany(sql, data)
            connection.commit()
            return f"Data inserted successfully. Rows affected: {cursor.rowcount}"
        except sqlite3.Error as e:
            return f"Error inserting data: {e}"

    def execute_read_query(self, connection, sql):
        """Execute a read query (SELECT) and return the results"""
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            return f"Query executed successfully. Rows fetched: {len(results)}", results
        except sqlite3.Error as e:
            return f"Error occurred: {e}", None


def main(x=0):
    db = DeathNoteDatabase()
    """ Main function to run all queries and display the results """
    db_file = "death_note.db"
    conn = db.create_connection(db_file)
    output = []
    final_output = (your_ID(),)

    if conn:
        db.create_tables(conn)
        db.insert_data(conn)
        output.append(db.select_characters_and_roles(conn))
        output.append(db.select_deaths_and_characters(conn))
        output.append(db.select_shinigami_with_notes(conn))
        output.append(db.select_events_after_ls_death(conn))
        output.append(db.select_current_owners_of_notes(conn))
        output.append(db.count_deaths_by_kira(conn))
        output.append(db.select_task_force_members(conn))
        output.append(db.count_active_death_notes(conn))
        output.append(db.select_notes_and_owners(conn))
        output.append(db.calculate_avg_ownership_duration(conn))
        output.append(db.count_deaths_per_character(conn))
        output.append(db.select_characters_without_events(conn))
        output.append(db.union_characters_and_events(conn))
        output.append(db.count_ownership_per_character(conn))
        output.append(db.count_characters_per_note(conn))
        output.append(db.select_tokyo_events_with_characters(conn))
        output.append(db.select_characters_without_ownership(conn))
        output.append(db.most_frequent_note_owner(conn))
        output.append(db.select_non_kira_deaths(conn))
        output.append(db.select_characters_before_and_after_ls_death(conn))
        conn.close()

        # Delete the database file after all queries are executed
        if os.path.exists(db_file):
            os.remove(db_file)

    # Display the output of each query
    for idx, result in enumerate(output, start=1):
        if isinstance(result, tuple):
            # If it's a read query with results
            final_output += (f"Query {idx}: {result[0]}",)
            for row in result[1]:
                final_output += (row,)
        else:
            final_output += (f"Query {idx}: {result}",)

    for row in final_output[1:]:
        print(row)
    return final_output


if __name__ == "__main__":
    main()

#################################################################################################################
####### XXXXXXXXXXX !!!DO NOT MODIFY THIS SECTION!!! XXXXXXXXXXX ######################
#################################################################################################################
