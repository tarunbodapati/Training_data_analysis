import json
from datetime import datetime, timedelta


# Load JSON data from file
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# 1. Function to count the completions for each training course
def count_completed_trainings(data):
    training_completion_counts = {}
    for person in data:
        for completion in person.get('completions', []):
            course_name = completion.get('name')
            if course_name:
                training_completion_counts[course_name] = training_completion_counts.get(course_name, 0) + 1
    return training_completion_counts

# 2. Function to find people who completed specified trainings within a given fiscal year
def people_completed_trainings_by_fiscal_year(data, trainings_list, fiscal_year):
    fiscal_year_start = datetime(fiscal_year - 1, 7, 1)
    fiscal_year_end = datetime(fiscal_year, 6, 30)
    completed_trainings = {training: [] for training in trainings_list}

    for person in data:
        for completion in person.get('completions', []):
            course_name = completion.get('name')
            completion_date = completion.get('timestamp')
            if course_name in trainings_list and completion_date:
                date_completed = datetime.strptime(completion_date, '%m/%d/%Y')
                if fiscal_year_start <= date_completed <= fiscal_year_end:
                    completed_trainings[course_name].append(person['name'])

    return completed_trainings

# 3. Function to check for expired or expiring soon trainings
def expiring_trainings_within_month(data, reference_date_str):
    reference_date = datetime.strptime(reference_date_str, '%m/%d/%Y')
    one_month_later = reference_date + timedelta(days=30)
    expiring_or_expired = []

    for person in data:
        upcoming_expirations = []
        for completion in person.get('completions', []):
            expiration_date_str = completion.get('expires')
            if expiration_date_str:
                expiration_date = datetime.strptime(expiration_date_str, '%m/%d/%Y')
                if expiration_date < reference_date:
                    upcoming_expirations.append({"name": completion['name'], "status": "expired"})
                elif reference_date <= expiration_date <= one_month_later:
                    upcoming_expirations.append({"name": completion['name'], "status": "expires soon"})
        
        if upcoming_expirations:
            expiring_or_expired.append({"name": person['name'], "trainings": upcoming_expirations})
    
    return expiring_or_expired

# Main function to process the data and save the results
def process_trainings(file_path):
    data = load_json(file_path)
    
    # Output 1: Training counts
    training_counts = count_completed_trainings(data)
    with open('output_1.json', 'w') as f:
        json.dump(training_counts, f, indent=4)
    
    # Output 2: People who completed specified trainings in the fiscal year
    trainings_list = ["Electrical Safety for Labs", "X-Ray Safety", "Laboratory Safety Training"]
    people_completed = people_completed_trainings_by_fiscal_year(data, trainings_list, 2024)
    with open('output_2.json', 'w') as f:
        json.dump(people_completed, f, indent=4)

    # Output 3: Trainings that are expired or expiring soon
    expiring_trainings = expiring_trainings_within_month(data, "10/01/2023")
    with open('output_3.json', 'w') as f:
        json.dump(expiring_trainings, f, indent=4)

# Run the process
process_trainings('C:/Users/Bodapati Tarun Kumar/Desktop/project/trainings.txt')
