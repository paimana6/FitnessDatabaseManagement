
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(16) NOT NULL,
    password VARCHAR(16) NOT NULL,
    user_type VARCHAR(20) NOT NULL,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Members (
    member_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    full_name VARCHAR(50) NOT NULL,
    email VARCHAR(50),
    phone_number VARCHAR(20),
    address VARCHAR(100),
    fitness_goal VARCHAR(100),
    weight FLOAT,
    height FLOAT
);

CREATE TABLE Trainers (
    trainer_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    full_name VARCHAR(50) NOT NULL,
    email VARCHAR(50),
    phone_number VARCHAR(20),
    address VARCHAR(100)
);

CREATE TABLE TrainingSessions (
    session_id SERIAL PRIMARY KEY,
    trainer_id INT REFERENCES Trainers(trainer_id) ON DELETE CASCADE,
    member_id INT REFERENCES Members(member_id) ON DELETE CASCADE,
    session_date DATE,
    session_time TIME
);

CREATE TABLE TrainerSchedule (
    schedule_id SERIAL PRIMARY KEY,
    trainer_id INT REFERENCES Trainers(trainer_id) ON DELETE CASCADE,
    day_of_week VARCHAR(10) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL
);

CREATE TABLE Payments (
    payment_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    payment_method VARCHAR(50),
    card_number VARCHAR(16),
    expiration_date DATE,
    registration_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE Subscriptions (
    subscription_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    start_date DATE,
    amount_owed NUMERIC(10, 2) DEFAULT 30.00,  
    payment_status BOOLEAN DEFAULT FALSE,  
    payment_date TIMESTAMP DEFAULT NULL,  
    UNIQUE(user_id, start_date)
);

CREATE TABLE ExerciseRoutines (
    routine_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    difficulty_level VARCHAR(20),
    duration_minutes INTEGER,
    calories_burned INTEGER,
    muscle_groups VARCHAR(100)
);

CREATE TABLE FitnessFacts (
    fact_id SERIAL PRIMARY KEY,
    fact_text TEXT NOT NULL
);

CREATE TABLE MemberAchievements (
    achievement_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    achievement_description TEXT NOT NULL,
    date_achieved DATE NOT NULL
);

CREATE TABLE Equipment (
    equipment_id SERIAL PRIMARY KEY,
    equipment_name VARCHAR(100),
    equipment_type VARCHAR(100),
    purchase_date DATE
);

CREATE TABLE EquipmentMaintenance (
    maintenance_id SERIAL PRIMARY KEY,
    equipment_id INT REFERENCES Equipment(equipment_id),
    last_maintenance_date DATE,
    next_maintenance_date DATE,
    maintenance_notes TEXT
);

CREATE TABLE Room (
    room_id SERIAL PRIMARY KEY,
    room_name VARCHAR(100) NOT NULL,
    capacity INT NOT NULL,
    is_booked BOOLEAN DEFAULT FALSE
);

CREATE TABLE Booking (
    booking_id SERIAL PRIMARY KEY,
    room_id INT REFERENCES Room(room_id),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    purpose VARCHAR(255),
    booked_for VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ClassSchedule (
    schedule_id SERIAL PRIMARY KEY,
    class_name VARCHAR(100) NOT NULL,
    description TEXT,
    day_of_week VARCHAR(20) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    trainer_id INT REFERENCES Trainers(trainer_id)
);

CREATE TABLE GroupFitnessSessions (
    session_id SERIAL PRIMARY KEY,
    class_id INT REFERENCES ClassSchedule(schedule_id) ON DELETE CASCADE,
    member_id INT REFERENCES Members(member_id) ON DELETE CASCADE,
    session_date DATE,
    session_time TIME
);

