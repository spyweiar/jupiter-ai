import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import subprocess
import pyautogui
import random
import time
import logging
import requests
import json

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Initialize logger
logging.basicConfig(level=logging.ERROR)

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech using SpeechRecognition
def recognize_speech():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            audio = recognizer.listen(source)

            print("Recognizing...")
            query = recognizer.recognize_google(audio)
            print("You said:", query)
            return query.lower()

    except sr.UnknownValueError:
        logging.error("Could not understand audio")
        speak("Sorry, I could not understand that.")
        return None

    except sr.RequestError as e:
        logging.error(f"Could not request results from Google Speech Recognition service; {e}")
        speak("Sorry, there was an error with the speech recognition service.")
        return None

# Function to open a website
def open_website(command):
    supported_websites = {
        "open the web browser chrome": "https://www.google.com/",
        "google": "https://www.google.com/",
        "open discord": "https://discord.com/",
        "open yahoo": "https://www.yahoo.com/",
        "go to github": "https://github.com/",
        "open stackoverflow": "https://stackoverflow.com/",
        "open duckduckgo": "https://duckduckgo.com/",
        "open chrome": "https://www.google.com/",
        "open firefox": "https://www.firefox.com/",
        "open the web browser edge": "https://www.microsoft.com/edge/",
        "open edge": "https://www.microsoft.com/edge/",
        "open youtube": "https://www.youtube.com/",
        "youtube": "https://www.youtube.com/",
        "open spotify": "https://open.spotify.com/",
        "open facebook": "https://www.facebook.com/",
        "open instagram": "https://www.instagram.com/",
        "open netflix": "https://www.netflix.com/",
        "open github": "https://github.com/",
        "open twitter": "https://twitter.com/",
        "open stack overflow": "https://stackoverflow.com/",
        "open chat gpt": "https://chat.openai.com/",
        "open chat gbt": "https://chat.openai.com/",
        "open email": "https://mail.google.com/mail/u/0/#inbox",
        "open my email": "https://mail.google.com/mail/u/0/#inbox"
    }

    for keyword in supported_websites:
        if keyword in command:
            speak(f"Opening {keyword}...")
            webbrowser.open(supported_websites[keyword])
            return

    speak("Sorry, I didn't recognize the website. Please try again.")

# Function to search the web
def search(query):
    speak(f"Searching the web for {query}...")
    webbrowser.open(f"https://www.google.com/search?q={query}")

# Function to search Youtube
def youtube(query):
    speak(f"Searching Youtube for {query}...")
    webbrowser.open(f"https://www.youtube.com/search?q={query}")

# Function to open an application
def open_application(app_name):
    try:
        subprocess.Popen(f'"{app_name}"', shell=True)
        speak(f"Opening {app_name}...")
    except Exception as e:
        logging.error(f"Error opening {app_name}: {str(e)}")
        speak(f"Error opening {app_name}: {str(e)}")

# Function to open a photo viewer
def open_photo_viewer(image_path):
    subprocess.Popen(['explorer.exe', 'path', image_path])

# Function to take a screenshot using pyautogui library
def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    speak("Screenshot taken and saved as screenshot.png")

# Function to perform calculator operations
def perform_calculator():
    speak("Sure, let's do some calculations. Please say the operation, for example, 'add 7 and 3'.")
    operation = recognize_speech()

    if operation:
        try:
            result = evaluate_operation(operation)
            speak(f"The result is {result}.")
        except Exception as e:
            logging.error(f"Error in calculation: {str(e)}")
            speak(f"Sorry, there was an error in the calculation: {str(e)}")

# Function to evaluate calculator operation
def evaluate_operation(operation):
    components = operation.split()
    num1 = float(components[1])
    operator = components[0]
    num2 = float(components[2])
    # +
    if operator == "add":
        return num1 + num2
    # -
    elif operator == "subtract":
        return num1 - num2
    # *
    elif operator == "multiply":
        return num1 * num2
    # ==
    elif operator == "divide":
        if num2 == 0:
            raise ValueError("Cannot divide by zero.")
        return num1 / num2
    # **
    elif operator == "power":
        return num1 ** num2
    else:
        raise ValueError("Invalid operation.")

# Function to tell a joke
def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "What do you get when you cross a snowman and a vampire? Frostbite!",
        "Parallel lines have so much in common. It's a shame they'll never meet.",
        "Why did the computer go to therapy? It had too many bytes of emotional baggage.",
        "I told my wife she was drawing her eyebrows too high. She looked surprised."
    ]
    joke = random.choice(jokes)
    speak(joke)

# Function to lie to the user (as a joke)
def lie_to_me():
    lies = [
        "Did you know that the moon is made of green cheese?",
        "Bananas are actually berries, and strawberries aren't berries!",
        "Elephants are the only animals that can jump.",
        "Cows can sleep standing up, but they prefer to lie down.",
        "If you sneeze too hard, you can fracture a rib. Better be careful!"
    ]
    lie = random.choice(lies)
    speak(lie)

# Function to open File Explorer
def open_file_explorer():
    try:
        subprocess.Popen(['explorer.exe'])
        speak("File Explorer opened.")
    except Exception as e:
        logging.error(f"Error opening File Explorer: {str(e)}")
        speak(f"Error opening File Explorer: {str(e)}")

