
import speech_recognition as sr
import pyttsx3


engine = pyttsx3.init()
engine.setProperty("rate", 165)
engine.setProperty("volume", 1.0)

recognizer = sr.Recognizer()


def speak(text):
    print(f"AI: {text}")
    engine.say(text)
    engine.runAndWait()


def listen():
    with sr.Microphone() as source:
        print("\n🎙️ Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

            text = recognizer.recognize_google(
                audio,
                language="hi-IN"
            )

            print(f"You: {text}")
            return text.lower()

        except sr.WaitTimeoutError:
            return ""

        except sr.UnknownValueError:
            print("Could not understand.")
            return ""

        except sr.RequestError as e:
            print("Speech service error:", e)
            return ""


def main():
    speak("Hello Vikas sir, Welcome back.")

    while True:
        command = listen()

        if not command:
            continue

        if command in ["exit", "quit", "बंद", "बाहर"]:
            speak("Goodbye.")
            break

        if "hello" in command or "हेलो" in command:
            speak("Hello Vikas sir.")

        elif "time" in command or "समय" in command:
            import datetime
            now = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {now}.")

        else:
            speak(f"You said {command}")


if __name__ == "__main__":
    main()
