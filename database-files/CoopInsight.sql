DROP DATABASE IF EXISTS CoopInsight;
CREATE DATABASE IF NOT EXISTS CoopInsight;
USE CoopInsight;
CREATE TABLE IF NOT EXISTS `User`
(
    UserID      INT PRIMARY KEY,
    FirstName   VARCHAR(50) NOT NULL,
    LastName    VARCHAR(50) NOT NULL,
    Email       VARCHAR(50) NOT NULL,
    Password    VARCHAR(50) NOT NULL,
    PhoneNumber VARCHAR(15) NOT NULL,
    AccessLevel VARCHAR(50) NOT NULL DEFAULT 'User'
);
CREATE TABLE IF NOT EXISTS Skill
(
    SkillID   INT PRIMARY KEY,
    SkillName VARCHAR(50) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS Industry
(
    IndustryID   INT PRIMARY KEY,
    IndustryName VARCHAR(50) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS StudentMajor
(
    Major      VARCHAR(50) NOT NULL PRIMARY KEY,
    IndustryID INT REFERENCES Industry (IndustryID)
);
CREATE TABLE IF NOT EXISTS Company
(
    CompanyID          INT PRIMARY KEY,
    CompanyName        VARCHAR(50)  NOT NULL,
    IndustryID         INT REFERENCES Industry (IndustryID),
    CompanyDescription VARCHAR(500) NOT NULL,
    AdminID            INT REFERENCES `User` (UserID)
);
CREATE TABLE IF NOT EXISTS JobListing
(
    JobID          INT PRIMARY KEY,
    Name           VARCHAR(50)  NOT NULL,
    CompanyID      INT REFERENCES Company (CompanyID),
    Major          VARCHAR(50) REFERENCES StudentMajor (Major),
    MinGPA         FLOAT(4)     NOT NULL,
    IndustryID     INT REFERENCES Industry (IndustryID),
    Posted         DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    JobDescription VARCHAR(500) NOT NULL,
    SkillID        INT REFERENCES Skill (SkillID)
);
CREATE TABLE IF NOT EXISTS Employee
(
    EmployeeID INT PRIMARY KEY,
    UserID     INT REFERENCES `User` (UserID),
    HiredOn    DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Role       VARCHAR(50) NOT NULL DEFAULT 'Employee',
    JobID      INT REFERENCES JobListing (JobID),
    CompanyID  INT REFERENCES Company (CompanyID)
);
CREATE TABLE IF NOT EXISTS Student
(
    StudentID    INT PRIMARY KEY,
    UserID       INT REFERENCES `User` (UserID),
    GPA          FLOAT(4)    NOT NULL,
    Skill        INT REFERENCES Skill (SkillID),
    Major        VARCHAR(50) NOT NULL,
    SupervisorID INT REFERENCES Employee (EmployeeID)
);
CREATE TABLE IF NOT EXISTS Applicant
(
    ApplicantID INT PRIMARY KEY,
    StudentID   INT REFERENCES Student (StudentID),
    JobID       INT REFERENCES JobListing (JobID),
    Status      VARCHAR(50) NOT NULL DEFAULT 'Pending'
);
CREATE TABLE IF NOT EXISTS JobHistory
(
    JobHistoryID            INT PRIMARY KEY,
    UserID                  INT REFERENCES `User` (UserID),
    JobID                   INT REFERENCES JobListing (JobID),
    Wage                    INT                                NOT NULL,
    EmploymentStartDATETIME DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    EmploymentEndDATETIME   DATE,
    TerminationReason       VARCHAR(200)                       NOT NULL
);
CREATE TABLE IF NOT EXISTS Rating
(
    RatingID                    INT PRIMARY KEY,
    OverallRating               INT          NOT NULL,
    REVIEW                      VARCHAR(500) NOT NULL,
    WorkCultureRating           INT          NOT NULL,
    CompensationRating          INT          NOT NULL,
    WorkLifeBalanceRating       INT          NOT NULL,
    LearningOpportunitiesRating INT          NOT NULL,
    JobID                       INT REFERENCES JobListing (JobID),
    StudentID                   INT REFERENCES Student (StudentID)
);
CREATE TABLE IF NOT EXISTS Offer
(
    OfferID       INT PRIMARY KEY,
    ApplicantID   INT REFERENCES Student (StudentID),
    JobID         INT REFERENCES JobListing (JobID),
    Wage          INT         NOT NULL,
    StartDATETIME DATETIME    NOT NULL,
    EndDATETIME   DATE,
    Status        VARCHAR(50) NOT NULL DEFAULT 'Pending'
);
CREATE TABLE IF NOT EXISTS ErrorLog
(
    LogID            INT PRIMARY KEY,
    UserID           INT REFERENCES `User` (UserID),
    ErrorDescription VARCHAR(500) NOT NULL,
    ErrorDATETIME    DATETIME     NOT NULL
);
CREATE TABLE IF NOT EXISTS JobSkill
(
    JobSkillID INT PRIMARY KEY,
    JobID      INT REFERENCES JobListing (JobID),
    SkillID    INT REFERENCES Skill (SkillID)
);
