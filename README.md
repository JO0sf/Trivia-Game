# Trivia-Game
A game where users will be able to answer trivia questions with varying difficulties and categories.

## Issues
Couldn't figure out a way to quit the program without it having to reach the end.
Fixed this by importing sys and using sys.quit().

The user's answer choice being a string while the correct option was an int, so it wouldn't get counted as correct even the correct answer was given.
Fixed by converting the user's answer choice to an int.

Answer will print if user enter invalid input.
Fixed by changing when it prints to after telling user if they are right or wrong.

Will crash if there is an invalid input when answering a question.
Moved elif checking if there was a valid input before elif trying to change input to an int.

Won't loop and let user retry question if an invalid input was given.
Fixed by adding a isValid boolean variable that will keep looping until a valid input is given.

## Tasks
  1. Successfully connect to API and fetch questions
  2. Let users choose number of questions, category, and difficulty
  3. Make a way for questions to print one-at-a-time
  4. Make a way to tell when user gets question right
  5. Add up number of questions gotten correct