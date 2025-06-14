import speech_recognition as sr
import pyttsx3
import datetime

# Initialize speech engine
engine = pyttsx3.init()
recognizer = sr.Recognizer()

# Mock database (replace with API calls in real implementation)
restaurants = {
    "pizza hut": {"menu": {"pepperoni pizza": 12.99, "garlic bread": 4.99}},
    "burger king": {"menu": {"whopper": 8.99, "fries": 3.49}}
}

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio).lower()
        except:
            return ""

def place_order():
    order = {"items": []}
    
    # Step 1: Restaurant Selection
    speak("Welcome to FoodieVoice! What restaurant would you like to order from?")
    while True:
        restaurant = listen()
        if restaurant in restaurants:
            speak(f"Great choice! Here's {restaurant}'s menu: {', '.join(restaurants[restaurant]['menu'].keys())}")
            break
        else:
            speak("Sorry, we don't partner with that restaurant. Please try Pizza Hut or Burger King")

    # Step 2: Item Selection
    speak("What would you like to order? Say 'done' when finished")
    while True:
        item = listen()
        if "done" in item:
            break
        if item in restaurants[restaurant]["menu"]:
            speak(f"How many {item}s would you like?")
            quantity = listen()
            if quantity.isdigit():
                order["items"].append({
                    "name": item,
                    "price": restaurants[restaurant]["menu"][item],
                    "quantity": int(quantity)
                })
                speak(f"Added {quantity} {item}s to your cart")
            else:
                speak("Please say a number quantity")
        else:
            speak("Item not found. Please choose from the menu")

    # Step 3: Order Confirmation
    total = sum(item["price"] * item["quantity"] for item in order["items"])
    speak(f"Your total is ${total:.2f}. Would you like to confirm this order? Say yes or no")
    
    if "yes" in listen():
        speak(f"Order confirmed! Your food will arrive by {datetime.datetime.now().hour + 1}:00. Thank you!")
        return order
    else:
        speak("Order cancelled. Let's start over")
        return None

if __name__ == "__main__":
    speak("FoodieVoice assistant starting")
    placed_order = place_order()
    if placed_order:
        print("Order placed:", placed_order)