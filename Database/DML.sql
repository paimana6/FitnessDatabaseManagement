

ALTER SEQUENCE users_user_id_seq RESTART WITH 7;
ALTER SEQUENCE members_member_id_seq  RESTART WITH 3;


INSERT INTO Users (user_id, username, password, user_type)
VALUES
    (1, 'boss', 'adminpassword', 'admin'),
    (2, 'john', 'john', 'trainer'),
    (3, 'sam', 'sam', 'trainer'),
    (4, 'fatima', 'fatima', 'trainer'),
    (5, 'bob', 'bob', 'member'),
    (6, 'eve', 'eve', 'member');


INSERT INTO Trainers (trainer_id,user_id, full_name, email, phone_number, address)
VALUES
    (1,2, 'John Smith', 'john@gmail.com', '123-456-7890', '123 Main St, City, Country'),
    (2,3, 'Samantha Davis', 'samantha@gmail.com', '321-654-9870', '321 Pine St, City, Country'),
    (3,4, 'Fatima Wilson', 'fatima@gmail.com', '654-987-3210', '654 Maple St, City, Country');

INSERT INTO Members (member_id,user_id, full_name, email, phone_number, address, fitness_goal, weight, height)
VALUES
    (1,5, 'Bob Johnson', 'bob@gmail.com', '444-555-6666', '456 Oak St, City, Country', 'Build Muscle', 170.3, 70.8),
    (2,6, 'Eve Wilson', 'eve@gmail.com', '987-654-3210', '654 Cedar St, City, Country', 'Lose Weight', 130.8, 58.3);


INSERT INTO ExerciseRoutines (name, description, difficulty_level, duration_minutes, calories_burned, muscle_groups) 
VALUES ('Push-up Routine', 'A classic bodyweight exercise targeting the chest, shoulders, and triceps.', 'Beginner', 10, 100, 'Chest, Shoulders, Triceps');
INSERT INTO ExerciseRoutines (name, description, difficulty_level, duration_minutes, calories_burned, muscle_groups) 
VALUES ('Squat Routine', 'A compound lower-body exercise targeting the quadriceps, hamstrings, and glutes.', 'Intermediate', 15, 150, 'Quadriceps, Hamstrings, Glutes');
INSERT INTO ExerciseRoutines (name, description, difficulty_level, duration_minutes, calories_burned, muscle_groups) 
VALUES ('Plank Routine', 'A core-strengthening exercise that engages multiple muscle groups, including the abdominals and lower back.', 'Beginner', 5, 50, 'Abdominals, Lower Back');
INSERT INTO ExerciseRoutines (name, description, difficulty_level, duration_minutes, calories_burned, muscle_groups) 
VALUES ('Burpee Routine', 'A full-body exercise combining a squat, push-up, and jump, providing cardiovascular and strength benefits.', 'Advanced', 20, 200, 'Entire Body');
INSERT INTO ExerciseRoutines (name, description, difficulty_level, duration_minutes, calories_burned, muscle_groups) 
VALUES ('Lunges Routine', 'An effective lower-body exercise targeting the quadriceps, hamstrings, and glutes.', 'Intermediate', 12, 120, 'Quadriceps, Hamstrings, Glutes');


INSERT INTO FitnessFacts (fact_text) VALUES
('Running is cheaper than therapy, and you get to eat more pizza afterward.'),
('The only bad workout is the one that didn’t happen... and the one where you forget your gym shoes.'),
('Fitness tip: Work out early in the morning before your brain realizes what you’re doing.'),
('Sweat is just your fat crying because it knows it’s about to leave your body forever.'),
('The gym is like a dictionary - it has a lot of words, but you only use a few.'),
('The only time you should ever look back is to see how far you’ve come... unless you’re running on a treadmill.'),
('Exercise is a dirty word. Every time I hear it, I wash my mouth out with chocolate.'),
('Remember, the best exercise for the human heart is reaching down to lift someone else up.'),
('Fitness fact: You can’t outrun your fork.'),
('The only workout you’ll ever regret is the one you didn’t do. And the one where you tried to show off on the treadmill.');


