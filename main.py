import requests
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import io

API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

def get_clothing_recommendation(temp_celsius, description):
    if 'rain' in description or 'drizzle' in description:
        if temp_celsius < 20:
            return "Wear a raincoat and carry an umbrella!"
        else:
            return "Carry an umbrella, and wear light waterproof clothing."
    elif 'snow' in description:
        return "Wear a warm coat, gloves, and boots!"
    elif temp_celsius < 10:
        return "Wear a heavy jacket, scarf, and gloves!"
    elif 10 <= temp_celsius <= 20:
        return "Wear a light jacket or hoodie."
    elif 20 < temp_celsius <= 30:
        return "T-shirt and jeans should be fine."
    else:
        return "It's hot! Wear light clothes and stay hydrated."

def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    url = BASE_URL + f"q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            messagebox.showerror("Error", f"City not found: {city}")
            return

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        icon_code = data["weather"][0]["icon"]

        recommendation = get_clothing_recommendation(temp, desc)

        weather_info.set(f"Temperature: {temp}°C\n"
                         f"Description: {desc.title()}\n"
                         f"Humidity: {humidity}%\n\n"
                         f"👕 Outfit Tip: {recommendation}")

        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        icon_data = Image.open(io.BytesIO(icon_response.content))
        icon_image = ImageTk.PhotoImage(icon_data)
        icon_label.config(image=icon_image)
        icon_label.image = icon_image

    except Exception as e:
        messagebox.showerror("Error", f"Failed to get weather: {str(e)}")

root = Tk()
root.title("🌦️ Weather-Based Clothing Recommender")
root.geometry("400x500")
root.config(bg="#e1f5fe")

Label(root, text="Enter City Name:", font=("Arial", 14), bg="#e1f5fe").pack(pady=10)
city_entry = Entry(root, font=("Arial", 14), width=25)
city_entry.pack(pady=5)
Button(root, text="Get Weather", font=("Arial", 12, "bold"),
       bg="#29b6f6", fg="white", command=get_weather).pack(pady=10)
icon_label = Label(root, bg="#e1f5fe")
icon_label.pack()
weather_info = StringVar()
Label(root, textvariable=weather_info, font=("Arial", 12), bg="#e1f5fe", wraplength=350, justify="left").pack(pady=10)

root.mainloop()
