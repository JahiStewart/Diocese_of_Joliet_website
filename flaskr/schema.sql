-- Created by Vertabelo (http://vertabelo.com)
-- Last modification TEXT: 2023-11-13 19:34:10.753

-- drop database if exists dojsched;
-- create database dojsched;
-- use dojsched;

DROP TABLE IF EXISTS Organization;
DROP TABLE IF EXISTS Reservation;
DROP TABLE IF EXISTS Room;
DROP TABLE IF EXISTS RoomArrangement;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS UserOrganization;

-- tables
-- Table: Organization
CREATE TABLE Organization (
    Id TEXT NOT NULL unique,
    Name TEXT NOT NULL,
    Description TEXT NULL,
    CONSTRAINT Organization_pk PRIMARY KEY (Id)
);

-- Table: Reservation
CREATE TABLE Reservation (
    Id TEXT NOT NULL unique,
    User_Id TEXT NOT NULL,
    Res_Date TEXT NOT NULL,
    Beg_Time TEXT NOT NULL,
    End_Time TEXT NOT NULL,
    Purpose TEXT NULL,
    Organization_Id TEXT NULL,
    Attendee_Count INTEGER NOT NULL,
    Coffee_YN TEXT NOT NULL DEFAULT 'N',
    Soda_YN TEXT NOT NULL DEFAULT 'N',
    Water_YN TEXT NOT NULL DEFAULT 'N',
    Catering_YN TEXT NOT NULL DEFAULT 'N',
    Lapel_Mic TEXT NOT NULL DEFAULT 'N',
    Podium_Mic TEXT NOT NULL DEFAULT 'N',
    Handheld_Mic TEXT NOT NULL DEFAULT 'N',
    Conf_Phone TEXT NOT NULL DEFAULT 'N',
    Whiteboard_YN TEXT NOT NULL DEFAULT 'N',
    Easel_YN TEXT NOT NULL DEFAULT 'N',
    Special_Notes TEXT NULL,
    Lobby_YN TEXT NOT NULL DEFAULT 'N',
    Room_Id TEXT NOT NULL,
    RoomArrangement_Id TEXT NULL,
    Approved_YN TEXT NOT NULL DEFAULT 'N',
	Canceled_YN TEXT NOT NULL DEFAULT 'N',
    CONSTRAINT Reservation_pk PRIMARY KEY (Id),
    FOREIGN KEY (Organization_Id) REFERENCES Organization (Id),
    FOREIGN KEY (Room_Id) REFERENCES Room (Id),
    FOREIGN KEY (RoomArrangement_Id) REFERENCES RoomArrangement (Id),
    FOREIGN KEY (User_Id) REFERENCES User (Id)
);

-- Table: Space
CREATE TABLE Room (
    Id TEXT NOT NULL unique,
    Name TEXT NOT NULL,
    Picture_Name TEXT NULL,
    Capacity INTEGER NOT NULL,
    CONSTRAINT Room_pk PRIMARY KEY (Id)
);

-- Table: SpaceArrangement
CREATE TABLE RoomArrangement (
    Id TEXT NOT NULL,
    Description TEXT NOT NULL,
    Picture_Name TEXT NOT NULL,
    CONSTRAINT RoomArrangement_pk PRIMARY KEY (Id)
);

-- Table: User
CREATE TABLE User (
    Id TEXT UNIQUE NOT NULL,
    Email TEXT NOT NULL,
    Password TEXT NOT NULL,
    First_Name TEXT NOT NULL,
    Last_Name TEXT NOT NULL,
    Phone TEXT NULL,
    CONSTRAINT User_pk PRIMARY KEY (Id)
);

-- Table: UserOrganization
CREATE TABLE UserOrganization (
    Id TEXT NOT NULL unique,
    Organization_Id TEXT NOT NULL,
    User_Id TEXT NOT NULL,
    CONSTRAINT UserOrganization_pk PRIMARY KEY (Id),
    FOREIGN KEY (User_Id) REFERENCES User (Id),
    FOREIGN KEY (User_Id) REFERENCES User (Id)
);

-- foreign keys
-- Reference: Reservation_Organization (table: Reservation)
-- ALTER TABLE Reservation ADD CONSTRAINT Reservation_Organization FOREIGN KEY Reservation_Organization (Organization_Id)
--     REFERENCES Organization (Id);

-- Reference: Reservation_Space (table: Reservation)
-- ALTER TABLE Reservation ADD CONSTRAINT Reservation_Room FOREIGN KEY Reservation_Room (Room_Id)
--     REFERENCES Room (Id);

-- Reference: Reservation_SpaceArrangement (table: Reservation)
-- ALTER TABLE Reservation ADD CONSTRAINT Reservation_RoomArrangement FOREIGN KEY Reservation_RoomArrangement (RoomArrangement_Id)
--     REFERENCES RoomArrangement (Id);

-- Reference: Reservation_User (table: Reservation)
-- ALTER TABLE Reservation ADD CONSTRAINT Reservation_User FOREIGN KEY Reservation_User (User_Id)
--     REFERENCES User (Id);

-- Reference: UserOrganization_Organization (table: UserOrganization)
-- ALTER TABLE UserOrganization ADD CONSTRAINT UserOrganization_Organization FOREIGN KEY UserOrganization_Organization (Organization_Id)
--     REFERENCES Organization (Id);

-- Reference: UserOrganization_User (table: UserOrganization)
-- ALTER TABLE UserOrganization ADD CONSTRAINT UserOrganization_User FOREIGN KEY UserOrganization_User (User_Id)
--     REFERENCES User (Id);

-- End of file.

