CREATE TABLE missions (
    mission_id INTEGER PRIMARY KEY, 
    mission_name TEXT NOT NULL, 
    launch_date DATE, 
    mission_type TEXT
);

CREATE TABLE astronauts (
    astronaut_id INTEGER PRIMARY KEY, 
    astronaut_name TEXT NOT NULL, 
    birth_date DATE, 
    nationality TEXT, 
    missions_participated INTEGER DEFAULT 0
);

CREATE TABLE planets (
    planet_id INTEGER PRIMARY KEY, 
    planet_name TEXT NOT NULL, 
    distance_from_earth REAL NOT NULL, 
    discovered BOOLEAN DEFAULT FALSE
);

CREATE TABLE discoveries (
    discovery_id INTEGER PRIMARY KEY, 
    mission_id INTEGER, 
    discovery_name TEXT NOT NULL, 
    discovery_date DATE, 
    significance_level TEXT, 
    FOREIGN KEY (mission_id) REFERENCES missions(mission_id) ON DELETE CASCADE
);

CREATE TABLE crew_assignments (
    assignment_id INTEGER PRIMARY KEY, 
    mission_id INTEGER, 
    astronaut_id INTEGER, 
    role TEXT NOT NULL, 
    FOREIGN KEY (mission_id) REFERENCES missions(mission_id) ON DELETE CASCADE,
    FOREIGN KEY (astronaut_id) REFERENCES astronauts(astronaut_id) ON DELETE CASCADE
);

INSERT INTO missions (mission_id, mission_name, launch_date, mission_type) VALUES
(1, 'Apollo 11', '1969-07-16', 'Exploration'),
(2, 'Voyager 1', '1977-09-05', 'Research'),
(3, 'Mars Rover 2020', '2020-07-30', 'Exploration'),
(4, 'Hubble Deployment', '1990-04-24', 'Satellite Deployment'),
(5, 'Lunar Reconnaissance Orbiter', '2009-06-18', 'Exploration'),
(6, 'Cassini-Huygens', '1997-10-15', 'Research'),
(7, 'Galileo Probe', '1989-10-18', 'Exploration'),
(8, 'SpaceX Crew-1', '2020-11-15', 'Exploration'),
(9, 'James Webb Telescope', '2021-12-25', 'Satellite Deployment'),
(10, 'Viking 1', '1975-08-20', 'Research');

INSERT INTO astronauts (astronaut_id, astronaut_name, birth_date, nationality, missions_participated) VALUES
(1, 'Neil Armstrong', '1930-08-05', 'American', 2),
(2, 'Buzz Aldrin', '1930-01-20', 'American', 2),
(3, 'Yuri Gagarin', '1934-03-09', 'Russian', 1),
(4, 'Chris Hadfield', '1959-08-29', 'Canadian', 3),
(5, 'Peggy Whitson', '1960-02-09', 'American', 10),
(6, 'Sally Ride', '1951-05-26', 'American', 2),
(7, 'Tim Peake', '1972-04-07', 'British', 1),
(8, 'Mae Jemison', '1956-10-17', 'American', 1),
(9, 'Valentina Tereshkova', '1937-03-06', 'Russian', 1),
(10, 'John Glenn', '1921-07-18', 'American', 2);

INSERT INTO planets (planet_id, planet_name, distance_from_earth, discovered) VALUES
(1, 'Mars', 78.0, TRUE),
(2, 'Venus', 41.0, TRUE),
(3, 'Jupiter', 588.0, TRUE),
(4, 'Saturn', 1207.0, TRUE),
(5, 'Mercury', 77.3, TRUE),
(6, 'Uranus', 2581.0, FALSE),
(7, 'Neptune', 4347.0, FALSE),
(8, 'Pluto', 5913.0, FALSE),
(9, 'Europa', 628.3, TRUE),
(10, 'Titan', 1221.0, TRUE);

