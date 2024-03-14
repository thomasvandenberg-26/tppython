CREATE TABLE IDEAS(
     id INTEGER PRIMARY KEY,
    Name TEXT,
    Description TEXT,
    Desire INTEGER,
    Category TEXT,
    Needed INTEGER

);


INSERT INTO IDEAS (Name,Description, Desire, Category, Needed) VALUES('Code de la route','Entrainement',3,'Lecon de code', 1);

INSERT INTO IDEAS (Name,Description, Desire, Category, Needed) VALUES('Jouer de la musique','Musique',5,'Musique', 0);

INSERT INTO IDEAS (Name,Description, Desire, Category, Needed) VALUES('Revision Python','Entrainement dev ',2,'Développement', 1);

-- CREATE TABLE USERS(
--      id  INTEGER PRIMARY KEY,
--      Username TEXT,
--      Password TEXT,
--      user_IdeaId INTEGER FOREIGN KEY(user_IdeaId) REFERENCES IDEAS(id),

     

-- )

-- INSERT INTO IDEAS (Username, Password ) VALUES ('wadi','wadi');

-- INSERT INTO IDEAS (Username, Password ) VALUES ('thomas','thomas');
