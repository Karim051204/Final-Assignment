from flask import Flask, render_template, request, send_from_directory
import matplotlib.pyplot as plt
import numpy as np
import random
import os

# Initialize Flask App
app = Flask(__name__, static_url_path='/static')

# Function definitions

def generate_workout(goal, difficulty, exercises):
    # Generates 3 different workout plans based on user input
    workout_options = {
        "Weight Loss": ["Jump Rope", "Burpees", "Mountain Climbers", "Cycling", "Running", "Rowing", "Jumping Jacks", "Plank"],
        "Muscle Gain": ["Bench Press", "Deadlifts", "Squats", "Bicep Curls", "Pull-ups", "Dips", "Lunges", "Lat Pulldown"],
        "Endurance": ["Rowing", "Running Intervals", "Jump Rope", "Box Jumps", "Battle Ropes", "Plank Holds", "Sled Push"]
    }

    available_exercises = workout_options.get(goal, [])
    if len(available_exercises) < exercises:
        exercises = len(available_exercises)  # Makes sure we don't pick more exercises than available

    workout_plans = []
    for _ in range(3):  # Generates 3 different workouts
        workout = random.sample(available_exercises, exercises)
        workout_plans.append(workout)
    
    return workout_plans


def predict_progress(goal, weight, duration, frequency):
    #Predicts realistic progress over a 6-month period for weight loss, muscle gain, and endurance.
    months = np.arange(1, duration + 1)
    
    if goal == "Weight Loss":
        max_loss = 10  
        progress = weight - (max_loss * (1 - np.exp(-0.3 * months)) * (frequency / 3))  # Gradual slowdown
    elif goal == "Muscle Gain":
        max_gain = 6  
        progress = weight + (max_gain * (1 - np.exp(-0.2 * months)) * (frequency / 3))  # Slows over time
    else:
        max_improvement = 20  
        progress = weight + (max_improvement * (1 - np.exp(-0.25 * months)) * (frequency / 3))  # Initial quick gains, then slow
    
    return progress.tolist()


def generate_progress_graph(goal, weight, duration, frequency):
    #Creates a graph specific to the user's goal with realistic, gradual changes.
    progress_data = predict_progress(goal, weight, duration, frequency)
    months = np.arange(1, duration + 1)
    
    # Define colors based on goal for visual distinction
    if goal == "Weight Loss":
        line_color = "#FF5733"  # Orange-Red for weight loss
        title_color = "#FF8C00"
    elif goal == "Muscle Gain":
        line_color = "#33FF57"  # Green for muscle gain
        title_color = "#00FF00"
    else:
        line_color = "#3380FF"  # Blue for endurance
        title_color = "#0096FF"

    # Dark theme
    plt.style.use("dark_background")
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(months, progress_data, marker="o", linestyle="-", color=line_color, linewidth=3, markersize=10)

    # Titles and labels
    ax.set_xlabel("Months", fontsize=14, color="white")
    if goal == "Weight Loss":
        ax.set_ylabel("Weight (kg)", fontsize=14, color="white")
        ax.set_title("Projected Weight Loss Over Time", fontsize=16, color=title_color)
    elif goal == "Muscle Gain":
        ax.set_ylabel("Muscle Mass (kg)", fontsize=14, color="white")
        ax.set_title("Projected Muscle Growth Over Time", fontsize=16, color=title_color)
    else:
        ax.set_ylabel("Endurance Improvement (%)", fontsize=14, color="white")
        ax.set_title("Projected Endurance Improvement Over Time", fontsize=16, color=title_color)

    # Grid and styling
    ax.grid(color="gray", linestyle="--", linewidth=0.7, alpha=0.6)
    ax.spines["bottom"].set_color("white")
    ax.spines["left"].set_color("white")
    ax.tick_params(axis="x", colors="white")
    ax.tick_params(axis="y", colors="white")

    # Save graph
    graph_path = "static/progress_chart.png"
    plt.savefig(graph_path, transparent=True)  # Transparent for better blending
    plt.close()
    
    return graph_path

# Route definitions

@app.route("/", methods=["GET", "POST"])
def home():
    #Main Page - Collects user input and generates 3 different workout plans.
    if request.method == "POST":
        username = request.form["username"]
        weight = int(request.form["weight"])
        goal = request.form["goal"]
        difficulty = request.form["difficulty"]
        exercises = int(request.form["exercises"])
        frequency = int(request.form["frequency"])  

        # Generate 3 different workout plans
        workouts = generate_workout(goal, difficulty, exercises)

        return render_template("workout_results.html", username=username, workouts=workouts, weight=weight, goal=goal, frequency=frequency)
    
    return render_template("index.html")


@app.route("/progress")
def progress():
    #Generates a progress prediction graph.
    goal = request.args.get("goal", "Weight Loss")
    weight = int(request.args.get("weight", 70))
    duration = int(request.args.get("duration", 6))
    frequency = int(request.args.get("frequency", 3))

    graph_path = generate_progress_graph(goal, weight, duration, frequency)
    
    return render_template("progress.html", image_path=graph_path)

# Main function

if __name__ == "__main__":
    # Ensures that folders and direcotry exists
    if not os.path.exists("static"):
        os.makedirs("static")
        os.makedirs("static/css") 
        os.makedirs("static/images") 

    app.run(debug=True)
