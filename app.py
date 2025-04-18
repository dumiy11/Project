from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import datetime
import threading
import os
import pyttsx3
import pyjokes
import queue
import webbrowser
import wikipedia
import smtplib
from email.mime.text import MIMEText

# ---- Speech Queue & Worker ----
speech_queue = queue.Queue()

def speech_worker():
    engine = pyttsx3.init('sapi5')
    engine.setProperty('rate', 150)  # Speaking speed
    engine.setProperty('volume', 1.0)  # Max volume
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    while True:
        text = speech_queue.get()  # Get text from the queue
        if text is None:  # Gracefully exit when the app stops
            break
        engine.say(text)
        engine.runAndWait()
        speech_queue.task_done()

# Start the speech worker thread once
speech_thread = threading.Thread(target=speech_worker, daemon=True)
speech_thread.start()

# ---- Speak Function ----
def speak(text):
    print("[Auralis is speaking]:", text)
    speech_queue.put(text)  # Put text in the queue for speaking

# ---- Time-based Greeting ----
def wishMe(start=True):
    hour = int(datetime.datetime.now().hour)

    if start:
        if hour >= 0 and hour < 12:
            speak("Good Morning!")
        elif hour >= 12 and hour < 18:
            speak("Good Afternoon!")
        else:
            speak("Good Evening!")

        speak("I am Auralis. Good to see you again.")
    else:
        speak("Goodbye, sir.")
        if hour >= 0 and hour < 12:
            speak("Have a good day!")
        elif hour >= 18 and hour < 24:
            speak("Have a good night!")

# ---- Take Command Function ----
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=5, phrase_time_limit=8)

        try:
            query = r.recognize_google(audio, language='en-in').lower()
            print("You said:", query)
            return query

        except sr.UnknownValueError:
            return "Sorry, I didn't understand that."
        except sr.RequestError:
            return "Speech service is down."

# ---- Website Launcher ----
websites = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "instagram": "https://www.instagram.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://twitter.com",
    "x": "https://twitter.com",
    "chatgpt": "https://chat.openai.com",
    "linkedin": "https://www.linkedin.com",
    "github": "https://github.com",
    "stackoverflow": "https://stackoverflow.com",
    "reddit": "https://www.reddit.com",
    "amazon": "https://www.amazon.in",
    "flipkart": "https://www.flipkart.com",
    "netflix": "https://www.netflix.com",
    "spotify": "https://open.spotify.com",
    "quora": "https://www.quora.com",
    "pinterest": "https://www.pinterest.com",
    "snapchat": "https://web.snapchat.com",
    "whatsapp": "https://web.whatsapp.com",
    "discord": "https://discord.com",
    "gmail": "https://mail.google.com",
    "maps": "https://maps.google.com",
    "news": "https://news.google.com",
    "bing": "https://www.bing.com",
    "yahoo": "https://in.yahoo.com",
    "zomato": "https://www.zomato.com",
    "swiggy": "https://www.swiggy.com"
}

def open_site(url):
    os.system(f'start "" "{url}"')

def open_notepad():
    os.system("start notepad")

# ---- Command Processor ----
context_memory = {}

# Email sender credentials (replace with actual or fetch securely)
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_password"

def send_email(to_address, subject, content):
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = to_address

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

def play_music():
    music_folder = "D:\music"  # Change to your path
    songs = os.listdir(music_folder)
    if songs:
        os.startfile(os.path.join(music_folder, songs[0]))
        return "Playing music..."
    return "No songs found in your music folder."

def set_reminder(message, seconds):
    def reminder_job():
        speak(f"Reminder: {message}")
    threading.Timer(seconds, reminder_job).start()

