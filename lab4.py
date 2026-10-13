import requests
import html
import sys

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
            amount = int(input("\nFirst off, how many questions would you like to answer? (1-50): "))
            if 1 <= amount <= 50:
                return amount
            elif amount == 0:
                print(goodbye_message)
                sys.exit(0)
            else:
                print("Please enter a number between 1 and 50.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def category_selection():
    """
    Allow the user to select the category for the quiz questions.
    """
    while True:
        try:
            category = int(input("\nPlease select a category:\n9. General Knowledge\n10. Entertainment: Books\n11. Entertainment: Film\n12. Entertainment: Music\n13. Entertainment: Musicals & Theatres\n14. Entertainment: Television\n15. Entertainment: Video Games\n16. Entertainment: Board Games\n17. Science & Nature\n18. Science: Computers\n19. Science: Mathematics\n20. Mythology\n21. Sports\n22. Geography\n23. History\n24. Politics\n25. Art\n26. Celebrities\n27. Animals\n28. Vehicles\n29. Entertainment: Comics\n30. Science: Gadgets\n31. Entertainment: Japanese Anime & Manga\n32. Entertainment: Cartoon & Animations\nEnter the number corresponding to your choice (or 8 for any category): "))
            if 9 <= category <= 32:
                return category
            elif category == 8:
                return None
            elif category == 0:
                print(goodbye_message)
                sys.exit(0)
            else:
                print("Please enter a number between 8 and 32.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def difficulty_selection():
    """
    Allow the user to select the difficulty level for the quiz questions.
    """
    while True:
        difficulty = input("\nPlease select a difficulty level (easy, medium, hard, or any): ").strip().lower()
        if difficulty in ["easy", "medium", "hard"]:
            return difficulty
        elif difficulty == "any":
            return None
        elif difficulty == "0":
            print(goodbye_message)
            sys.exit(0)
        else:
            print("Invalid input. Please enter 'easy', 'medium', 'hard', or 'any'.")

def goodbye_message():
    return "Exiting the trivia quiz. Goodbye!"

def final_score(points=0, total=0):
    return f"Final score: {points}/{total}\n{goodbye_message}"

def early_quit_message(points=0, attempted=0, total=0):
    return f"{attempted}/{total} questions attempted\n{final_score(points, total)}"

# Main execution block
points = 0

print("Welcome to the Trivia Quiz Game!")
print("Enter '0' at any point to quit.\n")

amount = amount_selection()
category = category_selection()
difficulty = difficulty_selection()

trivia_list = get_trivia_questions(amount=amount, category=category, difficulty=difficulty, qtype="multiple")

for i, q in enumerate(trivia_list, start=1):
    correct_option = 0

    print(f"\nQ{i}: {q['question']}")
    options = q["incorrect_answers"] + [q["correct_answer"]]
    import random
    random.shuffle(options)

    for j, opt in enumerate(options, start=1):
        print(f"  {j}. {opt}")
        if opt == q["correct_answer"]:
            correct_option = j

    answer = input("Your answer (1-4): ")
    print(f"Answer: {q['correct_answer']}")
    if answer == '0':
        print(early_quit_message(points, i, amount))
        sys.exit(0)
    elif int(answer) == correct_option:
        print("Correct!\n")
        points += 1
    elif answer in ['1', '2', '3', '4']:
        print("Incorrect!\n")
    elif answer == "":
        print("Invalid input. Please enter a number between 1 and 4.\n")
    else:
        print("Invalid input. Please enter a number between 1 and 4.\n")

print(final_score(points, amount))