INSERT INTO Equipment (equipment_name, equipment_type, purchase_date)
VALUES 
    ('Treadmill', 'Cardio', '2023-01-15'),
    ('Dumbbells', 'Strength', '2023-02-20'),
    ('Stationary Bike', 'Cardio', '2023-03-10'),
    ('Leg Press Machine', 'Strength', '2023-04-05'),
    ('Elliptical Trainer', 'Cardio', '2023-05-12'),
    ('Rowing Machine', 'Cardio', '2023-06-20'),
    ('Bench Press', 'Strength', '2023-07-25'),
    ('Barbell', 'Strength', '2023-08-10'),
    ('Exercise Ball', 'Other', '2023-09-15'),
    ('Resistance Bands', 'Other', '2023-10-20'),
    ('Jump Rope', 'Other', '2023-11-10'),
    ('Yoga Mat', 'Other', '2023-12-05'),
    ('Smith Machine', 'Strength', '2024-01-15'),
    ('Stability Ball', 'Other', '2024-02-20');

INSERT INTO Room (room_id, room_name, capacity) VALUES
(1, 'Meeting Room', 10),
(2, 'Studio A', 15),
(3, 'Studio B', 12),
(4, 'Weight Room', 30),
(5, 'Cardio Room', 20),
(6, 'Tennis Court', 2);

INSERT INTO TrainingSessions (trainer_id, member_id, session_date, session_time)
VALUES
    (1, 1, '2024-04-15', '09:00:00'),  
    (2, 2, '2024-04-16', '10:00:00'), 
    (3, 1, '2024-04-17', '11:00:00');  


INSERT INTO TrainerSchedule (trainer_id, day_of_week, start_time, end_time)
VALUES
    (1, 'Monday', '08:00:00', '12:00:00'),
    (2, 'Tuesday', '09:00:00', '13:00:00'),
    (3, 'Wednesday', '10:00:00', '14:00:00');


INSERT INTO Payments (user_id, payment_method, card_number, expiration_date)
VALUES
    (5, 'Credit Card', '1234567812345678', '2025-12-31'),  
    (6, 'PayPal', '9834657892', '2025-12-31');      


INSERT INTO Subscriptions (user_id, start_date, amount_owed, payment_status, payment_date)
VALUES
    (5, '2024-04-01', 30.00, FALSE, '2024-04-01'),  
    (6, '2024-04-01', 30.00, FALSE, '2024-04-01');  


INSERT INTO MemberAchievements (user_id, achievement_description, date_achieved)
VALUES
    (5, 'Ran 5 kilometers', '2024-04-05'),  
    (6, 'Lost 5 pounds', '2024-04-10');     

INSERT INTO EquipmentMaintenance (equipment_id, last_maintenance_date, next_maintenance_date, maintenance_notes)
VALUES
    (1, '2024-03-01', '2024-09-01', 'Routine maintenance performed.'),
    (2, '2024-02-15', '2024-08-15', 'Checked for any damages.'),
    (3, '2024-03-10', '2024-09-10', 'Oiled moving parts.');

INSERT INTO Booking (room_id, start_time, end_time, purpose, booked_for)
VALUES
    (1, '2024-04-20 09:00:00', '2024-04-20 10:00:00', 'Meeting', 'John Smith'),
    (2, '2024-04-21 10:00:00', '2024-04-21 11:00:00', 'Yoga Class', 'Samantha Davis');

INSERT INTO ClassSchedule (class_name, description, day_of_week, start_time, end_time, trainer_id)
VALUES
    ('Yoga Class', 'Relaxing yoga session for all levels.', 'Monday', '18:00:00', '19:00:00', 2),
    ('Spin Class', 'High-intensity cycling workout.', 'Wednesday', '17:00:00', '18:00:00', 3);


INSERT INTO GroupFitnessSessions (class_id, member_id, session_date, session_time)
VALUES
    (1, 1, '2024-04-22', '18:00:00'),  
    (2, 2, '2024-04-23', '17:00:00');  