INSERT INTO discoveries (discovery_id, mission_id, discovery_name, discovery_date, significance_level) VALUES
(1, 1, 'Lunar Surface Composition', '1969-07-21', 'High'),
(2, 3, 'Perseverance Landing', '2021-02-18', 'High'),
(3, 2, 'Interstellar Medium', '1990-08-25', 'High'),
(4, 4, 'Hubble’s Deep Field Images', '1995-12-18', 'High'),
(5, 6, 'Saturn’s Rings Structure', '2004-07-01', 'Medium'),
(6, 8, 'SpaceX Dragon Docking', '2020-11-17', 'Medium'),
(7, 5, 'Mapping Lunar Craters', '2009-09-15', 'Medium'),
(8, 9, 'Infrared Universe Views', '2022-07-12', 'High'),
(9, 10, 'Mars Soil Analysis', '1976-07-20', 'High'),
(10, 7, 'Galilean Moons of Jupiter', '1995-12-07', 'High');

INSERT INTO crew_assignments (assignment_id, mission_id, astronaut_id, role) VALUES
(1, 1, 1, 'Commander'),
(2, 1, 2, 'Pilot'),
(3, 8, 4, 'Commander'),
(4, 8, 5, 'Scientist'),
(5, 6, 9, 'Engineer'),
(6, 5, 6, 'Scientist'),
(7, 7, 3, 'Commander'),
(8, 3, 7, 'Scientist'),
(9, 4, 8, 'Engineer'),
(10, 10, 10, 'Commander');

