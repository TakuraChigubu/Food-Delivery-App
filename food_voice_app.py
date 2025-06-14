import tkinter as tk
from tkinter import scrolledtext
import threading
import speech_recognition as sr
import pyttsx3
import datetime
import queue

class VoiceFoodApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FoodieVoice Assistant")
        
        # GUI Components
        self.create_widgets()
        
        # Voice setup
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.queue = queue.Queue()
        
        # Mock database
        self.restaurants = {
            "pizza hut": {"menu": {"pepperoni pizza": 12.99, "garlic bread": 4.99}},
            "burger king": {"menu": {"whopper": 8.99, "fries": 3.49}}
        }

    def create_widgets(self):
        # Chat Log
        self.chat_log = scrolledtext.ScrolledText(self.root, width=60, height=20)
        self.chat_log.pack(pady=10)
        
        # Control Buttons
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(pady=10)
        
        self.start_btn = tk.Button(self.btn_frame, text="Start", command=self.start_app)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.order_btn = tk.Button(self.btn_frame, text="Place Order", command=self.place_order)
        self.order_btn.pack(side=tk.LEFT, padx=5)
        
        self.exit_btn = tk.Button(self.btn_frame, text="Exit", command=self.root.destroy)
        self.exit_btn.pack(side=tk.LEFT, padx=5)

    def update_log(self, text, is_user=False):
        tag = "user" if is_user else "system"
        self.chat_log.configure(state='normal')
        self.chat_log.insert(tk.END, f"{'You: ' if is_user else 'System: '}{text}\n", tag)
        self.chat_log.configure(state='disabled')
        self.chat_log.see(tk.END)

    def speak(self, text):
        self.update_log(text)
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            self.update_log("Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio).lower()
                self.update_log(text, is_user=True)
                return text
            except sr.UnknownValueError:
                self.update_log("Could not understand audio")
                return ""
            except sr.RequestError:
                self.update_log("Speech service unavailable")
                return ""

    def place_order(self):
        def order_thread():
            order = {"items": []}
            
            # Restaurant Selection
            self.speak("Welcome to FoodieVoice! What restaurant would you like to order from?")
            restaurant = ""
            while True:
                restaurant = self.listen()
                if restaurant in self.restaurants:
                    menu = ", ".join(self.restaurants[restaurant]["menu"].keys())
                    self.speak(f"Great choice! Here's {restaurant}'s menu: {menu}")
                    break
                else:
                    self.speak("Sorry, we don't partner with that restaurant. Please try Pizza Hut or Burger King")

            # Item Selection
            self.speak("What would you like to order? Say 'done' when finished")
            while True:
                item = self.listen()
                if "done" in item:
                    break
                if item in self.restaurants[restaurant]["menu"]:
                    self.speak(f"How many {item}s would you like?")
                    quantity = self.listen()
                    if quantity.isdigit():
                        order["items"].append({
                            "name": item,
                            "price": self.restaurants[restaurant]["menu"][item],
                            "quantity": int(quantity)
                        })
                        self.speak(f"Added {quantity} {item}s to your cart")
                    else:
                        self.speak("Please say a number quantity")
                else:
                    self.speak("Item not found. Please choose from the menu")

            # Confirmation
            total = sum(item["price"] * item["quantity"] for item in order["items"])
            self.speak(f"Your total is ${total:.2f}. Confirm order? Say yes or no")
            
            if "yes" in self.listen():
                delivery_time = datetime.datetime.now().hour + 1
                self.speak(f"Order confirmed! Your food will arrive by {delivery_time}:00. Thank you!")
            else:
                self.speak("Order cancelled")

        threading.Thread(target=order_thread, daemon=True).start()

    def start_app(self):
        self.speak("FoodieVoice assistant ready to take your order!")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceFoodApp(root)
    
    # Configure text tags
    app.chat_log.tag_config("user", foreground="blue")
    app.chat_log.tag_config("system", foreground="green")
    
    root.mainloop()