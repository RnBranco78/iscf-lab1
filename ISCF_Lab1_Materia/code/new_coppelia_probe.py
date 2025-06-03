import sim
import time 
import requests
#change url api
API_URL = "http://127.0.0.1:8000/data/"
key = "https://api.openweathermap.org/data/2.5/weather?lat=38.661&lon=-9.2056&appid=94346c4f808479f8cf360666c2c5c3f4"
URL="https://iscf-960e0-default-rtdb.europe-west1.firebasedatabase.app/data.json"
# global configuration variables
clientID=-1

#firebase = pyrebase.initialize_app(config)
#database = firebase.database()

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
    temp = data["main"]["temp"]
    return temp

class DataCollection():
    def __init__(self):
        pass        

    def run(self):
        
        while True:
            data = {
                "x": None,
                "y": None,
                "z": None,
                "temp": None,
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

            temp = get_weather_data(key)
            if temp is not None:
                data["temp"] = temp

            print(data)

            # TODO Lab 1: Add the necessary code to send data to your API
            try:
                response = requests.post(API_URL, json=data)
                if response.status_code == 200:
                    print("Successfully Posted Data to API")
                else:
                    print(f"Error Trying to Post Data: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to Communicate to API: {e}")
            time.sleep(1)

            try:
                response = requests.get(API_URL)
                if response.status_code == 200:
                    print("Successfully Pulled Data")
                    try:
                        response1 = requests.post(URL, json=data)
                        if response1.status_code == 200:
                            print("Successfully Posted Data to FireBase")
                        else:
                            print(f"{response1.status_code},{response1.text}")
                    except requests.exceptions.RequestException as e:
                        print(f"Failed Communicating with FireBase: {e}")
                else:
                    print(f"Error Pulling Data: {response.status_code},{response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Failed Communicating with Local API: {e}")
            time.sleep(1)

if __name__ == '__main__':
    sim.simxFinish(-1) # just in case, close all opened connections
    clientID=sim.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to CoppeliaSim
    if clientID!=-1:
        data_collection = DataCollection()
        data_collection.run()      
    else:
        exit()
    