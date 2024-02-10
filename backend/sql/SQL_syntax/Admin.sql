CREATE TABLE Admins (
    Username VARCHAR(255) NOT NULL PRIMARY KEY, -- Admin username is the primary key
    PasswordHash VARCHAR(255) NOT NULL -- Admin password hash
)