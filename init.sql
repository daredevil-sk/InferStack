CREATE DATABASE IF NOT EXISTS model_registry;
USE model_registry;

CREATE TABLE IF NOT EXISTS models (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    version VARCHAR(50),
    storage_path TEXT,
    framework VARCHAR(50),
    accuracy FLOAT,
    UNIQUE(name, version)
);

CREATE TABLE IF NOT EXISTS inference_results (
    job_id VARCHAR(255) PRIMARY KEY,
    status VARCHAR(50),
    prediction TEXT,
    error TEXT,
);