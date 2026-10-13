import requests
import html

def get_trivia_questions(amount=10, category=None, difficulty=None, qtype=None):
    """
    Fetch trivia questions from the Open Trivia DB API.
    
    :param amount: Number of questions (1–50)
    :param category: Category ID
    :param difficulty: 'easy', 'medium', or 'hard'
    :param qtype: 'multiple' or 'boolean'
    :return: List of question dictionaries
    """
    # Validate amount
    if not (1 <= amount <= 50):
        raise ValueError("Amount must be an integer between 1 and 50.")

    # Base API URL
    url = "https://opentdb.com/api.php"
    
    # Build query parameters
    params = {"amount": amount}
    if category:
        params["category"] = category
    if difficulty:
        params["difficulty"] = difficulty.lower()
    if qtype:
        params["type"] = qtype.lower()

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()
    except requests.RequestException as e:
        print(f"Error fetching trivia questions: {e}")
        return []

    # API response code handling
    if data.get("response_code") != 0:
        print(f"API returned error code: {data.get('response_code')}")
        return

    # Decode HTML entities in questions/answers
    questions = []
    for item in data.get("results", []):
        questions.append({
            "category": html.unescape(item["category"]),
            "type": item["type"],
            "difficulty": item["difficulty"],
            "question": html.unescape(item["question"]),
            "correct_answer": html.unescape(item["correct_answer"]),
            "incorrect_answers": [html.unescape(ans) for ans in item["incorrect_answers"]]
        })

    return questions

def amount_selection():
    """
    Allow the user to select the number of questions for the quiz.
    """
    while True:
        try:
            amount = int(input("First off, how many questions would you like to answer? (1-50): "))
            if 0 <= amount <= 50:
                choices.append(amount)
            else:
                print("Please enter a number between 1 and 50.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Main execution block
print("Welcome to the Trivia Quiz Game!")
print("Enter '0' at any point to quit.\n")

amount = amount_selection()


trivia_list = get_trivia_questions(amount=amount, difficulty="medium", qtype="multiple")

if trivia_list:
    for i, q in enumerate(trivia_list, start=1):
        print(f"\nQ{i}: {q['question']}")
        options = q["incorrect_answers"] + [q["correct_answer"]]
        # Shuffle options
        import random
        random.shuffle(options)
        for j, opt in enumerate(options, start=1):
            print(f"  {j}. {opt}")
        print(f"Answer: {q['correct_answer']}")
