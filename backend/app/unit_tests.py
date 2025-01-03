from fastapi.testclient import TestClient
import sys
import os

# Ensure the correct path is added for module resolution
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/../"))

from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_create_user():
    user_data = {
        "name": "John Doe",
        "age": 30,
        "gender": "Male",
        "height": 180.0,
        "weight": 75.5
    }
    response = client.post("/users?user_id=1", json=user_data)
    assert response.status_code == 200
    assert response.json()["user"]["name"] == "John Doe"

def test_add_workout():
    workout_data = {"user_id": 1, "exercise": "Running", "duration": 30}
    response = client.post("/workouts", json=workout_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Workout added successfully"

def test_get_workouts():
    response = client.get("/workouts/1")
    assert response.status_code == 200
    assert "workouts" in response.json()

def test_add_nutrition_log():
    nutrition_data = {"user_id": 1, "food": "Chicken Salad", "calories": 400}
    response = client.post("/nutrition", json=nutrition_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Nutrition log added successfully"



def test_get_weight_logs():
    # Add weight log for testing
    weight_log = {"user_id": 1, "weight": 75.0, "date": "2024-12-29"}
    client.post("/weight", json=weight_log)

    # Test retrieving weight logs
    response = client.get("/weight/1")
    assert response.status_code == 200
    assert "logs" in response.json()  # Updated to match the response
    assert len(response.json()["logs"]) > 0



def test_recommended_calories():
    params = {
        "age": 30,
        "weight": 75.5,
        "height": 180,
        "gender": "male",
        "activity_level": "medium",
        "target": "weight loss"
    }
    response = client.get("/recommended-calories", params=params)
    assert response.status_code == 200
    assert "recommended_calories" in response.json()
    assert response.json()["target"] == "weight loss"

def test_scrape_training_program_with_goal():
    response = client.get("/scrape-training-program?goal=muscle")
    assert response.status_code == 200
    data = response.json()
    assert "training_programs" in data
    assert isinstance(data["training_programs"], list)
    assert len(data["training_programs"]) > 0

    first_program = data["training_programs"][0]
    assert "title" in first_program
    assert "link" in first_program
    assert "description" in first_program

def test_scrape_training_program_with_invalid_goal():
    response = client.get("/scrape-training-program?goal=nonexistent")
    assert response.status_code == 200
    data = response.json()
    assert "training_programs" in data
    assert len(data["training_programs"]) == 1

    first_program = data["training_programs"][0]
    assert first_program["title"] == "Full Body Strength Training Program"
    assert "https://www.muscleandstrength.com/workouts/full-body-strength-training" in first_program["link"]    