import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

def save_csv(file_name, data, headers):
    file_exists = os.path.isfile(file_name)

    with open(file_name, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def load_csv(file_name):
    if not os.path.isfile(file_name):
        return []
    with open(file_name, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def log_activity():
    date = datetime.now().strftime('%Y-%m-%d')
    activity = input("Enter Activity Name: ")
    duration = int(input("Enter Activity Duration in Minutes: " ))
    calories = int(input("Enter Calories Burned: "))

    save_csv('fitness_tracker.csv',
             {
                 'Date':date,
                 'Activity': activity,
                 'Duration': duration,
                 'Calories': calories
             }, ['Date', 'Activity', 'Duration', 'Calories'])
    

def view_activity():
    activities = load_csv('activities.csv')
    if not activities:
        print("No past activity found.\n")
        return

    print("Past Activities: ")
    for activity in activities:
        print(f"{activity['Date']}: {activity['Activity']} - {activity['Duration']} mins, {activity['Calories']} cal")
    print()

def set_goals():
    weekly_minutes = int(input("Set weekly exercise goal (in minutes): "))
    daily_calories = int(input("Set daily calorie burn goal: "))
    save_csv('goals.csv', {
        'Weekly Minutes': weekly_minutes,
        'Daily Calories': daily_calories
    }, ['Weekly Minutes', 'Daily Calories'])
    print("Goals set successfully!\n")

def view_progress():
    activities = load_csv('fitness_tracker.csv')
    goals = load_csv('goals.csv')

    if not activities:
        print("No activities to analyze progress.\n")
        return

    if not goals:
        print("No goals set to compare progress.\n")
        return

    goals = goals[-1]
    weekly_goal = int(goals['Weekly Minutes'])
    daily_cal_goal = int(goals['Daily Calories'])

    weekly_data = {}
    for activity in activities:
        week = datetime.strptime(activity['Date'], '%Y-%m-%d').isocalendar()[1]
        weekly_data[week] = weekly_data.get(week, 0) + int(activity['Duration'])

    print("Weekly Progress:")
    for week, duration in weekly_data.items():
        print(f"Week {week}: {duration} minutes (Goal: {weekly_goal})")

    daily_data = {}
    for activity in activities:
        day = activity['Date']
        daily_data[day] = daily_data.get(day, 0) + int(activity['Calories'])

    print("\nDaily Progress:")
    for day, calories in daily_data.items():
        print(f"{day}: {calories} calories (Goal: {daily_cal_goal})")

    plot_progress(weekly_data, "Weekly Activity (Minutes)")
    plot_progress(daily_data, "Daily Calories Burned")

def plot_progress(data, title):
    plt.bar(data.keys(), data.values(), color='skyblue')
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.show()

def main():
    while True:
        print("Personal Fitness Tracker")
        print("1. Log a new activity")
        print("2. View activity history")
        print("3. Set and update fitness goals")
        print("4. View progress reports")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            log_activity()
        elif choice == '2':
            view_activity()
        elif choice == '3':
            set_goals()
        elif choice == '4':
            view_progress()
        elif choice == '5':
            print("Exiting tracker. Stay fit!")
            break
        else:
            print("Invalid choice. Please try again.\n")


main()
    