# ai_chatbot/data/sample_postgres.sql
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    department_id INTEGER,
    salary NUMERIC,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

INSERT INTO departments (name) VALUES
('HR'),
('Engineering'),
('Sales');

INSERT INTO employees (name, department_id, salary) VALUES
('Alice', 1, 50000),
('Bob', 2, 60000),
('Charlie', 2, 65000),
('David', 3, 55000),
('Eve', 1, 52000);