# Extend this block inside process_command:
def process_command(command):
    command = command.lower()

    # Handle variations of opening websites
    for name, url in websites.items():
        if any(phrase in command for phrase in [f"open {name}", f"take me to {name}", f"launch {name}", f"go to {name}"]):
            speak(f"Opening {name}")
            threading.Thread(target=open_site, args=(url,)).start()
            return f"Opening {name.title()}..."

    # Open specific Windows apps
    if "open calculator" in command:
        speak("Opening Calculator")
        threading.Thread(target=lambda: os.system("start calc")).start()
        return "Opening Calculator..."

    elif "open clock" in command:
        speak("Opening Clock")
        threading.Thread(target=lambda: os.system("start timedate.cpl")).start()
        return "Opening Clock..."

    elif "open settings" in command:
        speak("Opening Settings")
        threading.Thread(target=lambda: os.system("start ms-settings:")).start()
        return "Opening Settings..."

    elif "open task manager" in command:
        speak("Opening Task Manager")
        threading.Thread(target=lambda: os.system("start taskmgr")).start()
        return "Opening Task Manager..."

    elif "open notepad" in command:
        speak("Opening Notepad")
        threading.Thread(target=lambda: os.system("start notepad")).start()
        return "Opening Notepad..."

    elif "open paint" in command:
        speak("Opening Paint")
        threading.Thread(target=lambda: os.system("start mspaint")).start()
        return "Opening Paint..."

    elif "open file explorer" in command:
        speak("Opening File Explorer")
        threading.Thread(target=lambda: os.system("start explorer")).start()
        return "Opening File Explorer..."

    elif "open command prompt" in command:
        speak("Opening Command Prompt")
        threading.Thread(target=lambda: os.system("start cmd")).start()
        return "Opening Command Prompt..."

    # Other commands (time, joke, calculation, etc.)
    elif "time" in command:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {now}")
        return f"The time is {now}"

    elif "joke" in command:
        joke = pyjokes.get_joke()
        speak(joke)
        return joke

    elif "calculate" in command:
        try:
            expression = command.replace("calculate", "").strip()
            expression = expression.replace("x", "*")
            result = eval(expression)
            speak(f"The result is {result}")
            return f"The result is {result}"
        except:
            speak("I couldn't calculate that.")
            return "I couldn't calculate that."

    # Wikipedia search
    elif "wikipedia" in command:
        try:
            query = command.replace("wikipedia", "").strip()
            result = wikipedia.summary(query, sentences=2)
            speak(result)
            return result
        except:
            speak("Couldn't find anything on Wikipedia.")
            return "Wikipedia search failed."

    # Send Email
    elif "send email" in command:
        try:
            speak("To whom should I send the email?")
            recipient = take_command()
            speak("What's the subject?")
            subject = take_command()
            speak("What's the message?")
            message = take_command()
            send_email(recipient, subject, message)
            speak("Email sent successfully.")
            return "Email has been sent."
        except Exception as e:
            speak("Failed to send email.")
            return str(e)

    # Set Reminders
    elif "remind me" in command:
        try:
            speak("What should I remind you about?")
            reminder_text = take_command()
            speak("In how many seconds?")
            seconds = int(take_command())
            set_reminder(reminder_text, seconds)
            return f"Reminder set for {reminder_text} in {seconds} seconds."
        except:
            return "Failed to set reminder."

    # Play Music
    elif "play music" in command:
        return play_music()

    # Google Search
    elif "search google for" in command:
        query = command.split("search google for")[-1].strip()
        url = f"https://www.google.com/search?q={query}"
        speak(f"Searching Google for {query}")
        threading.Thread(target=lambda: webbrowser.open(url)).start()
        return f"Searching Google for {query}..."

    # YouTube Search
    elif "search youtube for" in command:
        query = command.split("search youtube for")[-1].strip()
        url = f"https://www.youtube.com/results?search_query={query}"
        speak(f"Searching YouTube for {query}")
        threading.Thread(target=lambda: webbrowser.open(url)).start()
        return f"Searching YouTube for {query}..."

    return "Sorry, I don't understand."

# ---- Flask App ----
app = Flask(__name__)

@app.route('/')
def index():
    wishMe()  # Call wishMe to greet the user when they visit the app
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    user_msg = data['message']
    reply = process_command(user_msg)
    return jsonify({"reply": reply})

@app.route('/mic')
def mic():
    user_input = take_command()
    reply = process_command(user_input)
    return jsonify({"user": user_input, "reply": reply})

@app.route('/stop', methods=['POST'])
def stop():
    speak("Goodbye!")
    return jsonify({"reply": "Speech stopped."})

if __name__ == '__main__':
    app.run(debug=True)