--- 1. Basic Retrieval ---
--- Write a query to list all missions launched after January 1, 2010
--- Include the mission_name and launch_date in the result
SELECT mission_name, launch_date 
FROM missions 
WHERE launch_date > '2010-01-01';
---
--- 2. Working with DISTINCT ---
--- Write a query to find distinct mission types in the missions table
--- Sort the mission types in alphabetical order
SELECT DISTINCT mission_type
FROM missions
ORDER BY mission_type ASC;
---
--- 3. Filtering with WHERE ---
--- Write a query to list all astronauts who are born after January 1, 1980
--- Include their astronaut_name and birth_date
SELECT astronaut_name, birth_date 
FROM astronauts 
WHERE birth_date > '1980-01-01';
---
--- 4. Using Aggregation ---
--- Write a query to find the average number of missions participated in by astronauts
--- Round the result to 2 decimal places
SELECT ROUND(AVG(missions_participated), 2) AS average_missions 
FROM astronauts;
---
--- 5. JOIN Operations ---
--- Write a query to list all missions along with the names of astronauts assigned to them
--- Use an INNER JOIN between missions and crew_assignments on mission_id
SELECT m.mission_name, a.astronaut_name 
FROM missions m 
INNER JOIN crew_assignments ca ON m.mission_id = ca.mission_id 
INNER JOIN astronauts a ON ca.astronaut_id = a.astronaut_id;
---
--- 6. Using GROUP BY ---
--- Write a query to find the number of missions each astronaut has been assigned to
--- List the astronaut_name and the count of mission_id
--- Order the result by the count in descending order
SELECT a.astronaut_name, COUNT(ca.mission_id) AS mission_count 
FROM astronauts a 
INNER JOIN crew_assignments ca ON a.astronaut_id = ca.astronaut_id 
GROUP BY a.astronaut_name 
ORDER BY mission_count DESC;
---
--- 7. HAVING Clause ---
--- Write a query to find astronauts who have participated in more than 2 missions
--- List their astronaut_name and the number of missions
SELECT astronaut_name, missions_participated
FROM astronauts
WHERE missions_participated > 2;
---
--- 8. Subqueries ---
--- Write a query to find the mission with the longest distnace target in the planets table
--- Use a subquery to find the maximum distnace
SELECT planet_name, distance_from_earth
FROM planets
WHERE distance_from_earth = (
    SELECT MAX(distance_from_earth)
    FROM planets
);
---
--- 9. Using LIKE for Pattern Matching ---
--- Write a query to find all missions whose names start with 'Apollo'
--- Sort the results by mission_name
SELECT mission_name 
FROM missions 
WHERE mission_name LIKE 'Apollo%' 
ORDER BY mission_name;
---
--- 10. Combining Data with UNION ---
--- Write two queries: one to list all astronaut_name from astronauts and another to list all planet_name from planets
--- Use a UNION to combine these results into a single list
SELECT astronaut_name AS name 
FROM astronauts 
UNION 
SELECT planet_name AS name 
FROM planets;
---
--- 11. JOIN with Filtering ---
--- Write a query to list all missions that have discoveries with a 'High' significance level
--- Include the mission_name and discovery_name
SELECT m.mission_name, d.discovery_name 
FROM missions m 
INNER JOIN discoveries d ON m.mission_id = d.mission_id 
WHERE d.significance_level = 'High';
---
--- 12. Nested Subqueries ---
--- Write a qeury to find astronauts who have participated in missions targeting planets closer than 100 million kilometers
--- Include their astronaut_name and the planet_name
SELECT a.astronaut_name, p.planet_name 
FROM astronauts a
INNER JOIN crew_assignments ca ON a.astronaut_id = ca.astronaut_id
INNER JOIN missions m ON ca.mission_id = m.mission_id
INNER JOIN planets p ON p.distance_from_earth < 100;
---
--- 13. Date Filtering ---
--- Write a query to list all astronauts whose birthdays fall in the month of December
--- Include their astronaut_name and birth_date
SELECT astronaut_name, birth_date 
FROM astronauts 
WHERE MONTH(birth_date) = 12;
---
--- 14. Ordering with Multiple Columns
--- Write a qeury to list all missions sorted first by launch_date (ascending) and then by mission_name (alphabetical)
SELECT mission_name, launch_date 
FROM missions 
ORDER BY launch_date ASC, mission_name ASC;
---
--- 15. Calculating Percentages ---
--- Write a qeury yo calculate the percentage of planets that have been discovered
--- Use ROUND to round the percentage to 2 decimal places
SELECT ROUND(
    (CAST(SUM(CASE WHEN discovered = TRUE THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*)) * 100, 
    2
) AS discovered_percentage 
FROM planets;
---
--- 16. Complex JOINs ---
--- Write a query to list each astronaut along with the names of all missions they have been part of 
--- Include the astronaut_name and mission_name, sorted by astronaut_name
SELECT a.astronaut_name, m.mission_name 
FROM astronauts a
INNER JOIN crew_assignments ca ON a.astronaut_id = ca.astronaut_id
INNER JOIN missions m ON ca.mission_id = m.mission_id
ORDER BY a.astronaut_name;
---
--- 17. Finding Top Performers
--- Write a qeury to find the top 5 astronauts with the highest number of mission participations
--- List their astronaut_name and missions_participated
SELECT astronaut_name, missions_participated 
FROM astronauts 
ORDER BY missions_participated DESC 
LIMIT 5;
---
--- 18. Using CASE Statements ---
--- Write a query to classify planets into three categories based on their distnace from Earth:
--- -- 'Nearby' if distance_from_earth < 50
--- -- 'Moderate' if distnace_from_earth is between 50 and 150 (inclusive)
--- -- 'Far' if distance_from_earth > 150
--- Include the planet_name and the category in the result
SELECT planet_name,
    CASE 
        WHEN distance_from_earth < 50 THEN 'Nearby'
        WHEN distance_from_earth BETWEEN 50 AND 150 THEN 'Moderate'
        ELSE 'Far'
    END AS distance_category
FROM planets;
---
--- 19. Dealing with NULL Values ---
--- Write a query to find all discoveries that do not have a specified discovery_date
--- Include the discovery_name in the result
SELECT discovery_name 
FROM discoveries 
WHERE discovery_date IS NULL;
---
--- 20. Combining Complex Conditions ---
--- Write a query to list all missions that have been assigned to more than 5 astronauts and have made a 'High' significance discovery
--- Use a HAVING clause to filter based on the number of crew members
SELECT m.mission_name 
FROM missions m
INNER JOIN crew_assignments ca ON m.mission_id = ca.mission_id
INNER JOIN discoveries d ON m.mission_id = d.mission_id
GROUP BY m.mission_id, m.mission_name, d.significance_level
HAVING COUNT(ca.astronaut_id) > 5 AND d.significance_level = 'High';