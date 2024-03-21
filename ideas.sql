CREATE TABLE USERS(
     id  INTEGER PRIMARY KEY,
     Username TEXT,
     Password TEXT
     
);
CREATE TABLE IDEAS(
     id INTEGER PRIMARY KEY,
    Name TEXT,
    Description TEXT,
    Desire INTEGER,
    Category TEXT,
    Needed INTEGER,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES USERS(id) 

);


INSERT INTO USERS (Username, Password) VALUES ('wadi', 'wadi');
INSERT INTO USERS (Username, Password) VALUES ('thomas', 'thomas');



INSERT INTO IDEAS (Name,Description, Desire, Category, Needed, user_id) VALUES('Code de la route','Entrainement',3,'Lecon de code', 1,1);

INSERT INTO IDEAS (Name,Description, Desire, Category, Needed , user_id) VALUES('Jouer de la musique','Musique',5,'Musique', 0,2);

INSERT INTO IDEAS (Name,Description, Desire, Category, Needed, user_id) VALUES('Revision Python','Entrainement dev ',2,'Développement', 0,2);


