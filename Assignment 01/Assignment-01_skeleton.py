import sqlite3
import os

def your_ID():
    # Return your ID here e.g. return "12220346" #########################################################
    return "12244668"
    ######################################################################################################

class EPLDatabase:
    def create_connection(self, db_file):
        """ Create a database connection to the SQLite database """
        connection = None
        try:
            connection = sqlite3.connect(db_file)
            connection.text_factory = str
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
        return connection

    def create_table(self, connection):
        # Create table query for the 'EPL' table ####################################################
        sql = """
        CREATE TABLE IF NOT EXISTS EPL (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_name TEXT NOT NULL,
            played INTEGER,
            won INTEGER,
            drawn INTEGER,
            lost INTEGER,
            goals_for INTEGER,
            goals_against INTEGER,
            goal_difference INTEGER,
            points INTEGER
        );
        """
        output = self.execute_query(connection, sql)
        return output

    def insert_data(self, connection):
        # 1. Write insert query to insert the data variable in the abovementioned table #######################
        sql = "INSERT INTO EPL (team_name, played, won, drawn, lost, goals_for, goals_against, goal_difference, points) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        #######################################################################################################
        data = [
            ("Manchester City", 38, 28, 5, 5, 99, 26, 73, 89),
            ("Liverpool", 38, 27, 8, 3, 94, 26, 68, 89),
            ("Chelsea", 38, 21, 10, 7, 76, 33, 43, 73),
            ("Tottenham", 38, 22, 5, 11, 69, 39, 30, 71),
            ("Arsenal", 38, 19, 9, 10, 61, 48, 13, 66),
            ("Manchester United", 38, 16, 10, 12, 57, 57, 0, 58),
            ("West Ham", 38, 16, 8, 14, 60, 51, 9, 56),
            ("Leicester City", 38, 14, 10, 14, 62, 59, 3, 52),
            ("Brighton", 38, 12, 15, 11, 42, 44, -2, 51),
            ("Wolves", 38, 12, 6, 20, 38, 57, -19, 42),
            ("Newcastle United", 38, 13, 10, 15, 44, 62, -18, 49),
            ("Crystal Palace", 38, 11, 16, 11, 50, 46, 4, 49),
            ("Brentford", 38, 13, 7, 18, 48, 56, -8, 46),
            ("Aston Villa", 38, 13, 6, 19, 52, 54, -2, 45),
            ("Southampton", 38, 9, 13, 16, 43, 67, -24, 40),
            ("Everton", 38, 11, 6, 21, 43, 66, -23, 39),
            ("Leeds United", 38, 9, 11, 18, 42, 79, -37, 38),
            ("Burnley", 38, 7, 14, 17, 34, 53, -19, 35),
            ("Watford", 38, 6, 5, 27, 34, 77, -43, 23),
            ("Norwich City", 38, 5, 7, 26, 23, 84, -61, 22)
        ]
        try:
            cursor = connection.cursor()
            cursor.executemany(sql, data)
            connection.commit()
            output = f"Data inserted successfully. Rows affected: {cursor.rowcount}"
        except sqlite3.Error as e:
            output = f"Error inserting data: {e}"
        return output

    def select_all(self, connection):
        # 2. Write select query to fetch all columns from the 'EPL' table #####################################
        sql = "SELECT * FROM EPL"
        #######################################################################################################
        return self.execute_read_query(connection, sql)

    def select_distinct_wins(self, connection):
        # 3. Write select distinct query to fetch unique values of the 'won' column ############################
        sql = "SELECT DISTINCT won FROM EPL;"
        ########################################################################################################
        return self.execute_read_query(connection, sql)

    def select_won_and_goal_difference(self, connection):
        # 4. Write select query to find teams with more than 20 wins and goal difference greater than 50 #######
        sql = "SELECT team_name FROM EPL WHERE won > 20 AND goal_difference > 50;"
        ########################################################################################################
        return self.execute_read_query(connection, sql)

    def select_draw_or_low_points(self, connection):
        # 5. Write select query to find teams with more than 10 draws OR less than 60 points ###################
        sql = "SELECT team_name FROM EPL WHERE drawn > 10 OR points < 60;"
        ########################################################################################################
        return self.execute_read_query(connection, sql)

    def select_no_losses(self, connection):
        # 6. Write select query to find teams that have not lost any matches ###################################
        sql = "SELECT * FROM EPL WHERE lost = 0;"
        ########################################################################################################
        return self.execute_read_query(connection, sql)

    def update_points(self, connection):
        # 7. Write update query to change points of 'Manchester United' to 60 ##################################
        sql = "UPDATE EPL SET points = 60 WHERE team_name = 'Manchester United'"
        ########################################################################################################
        return self.execute_query(connection, sql)

    def delete_low_points(self, connection):
        # 8. Write delete query to remove records of teams with less than 40 points ############################
        sql = "DELETE FROM EPL WHERE points < 40;"
        ########################################################################################################
        return self.execute_query(connection, sql)

    def select_top_teams(self, connection):
        # 9. Write select query to fetch the top 3 teams based on points #######################################
        sql = "SELECT team_name, points FROM EPL ORDER BY points DESC LIMIT 3;"
        ########################################################################################################
        return self.execute_read_query(connection, sql)

    def select_max_goals(self, connection):
        # 10. Write select query to find the team with the maximum number of goals scored #######################
        sql = "SELECT team_name FROM EPL WHERE goals_for = (SELECT MAX(goals_for) FROM EPL)"
        ########################################################################################################
        return self.execute_read_query(connection, sql)

    def select_average_points(self, connection):
        # 11. Write select query to calculate the average number of points in the EPL ###########################
        sql = "SELECT AVG(points) FROM EPL"
        ########################################################################################################
        return self.execute_read_query(connection, sql)




#################################################################################################################
####### XXXXXXXXXXX !!!DO NOT MODIFY THIS SECTION!!! XXXXXXXXXXX ######################
#################################################################################################################

    def execute_query(self, connection, sql):
        """ Execute a write query (INSERT, UPDATE, DELETE) and return a success message """
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            connection.commit()
            return f"Query executed successfully. Rows affected: {cursor.rowcount}"
        except sqlite3.Error as e:
            return f"Error occurred: {e}"

    def execute_read_query(self, connection, sql):
        """ Execute a read query (SELECT) and return the results """
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            return f"Query executed successfully. Rows fetched: {len(results)}", results
        except sqlite3.Error as e:
            return f"Error occurred: {e}", None

def main(x=0):
    db = EPLDatabase()
    """ Main function to run all queries and display the results """
    db_file = "epl_database.db"
    conn = db.create_connection(db_file)
    output = []
    final_output = (your_ID(),)

    if conn:
        db.create_table(conn)
        output.append(db.insert_data(conn))
        output.append(db.select_all(conn))
        output.append(db.select_distinct_wins(conn))
        output.append(db.select_won_and_goal_difference(conn))
        output.append(db.select_draw_or_low_points(conn))
        output.append(db.select_no_losses(conn))
        output.append(db.update_points(conn))
        output.append(db.delete_low_points(conn))
        output.append(db.select_top_teams(conn))
        output.append(db.select_max_goals(conn))
        output.append(db.select_average_points(conn))
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