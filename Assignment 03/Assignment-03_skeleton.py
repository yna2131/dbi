########################### DO NOT MODIFY THIS SECTION ##########################
#################################################################################
import sqlite3
from sqlite3 import Error
import csv

#################################################################################

######################################################################


class A3_sql:
    ############### DO NOT MODIFY THIS SECTION ###########################
    ######################################################################
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))

        return connection

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            if query == "":
                return "Query Blank"
            else:
                cursor.execute(query)
                connection.commit()
                return "Query executed successfully"
        except Error as e:
            return "Error occurred: " + str(e)

    def import_data(self, connection, path):
        with open(path, encoding="utf8") as f:
            reader = csv.reader(f)
            movielist = list(reader)
            for movie in movielist:
                # print(movie)
                connection.execute(
                    "INSERT INTO movies VALUES (?,?,?)", (movie[0], movie[1], movie[2])
                )

        sql = "SELECT COUNT(id) FROM movies;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    def import_data2(self, connection, path):
        ############### CREATE IMPORT CODE BELOW ############################
        with open(path, encoding="utf8") as f:
            reader = csv.reader(f)
            cast_list = list(reader)
            for cast in cast_list:
                # print(movie)
                connection.execute(
                    "INSERT INTO movie_cast VALUES (?,?,?,?,?)",
                    (cast[0], cast[1], cast[2], cast[3], cast[4]),
                )
        ######################################################################

        sql = "SELECT COUNT(cast_id) FROM movie_cast;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    ######################################################################
    ######################################################################

    # Part a InhaID [1 point]
    def InhaID(self):
        return "12244668"

    # Part b createTable_1 [2 points]
    def createTable_1(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_sql = """CREATE TABLE movies (
                        id int,
                        title text,
                        score real
                        );"""
        ######################################################################

        return self.execute_query(connection, part_b_sql)

    # Part c createTable_2 [2 points]
    def createTable_2(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_c_sql = """CREATE TABLE movie_cast(
                        movie_id int,
                        cast_id int,
                        cast_name text,
                        birthday text,
                        popularity real
                        );"""
        ######################################################################

        return self.execute_query(connection, part_c_sql)

    # Part d_1 createIndex_1 [1 points]
    def createIndex_1(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_d_1_sql = "CREATE INDEX movie_index ON movies (id);"
        ######################################################################
        return self.execute_query(connection, part_d_1_sql)

    # Part d_2 createIndex_2 [1 points]
    def createIndex_2(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_d_2_sql = "CREATE INDEX cast_index ON movie_cast (cast_id);"
        ######################################################################
        return self.execute_query(connection, part_d_2_sql)

    # Part e calcProportion [3 points]
    def calcProportion(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_e_sql = """SELECT ROUND(
                        (CAST(COUNT(*) AS FLOAT) / (SELECT COUNT(*) FROM movies)) * 100, 2)
                        FROM movies
                        WHERE score BETWEEN 7 AND 20;"""
        ######################################################################
        cursor = connection.execute(part_e_sql)
        return cursor.fetchall()[0][0]

    # Part f prolificActors [5 points]
    def prolificActors(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_f_sql = """SELECT cast_name, COUNT(movie_id) AS appearance_count
                        FROM movie_cast
                        WHERE popularity > 10
                        GROUP BY cast_name
                        ORDER BY appearance_count DESC, cast_name ASC
                        LIMIT 5;"""
        ######################################################################
        cursor = connection.execute(part_f_sql)
        return cursor.fetchall()

    # Part g highScoringMovie [5 points]
    def highScoringMovie(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_g_sql = """SELECT m.title AS movie_title, ROUND(m.score, 2) AS score, COUNT(mc.cast_id) AS cast_count
                        FROM movies m
                        JOIN movie_cast mc ON m.id = mc.movie_id
                        GROUP BY m.id
                        ORDER BY score DESC, cast_count ASC, movie_title ASC
                        LIMIT 5;"""
        ######################################################################
        cursor = connection.execute(part_g_sql)
        return cursor.fetchall()

    # Part h highScoringActor [5 points]
    def highScoringActor(self, connection):
        ############### EDIT SQL STATEMENT ###################################
        part_h_sql = """SELECT mc.cast_id, mc.cast_name, ROUND(AVG(m.score), 2) AS average_score
                        FROM movies m
                        JOIN movie_cast mc ON m.id = mc.movie_id
                        WHERE m.score >= 25
                        GROUP BY mc.cast_id, mc.cast_name
                        HAVING COUNT(m.id) >= 3
                        ORDER BY average_score DESC, cast_name ASC
                        LIMIT 10;"""
        ######################################################################
        cursor = connection.execute(part_h_sql)
        return cursor.fetchall()


########################### DO NOT MODIFY THIS SECTION ##########################
#################################################################################
def main(x=0):
    db = A3_sql()
    output = ()

    try:
        conn = db.create_connection("A3")
    except:
        output += ("Database Creation Error",)

    try:
        conn.execute("DROP TABLE IF EXISTS movies;")
        conn.execute("DROP TABLE IF EXISTS movie_cast;")
        conn.execute("DROP TABLE IF EXISTS cast_bio;")
        conn.execute("DROP VIEW IF EXISTS good_collaboration;")
        conn.execute("DROP TABLE IF EXISTS movie_overview;")
    except Exception as e:
        output += ("Error in Table Drops", str(e))

    try:
        stu_id = db.InhaID()
        if stu_id == "Write your ID here":
            output += ("Error in Part a",)
        else:
            output += (f"part a: {stu_id}",)
    except Exception as e:
        output += ("Error in Part a", str(e))

    try:
        output += (f"part b: {db.createTable_1(conn)}",)
    except Exception as e:
        output += ("Error in Part b", str(e))

    try:
        output += (f"part c: {db.createTable_2(conn)}",)
    except Exception as e:
        output += ("Error in Part c", str(e))

    try:
        row_count_movies = db.import_data(conn, "data/movies.csv")
        row_count_cast = db.import_data2(conn, "data/movie_cast.csv")
        output += (f"Row count for Movies Table: {row_count_movies}",)
        output += (f"Row count for Movie Cast Table: {row_count_cast}",)
    except Exception as e:
        output += ("Error in importing data", str(e))

    try:
        output += (f"part d 1: {db.createIndex_1(conn)}",)
        output += (f"part d 2: {db.createIndex_2(conn)}",)
    except Exception as e:
        output += ("Error in part d", str(e))

    try:
        output += (f"part e: {db.calcProportion(conn)}",)
    except Exception as e:
        output += ("Error in part e", str(e))

    try:
        output += ("part f:",)
        for line in db.prolificActors(conn):
            output += (f"{line[0]} {line[1]}",)
    except Exception as e:
        output += ("Error in part f", str(e))

    try:
        output += ("part g:",)
        for line in db.highScoringMovie(conn):
            output += (f"{line[0]} {line[1]} {line[2]}",)
    except Exception as e:
        output += ("Error in part g", str(e))

    try:
        output += ("part h:",)
        for line in db.highScoringActor(conn):
            output += (f"{line[0]} {line[1]} {line[2]}",)
    except Exception as e:
        output += ("Error in part h", str(e))

    conn.close()

    # Print the final output tuple
    for line in output:
        print(line)

    conn.close()
    return output


if __name__ == "__main__":
    main()

#################################################################################
#################################################################################
