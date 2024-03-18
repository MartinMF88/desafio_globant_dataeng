create table departments (
	id_department integer primary key,
	department text);
	
	
create table hired_employees (
	id_employee integer primary key,
	name_employee text,
	hire_date TIMESTAMP WITH TIME ZONE,
	department_id integer,
	job_id integer);
	
create table jobs (
	job_id integer primary key,
	job_position text);	

SELECT 
    d.department,
    j.job_position AS job,
    SUM(CASE WHEN EXTRACT(quarter FROM he.hire_date) = 1 THEN 1 ELSE 0 END) AS Q1,
    SUM(CASE WHEN EXTRACT(quarter FROM he.hire_date) = 2 THEN 1 ELSE 0 END) AS Q2,
    SUM(CASE WHEN EXTRACT(quarter FROM he.hire_date) = 3 THEN 1 ELSE 0 END) AS Q3,
    SUM(CASE WHEN EXTRACT(quarter FROM he.hire_date) = 4 THEN 1 ELSE 0 END) AS Q4
FROM 
    hired_employees he
JOIN 
    departments d ON he.department_id = d.id_department
JOIN 
    jobs j ON he.job_id = j.job_id
WHERE 
    EXTRACT(year FROM he.hire_date) = 2021
GROUP BY 
    d.department, j.job_position
ORDER BY 
    d.department, j.job_position;
	

	
WITH hired_count AS (
    SELECT 
        department_id,
        COUNT(*) AS total_hired
    FROM 
        hired_employees
    WHERE 
        EXTRACT(year FROM hire_date) = 2021
    GROUP BY 
        department_id
),
dept_avg AS (
    SELECT 
        AVG(total_hired) AS avg_hired
    FROM 
        hired_count
)
SELECT 
    d.id_department AS id,
    d.department,
    hc.total_hired AS hired
FROM 
    hired_count hc
JOIN 
    departments d ON hc.department_id = d.id_department
JOIN 
    dept_avg da ON TRUE
WHERE 
    hc.total_hired > da.avg_hired
ORDER BY 
    hc.total_hired DESC;