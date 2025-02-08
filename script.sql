-- For table schema information 
SELECT 
    c.COLUMN_NAME,
    c.DATA_TYPE,
    c.CHARACTER_MAXIMUM_LENGTH,
    c.IS_NULLABLE,
    c.COLUMN_DEFAULT,
    tc.CONSTRAINT_TYPE
FROM 
    INFORMATION_SCHEMA.COLUMNS c
LEFT JOIN 
    INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu ON c.COLUMN_NAME = kcu.COLUMN_NAME AND c.TABLE_NAME = kcu.TABLE_NAME
LEFT JOIN 
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc ON kcu.CONSTRAINT_NAME = tc.CONSTRAINT_NAME
WHERE 
    c.TABLE_NAME = 'Table name';


-- Master table for student Data Table 1 
CREATE TABLE Student (
    StudentID INT NOT NULL PRIMARY KEY,
    Fullname NVARCHAR(100) NOT NULL,
    Fname NVARCHAR(25),
    Mname NVARCHAR(25),
    Lname NVARCHAR(25),
    Password NVARCHAR(255) NOT NULL,
    Respass1 NVARCHAR(255),
    Respass2 NVARCHAR(255),
    Respass3 NVARCHAR(255),
    EmailId NVARCHAR(255) NOT NULL UNIQUE,
    Mobile VARCHAR(15) UNIQUE,
    Gender CHAR(10),
    DOB DATE NOT NULL,
    EducationLevel NVARCHAR(100) NOT NULL,
    College NVARCHAR(255) NOT NULL,
    Marks DECIMAL(10, 2) NOT NULL,
    Course NVARCHAR(100) NOT NULL,
    Specialization NVARCHAR(255) NOT NULL,
    PrimarySkill NVARCHAR(255) NOT NULL,
    SecondarySkill NVARCHAR(255),
    PositionApplying NVARCHAR(255),
    AlternateMobile CHAR(15),
    AlternateEmail NVARCHAR(255) NOT NULL,
    HomeState NVARCHAR(100) NOT NULL,
    HomeCity NVARCHAR(100) NOT NULL,
    CurrentState NVARCHAR(100) NOT NULL,
    CurrentCity NVARCHAR(100) NOT NULL,
    PreferredLocation NVARCHAR(100) NOT NULL,
    ResumeFilePath NVARCHAR(255),
    CreatedAt DATETIME DEFAULT GETDATE(),
    DOE DATETIME,
    gitlink NVARCHAR(50),
    linkedinlink NVARCHAR(50)
);

-- Skills table Table 2
CREATE TABLE def_skills (
    SkillID INT IDENTITY(1,1) PRIMARY KEY,
    Skills NVARCHAR(100) UNIQUE
);

-- States table Table 3
CREATE TABLE states (
    state_id INT PRIMARY KEY IDENTITY(1,1),
    state_name VARCHAR(100) NOT NULL
);

-- Cities table Table 4
CREATE TABLE Cities (
    city_id INT PRIMARY KEY IDENTITY(1,1),
    city_name VARCHAR(100) NOT NULL,
    state_id INT NULL,
    CONSTRAINT FK_State FOREIGN KEY (state_id) REFERENCES States(state_id)
);

-- Create Courses Table Table 5
CREATE TABLE Courses (
    CourseID INT PRIMARY KEY IDENTITY(1,1),
    CourseName VARCHAR(255) NOT NULL UNIQUE
);

-- Create Education Levels Table Table 6
CREATE TABLE EducationLevels (
    LevelID INT PRIMARY KEY IDENTITY(1,1),
    LevelName VARCHAR(255) NOT NULL UNIQUE
);

-- Create table Positions Table 7
CREATE TABLE positions(
	pos_id INT PRIMARY KEY IDENTITY(1,1),
	Pos NVARCHAR(50)
);

-- Evaluation table Table 8
CREATE TABLE Evaluation (
    EvalId INT IDENTITY(1,1) PRIMARY KEY,     
    StudentID INT NOT NULL,                    
    Marks INT NOT NULL,                      
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID) 
);

-- Updated table Evaluation
CREATE TABLE Evaluation (
    EvalId INT IDENTITY(1,1) PRIMARY KEY,     
    StudentID INT NOT NULL,                    
    Marks INT NOT NULL,
    Attempt INT NOT NULL,
    Code NVARCHAR(MAX),                      
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID) 
);
<<<<<<< HEAD

-- Table of cities available for the jobs
CREATE TABLE AvailCities (
    AcID INT PRIMARY KEY IDENTITY(1,1),
    City NVARCHAR(255)
);
=======
>>>>>>> 1a3273ae59f8e552b94296cf8d7769cc7ccd9ab3

# file updated at 2025-03-20

# file updated at 2024-08-03

# file updated at 2024-08-05

# file updated at 2024-08-21

# file updated at 2024-09-20

# file updated at 2024-10-15

# file updated at 2024-11-24

# file updated at 2025-01-30

# file updated at 2025-02-08
