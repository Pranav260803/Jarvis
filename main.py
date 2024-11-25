import speech_recognition as sr
import webbrowser
import pyttsx3
import music_library
import requests

# Initialize pyttsx3 engine
ttsx = pyttsx3.init()

# Set voice to female
voices = ttsx.getProperty('voices')
ttsx.setProperty('voice', voices[1].id)

newsapi = "7d5975f84696478bb40a65e784b7d22a"

# Function to speak text
def speak(text):
    ttsx.say(text)
    ttsx.runAndWait()

# Function to process recognized commands
def process_command(c):
    # Check if the command starts with "open"
    if c.lower().startswith("open"):
        # Extract the website name by removing the word "open"
        website_name = c.lower().replace("open", "").strip()
        if website_name:
            # Construct the URL and open the website
            url = f"https://{website_name}.com"
            webbrowser.open(url)
            speak(f"Opening {website_name}.")
        else:
            speak("I didn't catch the website name. Please try again.")
    
    # Play a song from music library
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1].strip()  # Extract song name after 'play'
        if song in music_library.music:
            link = music_library.music[song]
            webbrowser.open(link)
            speak(f"Playing {song}.")
        else:
            speak("Sorry, I couldn't find that song in the library.")
    
    # Fetch and read news headlines
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()

            # Extract the articles
            articles = data.get('articles', [])
            
            if articles:
                # Print the headlines
                for article in articles:
                    speak(article['title'])
            else:
                speak("No news articles found.")
        else:
            speak("Sorry, I couldn't fetch the news at the moment.")
    
    else:
        # let open ai handle request
        pass


if __name__ == "__main__":
    speak("Initializing Jarvis....")
    recognizer = sr.Recognizer()
    
    while True:
        try:
            # Listen for the word "Jarvis"
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source)

            print("Recognizing...")
            word = recognizer.recognize_google(audio).lower()

            if word == "jarvis":
                speak("Yes, I am listening.")
                
                # Listen for the actual command
                with sr.Microphone() as source:
                    
                    print("Jarvis is listening...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)
                    print(f"Command received: {command}")
                    
                    process_command(command)

        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            speak("Sorry, I did not understand that.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            speak("I am having trouble connecting to the internet.")
        except Exception as e:
            print(f"An error occurred: {e}")