# Function to get the weather data for a given location
def get_weather_data(location):
    api_key = "4dc5b7624b599a5e024987347068c865"
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}lat=44.34&lon=10.99&appid={api_key}&q={location}"

    try:
        response = requests.get(complete_url)
        data = response.json()

        if data["cod"] != "404":
            main_data = data["main"]
            current_temperature = main_data["temp"]
            current_condition = data["weather"][0]["description"]

            return {
                "current_temperature": current_temperature,
                "current_condition": current_condition
            }

        else:
            speak("Sorry, I could not find the weather data for that location.")
            return None

    except Exception as e:
        logging.error(f"Error getting weather data: {str(e)}")
        return None

# Function to get the news data for a given topic
def get_news_data(topic):
    api_key = "cd60c7e61a514b6ca0c4ca4ee2917434"
    base_url = "https://newsapi.org/v2/top-headlines?"
    complete_url = f"{base_url}apiKey={api_key}&q={topic}"

    try:
        response = requests.get(complete_url)
        data = response.json()

        if data["status"] == "ok":
            headlines = data["articles"][:10]
            headlines_text = [headline["title"] for headline in headlines]
            return {
                "headlines": headlines_text
            }

        else:
            speak("Sorry, I could not find any news for that topic.")
            return None

    except Exception as e:
        logging.error(f"Error getting news data: {str(e)}")
        return None

# Function to perform a task based on the user's command
def perform_task(command):
    # Hello
    if any(keyword in command for keyword in ["hello", "hi"]):
        speak("Hello! How can I help you today?")

    # How are you functionally elif
    elif any(keyword in command for keyword in ["how are you", "how are you doing"]):
        speak("I am just a computer program, but I am functioning as expected. How can I help you?")

    # What is your name
    elif any(keyword in command for keyword in ["What is your name", "say your name"]):
        speak("I am Jupiter Assistant. Nice to meet you!")

    # How old are you
    elif "how old are you" in command:
        speak("I am a computer program, so I don't have an age.")

    # Thank you
    elif "thank you" in command:
        speak("You're welcome!")

    elif "what is python" in command:
        speak("Python is a high-level, general-purpose programming language. You can read more about it on Wikipedia.")
        speak("Do you want to read more about Python?")
        answer = recognize_speech()
        if answer and "yes" in answer:
            webbrowser.open("https://en.wikipedia.org/wiki/Python_(programming_language)")


    # Create list
    elif "create to-do list" in command:
        todo_list = []
        speak("What would you like to add to the to-do list?")
        while True:
            item = recognize_speech()
            if not item or "stop" in item:
                break
            todo_list.append(item)
        with open("todo.txt", "w") as f:
            f.write("\n".join(todo_list))
        speak("To-do list created.")

    # Youtube Search
    elif any(keyword in command for keyword in ["search the youtube", "search youtube"]):
        speak("What would you like to search for on youtube?")
        youtube_query = recognize_speech()
        if youtube_query:
            youtube(youtube_query)

    # Google Search
    elif any(keyword in command for keyword in ["search the web", "search Google"]):
        speak("What would you like to search for?")
        search_query = recognize_speech()
        if search_query:
            search(search_query)

    # Open application
    elif "open application" in command:
        speak("Which application would you like to open?")
        app_name = recognize_speech()
        if app_name:
            open_application(app_name)

    # Open photo viewer
    elif "open photo viewer" in command:
        image_path = "C:\\Path\\To\\Your\\Photo.jpg"
        open_photo_viewer(image_path)

    # Take Screenshot
    elif "take screenshot" in command:
        take_screenshot()

    # Calculator
    elif "calculator" in command:
        perform_calculator()

    # Tell me a joke
    elif "tell me a joke" in command:
        tell_joke()

    # Lie to me
    elif "lie to me" in command:
        lie_to_me()

    # Open file explorer
    elif "open file explorer" in command:
        open_file_explorer()

    # Time
    elif "time" in command:
        current_time = time.strftime("%H:%M:%S")
        speak(f"The time is {current_time}.")

    # Weather
    elif "weather" in command:
        speak("What is the location?")
        location = recognize_speech()
        if location:
            weather_data = get_weather_data(location)
            if weather_data:
                speak(f"The current temperature in {location} is {weather_data['current_temperature']} degrees Celsius with {weather_data['current_condition']}.")
            else:
                speak("Sorry, I could not find the weather data for that location.")
        else:
            speak("Please tell me the location.")

    # News
    elif "news" in command:
        speak("What is the topic?")
        topic = recognize_speech()
        if topic:
            news_data = get_news_data(topic)
            if news_data:
                speak(f"Here are the latest news headlines for {topic}:")
                for i, headline in enumerate(news_data['headlines']):
                    speak(f"{i+1}. {headline}")
            else:
                speak("Sorry, I could not find any news for that topic.")

    # Exit
    elif any(keyword in command for keyword in ["exit", "bye"]):
        speak("Goodbye! Have a great day.")
        exit()

# Function to show the login page
def show_login_page():
    speak("Can you enter your username and password?")
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")
    return username, password

# Function to check login
def check_login(username, password):
    valid_credentials = {"dmxt": "Bb8847337", "anas": "spywearBb8847337", "user": "123456", "user2": "111555"}
    return username in valid_credentials and valid_credentials[username] == password

if __name__ == "__main__":
    speak("Hello! I am Jupiter. How can I help you today?")

    while True:
        username, password = show_login_page()
        if check_login(username, password):
            speak("Login successful.")
            break
        else:
            speak("Invalid username or password. Please try again.")

    while True:
        command = recognize_speech()
        if command:
            perform_task(command)