
-- Job Application Tracker
-- Sample Data
-- Run after creating the tables in schema.sql
-- Intended for an empty database

-- ============================================
-- 1. COMPANIES
-- ============================================

INSERT INTO companies
(company_id, company_name, industry, website, city, state, notes)
VALUES
(1, 'TechNova Solutions', 'Software Development',
 'https://example.com', 'Miami', 'FL',
 'Software development and technology consulting'),

(2, 'DataWorks Analytics', 'Data Analytics',
 'https://example.org', 'Orlando', 'FL',
 'Specializes in database systems and analytics'),

(3, 'CloudBridge Technologies', 'Cloud Computing',
 'https://example.net', 'Tampa', 'FL',
 'Cloud infrastructure and backend services'),

(4, 'NextGen Financial', 'Financial Technology',
 'https://example.edu', 'Fort Lauderdale', 'FL',
 'Financial software and payment solutions'),

(5, 'InnovateAI Labs', 'Artificial Intelligence',
 'https://example.io', 'Austin', 'TX',
 'AI research and machine learning applications');


-- ============================================
-- 2. JOBS
-- ============================================

INSERT INTO jobs
(job_id, company_id, job_title, job_type,
 salary_min, salary_max, job_url, date_posted,
 requirements)
VALUES
(1, 1, 'Junior Backend Developer', 'Full-time',
 65000, 85000, 'https://example.com/jobs/1',
 '2026-11-01',
 '["Python", "Flask", "SQL", "Git"]'),

(2, 1, 'Software Engineering Intern', 'Internship',
 25000, 35000, 'https://example.com/jobs/2',
 '2026-11-03',
 '["Python", "Java", "Git"]'),

(3, 2, 'Junior Database Developer', 'Full-time',
 60000, 80000, 'https://example.org/jobs/3',
 '2026-10-25',
 '["SQL", "MySQL", "Python", "Database Design"]'),

(4, 2, 'Data Analyst Intern', 'Internship',
 30000, 40000, 'https://example.org/jobs/4',
 '2026-11-05',
 '["Python", "SQL", "Pandas", "Excel"]'),

(5, 3, 'Backend Software Engineer', 'Full-time',
 85000, 110000, 'https://example.net/jobs/5',
 '2026-10-20',
 '["Python", "REST APIs", "Docker", "AWS"]'),

(6, 3, 'Cloud Developer Intern', 'Internship',
 35000, 45000, 'https://example.net/jobs/6',
 '2026-11-07',
 '["Python", "AWS", "Git", "Linux"]'),

(7, 4, 'Full Stack Developer', 'Full-time',
 75000, 100000, 'https://example.edu/jobs/7',
 '2026-10-30',
 '["JavaScript", "HTML", "CSS", "SQL", "React"]'),

(8, 5, 'Machine Learning Intern', 'Internship',
 40000, 55000, 'https://example.io/jobs/8',
 '2026-11-10',
 '["Python", "Pandas", "NumPy", "Machine Learning"]');


-- ============================================
-- 3. APPLICATIONS
-- ============================================

INSERT INTO applications
(application_id, job_id, application_date, status,
 resume_version, cover_letter_sent, interview_data)
VALUES
(1, 1, '2026-11-02', 'Applied',
 'Backend Resume V1', FALSE, NULL),

(2, 2, '2026-11-04', 'Screening',
 'Software Resume V1', TRUE, NULL),

(3, 3, '2026-10-28', 'Interview',
 'Database Resume V2', TRUE,
 '{"interview_date": "2026-11-20", "type": "Technical", "notes": "SQL and database design interview"}'),

(4, 4, '2026-11-06', 'Rejected',
 'Data Resume V1', FALSE, NULL),

(5, 5, '2026-10-22', 'Offer',
 'Backend Resume V2', TRUE,
 '{"interview_date": "2026-11-05", "type": "Technical", "notes": "Completed technical interview"}'),

(6, 8, '2026-11-12', 'Applied',
 'AI Resume V1', TRUE, NULL);


-- ============================================
-- 4. CONTACTS
-- ============================================

INSERT INTO contacts
(contact_id, company_id, contact_name, title,
 email, phone, linked_in_url, notes)
VALUES
(1, 1, 'Sarah Mitchell', 'Technical Recruiter',
 'sarah.mitchell@example.com', '555-010-1001',
 'https://www.linkedin.com/',
 'Recruiter for backend and software positions'),

(2, 2, 'David Chen', 'Hiring Manager',
 'david.chen@example.org', '555-010-1002',
 'https://www.linkedin.com/',
 'Contact for database development opportunities'),

(3, 3, 'Emily Rodriguez', 'HR Specialist',
 'emily.rodriguez@example.net', '555-010-1003',
 'https://www.linkedin.com/',
 'Handles engineering recruitment'),

(4, 4, 'Michael Johnson', 'Engineering Manager',
 'michael.johnson@example.com', '555-010-1004',
 'https://www.linkedin.com/',
 'Oversees full stack development team'),

(5, 5, 'Jessica Lee', 'University Recruiter',
 'jessica.lee@example.com', '555-010-1005',
 'https://www.linkedin.com/',
 'Recruiter for internship opportunities');
