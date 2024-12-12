-- Result set containing unique course names
SELECT DISTINCT name FROM Courses;

-- Result set containing Course Names and Professor Names that are related
SELECT c.name AS course_name, p.name AS professor_name
FROM Courses c
JOIN Professors p ON c.prof_id = p.id;

-- Result set containing Professors Names, Students Names and subsequent course names
SELECT p.name AS professor_name, s.name AS student_name, c.name AS course_name
FROM Classes cl
JOIN Courses c ON cl.course_id = c.id
JOIN Professors p ON c.prof_id = p.id
JOIN Students s ON cl.student_id = s.id;

-- Result set containing Number of students in each unique course
SELECT c.name AS course_name, COUNT(DISTINCT cl.student_id) AS student_count
FROM Classes cl
JOIN Courses c ON cl.course_id = c.id
GROUP BY c.name;

-- Result set containing Number of students in each individual course sections
SELECT c.name AS course_name, c.section, COUNT(DISTINCT cl.student_id) AS student_count
FROM Classes cl
JOIN Courses c ON cl.course_id = c.id
GROUP BY c.id, c.name, c.section;

-- Result set containing Total number of students under each professor
SELECT p.name AS professor_name, COUNT(DISTINCT cl.student_id) AS student_count
FROM Professors p
JOIN Courses c ON p.id = c.prof_id
JOIN Classes cl ON c.id = cl.course_id
GROUP BY p.name;

-- Result set containing course name and students name sorted by course name
SELECT c.name AS course_name, s.name AS student_name
FROM Classes cl
JOIN Courses c ON cl.course_id = c.id
JOIN Students s ON cl.student_id = s.id
ORDER BY c.name, s.name;

-- Result set containing all students whose name starts with A and the courses they have taken
SELECT s.name AS student_name, c.name AS course_name
FROM Classes cl
JOIN Students s ON cl.student_id = s.id
JOIN Courses c ON cl.course_id = c.id
WHERE s.name LIKE 'A%';
