import pytest
from project import generate_workout, predict_progress

def test_generate_workout():
    """Test that generate_workout returns exactly 3 workout plans with the correct number of exercises."""
    goal = "Muscle Gain"
    difficulty = "Intermediate"
    exercises = 5
    workouts = generate_workout(goal, difficulty, exercises)
    
    assert len(workouts) == 3  # Ensure 3 different workout plans are generated
    for workout in workouts:
        assert len(workout) == exercises  # Ensure each workout has the correct number of exercises
        assert all(isinstance(ex, str) for ex in workout)  # Ensure exercises are strings

def test_predict_progress():
    """Test that predict_progress returns a valid list of predicted values."""
    goal = "Weight Loss"
    weight = 80  # Starting weight
    duration = 6  # 6 months
    frequency = 3  # 3 workouts per week
    progress = predict_progress(goal, weight, duration, frequency)
    
    assert isinstance(progress, list)  # Ensure the output is a list
    assert len(progress) == duration  # Ensure the list length matches the duration
    assert all(isinstance(val, (int, float)) for val in progress)  # Ensure all values are numbers
    assert progress[0] > progress[-1]  # Ensure weight loss is happening over time

def test_predict_progress_muscle_gain():
    """Test that muscle gain follows an increasing trend."""
    goal = "Muscle Gain"
    weight = 70  # Starting weight
    duration = 6  # 6 months
    frequency = 4  # 4 workouts per week
    progress = predict_progress(goal, weight, duration, frequency)
    
    assert progress[0] < progress[-1]  # Ensure muscle mass increases over time

def test_predict_progress_endurance():
    """Test that endurance improvement follows an increasing trend."""
    goal = "Endurance"
    weight = 100  # Dummy initial value
    duration = 6  # 6 months
    frequency = 5  # 5 workouts per week
    progress = predict_progress(goal, weight, duration, frequency)
    
    assert progress[0] < progress[-1]  # Ensure endurance improves over time
