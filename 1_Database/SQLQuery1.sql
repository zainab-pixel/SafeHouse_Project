-- 1. Création de la Base de Données
CREATE DATABASE SafeHouseDB;
GO

USE SafeHouseDB;
GO

-- 2. Table unique pour les données des capteurs (Température, Lumière, etc.)
CREATE TABLE SensorData (
    id INT IDENTITY(1,1) PRIMARY KEY,
    sensor_type VARCHAR(50) NOT NULL, -- ex: 'temperature', 'light'
    value_float FLOAT NULL,           -- pour 21.5
    value_string VARCHAR(50) NULL,    -- pour 'ON', 'OFF'
    zone VARCHAR(50) DEFAULT 'salon',
    timestamp DATETIME DEFAULT GETDATE()
);

-- 3. Table pour l'historique des événements (Logs)
CREATE TABLE EventLogs (
    id INT IDENTITY(1,1) PRIMARY KEY,
    event_type VARCHAR(50),
    description VARCHAR(255),
    timestamp DATETIME DEFAULT GETDATE()
);
-- 4. Table des Utilisateurs (Login/Register)
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='dashboard_appuser' AND xtype='U')
CREATE TABLE dashboard_appuser (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    email NVARCHAR(100) UNIQUE NOT NULL,
    password NVARCHAR(100) NOT NULL,
    role NVARCHAR(50),
    permissions NVARCHAR(MAX),
    created_at DATETIME DEFAULT GETDATE()
);
GO

-- 4. Données initiales pour éviter que le dashboard soit vide au début
INSERT INTO SensorData (sensor_type, value_float, value_string, zone) VALUES ('temperature', 22.5, NULL, 'salon');
INSERT INTO SensorData (sensor_type, value_float, value_string, zone) VALUES ('light', NULL, 'OFF', 'salon');
INSERT INTO SensorData (sensor_type, value_float, value_string, zone) VALUES ('door', NULL, 'CLOSED', 'entree');
GO