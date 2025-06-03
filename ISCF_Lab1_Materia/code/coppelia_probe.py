import sim
import time 
import requests

api_url = "http://127.0.0.1:8000/data/"
#url = "https://iscf-960e0-default-rtdb.europe-west1.firebasedatabase.app/"
key = "https://api.openweathermap.org/data/2.5/weather?lat=38.661&lon=-9.2056&appid=94346c4f808479f8cf360666c2c5c3f4"

# global configuration variables
clientID=-1

# Helper function provided by the teaching staff
def get_data_from_simulation(id):
    """Connects to the simulation and gets a float signal value

    Parameters
    ----------
    id : str
        The signal id in CoppeliaSim

    Returns
    -------
    data : float
        The float value retrieved from the simulation. None if retrieval fails.
    """
    if clientID!=-1:
        res, data = sim.simxGetFloatSignal(clientID, id, sim.simx_opmode_blocking)
        if res==sim.simx_return_ok:
            return data
    return None

def get_weather_data(key):
    response = requests.get(key)
    data = response.json()
    country = data["sys"]["country"]
    city = data["name"]
    temperature = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    temp_min = data["main"]["temp_min"]
    temp_max = data["main"]["temp_max"]
    return {
        "Country": country,
        "City": city,
        "Current Temperature": temperature,
        "Feels Like": feels_like,
        "Minimum Temperature": temp_min,
        "Maximum Temperature": temp_max
    }

class DataCollection():
    def __init__(self):
        pass        

    def run(self):
        
        while True:
            data = {
                "x": None,
                "y": None,
                "z": None,
                "weather": None,
                "timestamp": time.time()
            }
            
            x = get_data_from_simulation("accelX")            
            if x is not None:
                data["x"] = x
            
            y = get_data_from_simulation("accelY")
            if y is not None:
                data["y"] = y

            z = get_data_from_simulation("accelZ")
            if z is not None:
                data["z"] = z

            weather = get_weather_data(key)
            if weather is not None:
                data["weather"] = weather
            
            print(data)

            # TODO Lab 1: Add the necessary code to send data to your API
            try:
                response = requests.post(api_url, json=data)
                if response.status_code == 200:
                    print("Posted Data to Local API")
                else:
                    print("Error Trying to Post")
            except requests.exceptions.RequestException as e:
                print(f"Failure to Communicate with API: {e}")
            time.sleep(1)

if __name__ == '__main__':
    sim.simxFinish(-1) # just in case, close all opened connections
    clientID=sim.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to CoppeliaSim
    if clientID!=-1:
        data_collection = DataCollection()
        data_collection.run()      
    else:
        exit()
    