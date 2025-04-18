🚦 Traffic Alert – Smart Traffic Prediction Web Application
📌 Project Overview
Traffic Alert is a smart traffic prediction system developed to enhance urban mobility by forecasting traffic conditions using machine learning. The system assists commuters in planning their journeys more efficiently by providing real-time traffic predictions. This web-based tool uses historical data and a Long Short-Term Memory (LSTM) deep learning model to provide accurate traffic forecasts.

🎯 Key Features

🔒 User Authentication – Login/Register for personalized access

📍 Input-Based Prediction – Users enter Origin, Destination, Time, and Weekday

🔁 Traffic Volume Prediction – LSTM model forecasts congestion

🗺️ Google Maps API Integration – Real-time route mapping

💻 Frontend – Built with HTML, CSS, and Bootstrap

🧠 Backend – Powered by Python, Flask, and LSTM model

🧪 Tech Stack

Frontend:

HTML5

CSS3

Bootstrap 4

Backend:

Python 3

Flask

Google Maps API

Pandas, NumPy, Keras (LSTM)

Model:

LSTM (Long Short-Term Memory) based time-series model

Trained on historical traffic data (CSV format)

## 📈 Dataset

This project uses a **custom-created dataset** using the google map API .  
In the dataset , there are main area of the Ahmedabad in gujrat.
You can find the dataset in the [data/trafficpredictiondataset](data/trafficpredictiondataset) file within this repository.



😊 Preview 

Login page

![newloginpage](https://github.com/user-attachments/assets/67e1290c-f872-485a-aca7-035dba6dbf48)

Register Page 

![newregisterpage](https://github.com/user-attachments/assets/26100dff-fbff-477d-8bbe-7933f0d77a07)

Home Page 

![newhomepage](https://github.com/user-attachments/assets/7f144815-317b-45b2-af70-7bab97bfa8db)

Prediction Page 

![newresultpage](https://github.com/user-attachments/assets/c5c60caf-d5ff-440b-ab16-6b7b7b86dc77)



## Setup & Installation 👀

To run this project, perform the following tasks 😨

Download the code file manually or via git
```bash
git clone https://github.com/Neeshi14/Traffic-Alert-.git
```

Create a virtual environment and activate it **(recommended)**

Open your command prompt and change your project directory to ```Traffic Alert``` and run the following command 
```bash
python -m venv myenv

cd myenv/Scripts

activate

```

Downloading packages from ```requirements.txt``` 

pip install -r requirements.txt

```

``Congratulations 🥳😱 your set-up 👆 and installation is finished 😵🤯``

I hope that your `myenv`` is activated and working directory 

Run the ```app.py``` file using
```cmd
python run app.py

```



