-- Joe Shmoe
INSERT INTO User
    (UserID, FirstName, LastName, Email, Password, PhoneNumber)
VALUES
    (default, 'Joe', 'Shmoe', 'j.shmoe@gmail.com', '123abc', '+15555555555');

INSERT INTO Skill
    (SkillID, SkillName)
VALUES
    (default, 'Software Engineering');

INSERT INTO Industry
    (IndustryID, IndustryName)
VALUES
    (default, 'Software Engineering');

INSERT INTO StudentMajor
    (Major, IndustryID)
VALUES
    ('Computer Science', 1);

INSERT INTO Company
(CompanyID, CompanyName, IndustryID, CompanyDescription, AdminID)
VALUES
    (default, 'Beta', 1, 'Meta but Beta', 1);

Insert Into JobListing (JobID, Name, CompanyID, Major, MinGPA, IndustryID, Posted, JobDescription, SkillID) VALUES (default, 'SWE Job', 1, 'Computer Science', 3.5, 1, default, 'SWE!', 1);


INSERT INTO Student (StudentID, UserID, GPA, Skill, Major, SupervisorID) VALUES (default, 1, 3.5, 1, 'Computer Science', null);
UPDATE Student SET Major = 'Computer Science' WHERE UserID = (SELECT UserID FROM User WHERE FirstName = 'Joe' AND LastName = 'Shmoe');
SELECT * FROM Student WHERE StudentID IN (SELECT StudentID FROM JobHistory WHERE JobID = 1);
SELECT * FROM JobListing WHERE Major = (SELECT Major FROM Student WHERE UserID = 1);
INSERT INTO Rating (OverallRating, Review, WorkCultureRating, CompensationRating, WorkLifeBalanceRating, LearningOpportunitiesRating, JobID, UserID) VALUES (5, 'Great employer!', 5, 5, 5, 5, 1, 1);
INSERT INTO Applicant (ApplicantID, StudentID, JobID, Status) VALUES (default, 1, 1, default);

SELECT * FROM Applicant INNER JOIN Student s ON Applicant.StudentID = s.StudentID INNER JOIN JobListing j ON Applicant.JobID = j.JobID WHERE s.GPA >= 3.5 AND j.Major = s.Major;
UPDATE Applicant SET Status = 'Rejected' WHERE ApplicantID = 1;
INSERT INTO JobListing (JobID, Name, CompanyID, Major, MinGPA, IndustryID, Posted, JobDescription, SkillID) VALUES (default, 'SWE Job', 1, 'Computer Science', 3.5, 1, default, 'SWE!', 1);
SELECT * FROM Student INNER JOIN Applicant ON Student.StudentID = Applicant.StudentID;
SELECT * FROM JobHistory WHERE JobID = 1;
UPDATE Student SET SupervisorID = 1 WHERE StudentID = 1;

SELECT COUNT(*) FROM Applicant WHERE JobID = 1;
SELECT COUNT(*) FROM Employee WHERE CompanyID = 1 AND HiredOn >= NOW() - INTERVAL 1 MONTH;
SELECT AVG(Review) FROM Rating WHERE JobID = 1;
SELECT * FROM JobListing ORDER BY MinGPA DESC;
SELECT * FROM Offer ORDER BY Wage ASC;
SELECT COUNT(*) FROM JobListing WHERE Posted >= NOW() - INTERVAL 7 DAY;

DELETE FROM Company WHERE CompanyID = 1;
INSERT INTO Company (CompanyID, CompanyName, IndustryID, CompanyDescription, AdminID) VALUES (DEFAULT, 'CoopInsight', 1, 'Databased!', 1);
UPDATE User SET AccessLevel = 'admin' WHERE UserID = 1;
DELETE FROM JobListing WHERE JobID = 1;
DELETE FROM Rating WHERE RatingID = 1;
SELECT * FROM ErrorLog WHERE ErrorDate >= NOW() - INTERVAL 7 DAY;