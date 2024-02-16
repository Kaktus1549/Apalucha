CREATE TABLE Films(
    ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT, -- Film ID is the primary key
    Title VARCHAR(255) NOT NULL, -- Film name
    Team VARCHAR(255) NOT NULL, -- Film team
    FinalVoteCount INT DEFAULT 0 -- Final vote count
)