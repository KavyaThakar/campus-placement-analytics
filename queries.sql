-- ============================================================================
-- queries.sql
-- Multi-Degree Campus Placement Analytics - Analytical SQL Query Suite
-- Target Database: placement.db | Table: students
-- ============================================================================

-- Query 1: Overall Placement Overview across All Degree Programs
SELECT 
    COUNT(*) AS total_students,
    SUM(Placed_Flag) AS total_placed,
    COUNT(*) - SUM(Placed_Flag) AS total_unplaced,
    ROUND(AVG(Placed_Flag) * 100, 2) AS placement_rate_pct
FROM students;

-- Query 2: Placement Rate by Degree Field (B.Tech, M.Tech, MCA, BCA, Pharmacy, MBA, etc.)
SELECT 
    degree_t AS degree_field,
    COUNT(*) AS total_students,
    SUM(Placed_Flag) AS placed_students,
    ROUND(AVG(Placed_Flag) * 100, 2) AS placement_rate_pct
FROM students
GROUP BY degree_t
ORDER BY placement_rate_pct DESC;

-- Query 3: Placement Rate by Specialisation / Branch
SELECT 
    specialisation,
    COUNT(*) AS total_students,
    SUM(Placed_Flag) AS placed_students,
    ROUND(AVG(Placed_Flag) * 100, 2) AS placement_rate_pct
FROM students
GROUP BY specialisation
ORDER BY placement_rate_pct DESC;

-- Query 4: Salary Statistics by Specialisation (Placed Only)
SELECT 
    specialisation,
    COUNT(*) AS placed_count,
    ROUND(AVG(salary), 2) AS avg_salary,
    MIN(salary) AS min_salary,
    MAX(salary) AS max_salary
FROM students
WHERE status = 'Placed'
GROUP BY specialisation
ORDER BY avg_salary DESC;

-- Query 5: Window Function - Rank Students by Score within Degree Field
SELECT 
    student_id,
    gender,
    degree_t,
    specialisation,
    mba_p AS final_score_p,
    status,
    salary,
    RANK() OVER (PARTITION BY degree_t ORDER BY mba_p DESC) AS rank_within_degree
FROM students
ORDER BY degree_t, rank_within_degree
LIMIT 20;

-- Query 6: CTE - Academic Scores Comparison (Placed vs Unplaced)
WITH AcademicAverages AS (
    SELECT 
        status,
        COUNT(*) AS student_count,
        ROUND(AVG(ssc_p), 2) AS avg_ssc_p,
        ROUND(AVG(hsc_p), 2) AS avg_hsc_p,
        ROUND(AVG(degree_p), 2) AS avg_degree_p,
        ROUND(AVG(mba_p), 2) AS avg_final_p,
        ROUND(AVG(etest_p), 2) AS avg_etest_p
    FROM students
    GROUP BY status
)
SELECT 
    status,
    student_count,
    avg_ssc_p,
    avg_hsc_p,
    avg_degree_p,
    avg_final_p,
    avg_etest_p
FROM AcademicAverages;

-- Query 7: Placement Rate by Prior Work Experience
SELECT 
    workex,
    COUNT(*) AS total_students,
    SUM(Placed_Flag) AS placed_students,
    ROUND(AVG(Placed_Flag) * 100, 2) AS placement_rate_pct
FROM students
GROUP BY workex
ORDER BY placement_rate_pct DESC;

-- Query 8: Top 10 Salary Offers Across All Degree Fields
SELECT 
    student_id,
    gender,
    degree_t,
    specialisation,
    workex,
    ssc_p,
    hsc_p,
    degree_p,
    mba_p AS final_score_p,
    salary
FROM students
WHERE status = 'Placed'
ORDER BY salary DESC
LIMIT 10;

-- Query 9: Placement Rate by High School Stream
SELECT 
    hsc_s AS high_school_stream,
    COUNT(*) AS total_students,
    SUM(Placed_Flag) AS placed_students,
    ROUND(AVG(Placed_Flag) * 100, 2) AS placement_rate_pct
FROM students
GROUP BY hsc_s
ORDER BY placement_rate_pct DESC;

-- Query 10: Salary Metrics by Degree Field and Gender (Placed Only)
SELECT 
    degree_t,
    gender,
    COUNT(*) AS placed_count,
    ROUND(AVG(salary), 2) AS avg_salary,
    MIN(salary) AS min_salary,
    MAX(salary) AS max_salary
FROM students
WHERE status = 'Placed'
GROUP BY degree_t, gender
ORDER BY degree_t, gender;
