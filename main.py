import uvicorn
from enum import Enum
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Query
from fastapi import FastAPI, HTTPException, Depends, status, Request, Depends
import tensorflow as tf
import numpy as np
from starlette.responses import RedirectResponse
import os
from google.oauth2 import service_account
from google.cloud import storage
from dotenv import load_dotenv
from starlette.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import mysql.connector
from fastapi.openapi.utils import get_openapi
import secrets
from fastapi.security import HTTPBasic, HTTPBasicCredentials




# Load environment variables from .env file
load_dotenv()


# Create a new FastAPI app
app = FastAPI()

# Get the port from environment variable
port = int(os.environ.get("PORT", 8080))

# Define models for payload
class WaterItem(BaseModel):
    fc: float
    oxy: float
    ph: float
    tss: float
    temp: float
    tpn: float
    tp: float
    turb: float


class SoilItem(BaseModel):
    nitrogen: float
    phosphorus: float
    potassium: float
    ph: float


class AirItem(BaseModel):
    co: float
    ozon: float
    no2: float
    pm25: float


# Load ML models
water_model = tf.keras.models.load_model('./model/water.h5')
soil_model = tf.keras.models.load_model('./model/Soil.h5')
air_model = tf.keras.models.load_model('./model/Air.h5')


# Connect to MySQL database
mysql_host = os.environ.get("MYSQL_HOST")
mysql_user = os.environ.get("MYSQL_USER")
mysql_password = os.environ.get("MYSQL_PASSWORD")
mysql_database = os.environ.get("MYSQL_DATABASE")
mysql_connection = mysql.connector.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_password,
    database=mysql_database
)




# Check API key from MySQL
def check_api_key(api_key):
    cursor = mysql_connection.cursor()
    query = "SELECT COUNT(*) FROM user WHERE api_key = %s"
    cursor.execute(query, (api_key,))
    count = cursor.fetchone()[0]
    cursor.close()
    return count > 0

# Fungsi untuk mengambil data dari MySQL dengan memeriksa API key
def get_data_from_mysql(api_key):
    if not check_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    try:
        connection = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_database
        )
        cursor = connection.cursor()
        
        # Query MySQL untuk mengambil data
        query = "SELECT * FROM artikel ORDER BY id"
        cursor.execute(query)
        
        # Mendapatkan hasil data
        data = cursor.fetchall()
        
        # Menutup kursor dan koneksi
        cursor.close()
        connection.close()
        
        return data
        
    except mysql.connector.Error as error:
        print("Error while connecting to MySQL", error)
        return None


# Predict water quality
def predict_water_quality(fc, oxy, ph, tss, temp, tpn, tp, turb):
    res_message = "Undefined"
    data = np.array([[fc, oxy, ph, tss, temp, tpn, tp, turb]])
    result = water_model.predict(data)
    predicted_class = np.argmax(result)

    if predicted_class == 0:
        res_message = "Very Bad"
    elif predicted_class == 1:
        res_message = "Bad"
    elif predicted_class == 2:
        res_message = "Medium"
    elif predicted_class == 3:
        res_message = "Good"
    elif predicted_class == 4:
        res_message = "Excellent"

    return res_message


# Predict soil quality
def predict_soil_quality(nitrogen, phosphorus, potassium, ph):
    res_message = "Undefined"
    data = np.array([[nitrogen, phosphorus, potassium, ph]])
    result = soil_model.predict(data)
    predicted_class = np.argmax(result)

    if predicted_class == 0:
        res_message = "Tidak Sehat"
    elif predicted_class == 1:
        res_message = "Kurang Sehat"
    elif predicted_class == 2:
        res_message = "Sehat"

    return res_message


# Predict air quality
def predict_air_quality(co, ozon, no2, pm25):
    res_message = "Undefined"
    data = np.array([[co, ozon, no2, pm25]])
    result = air_model.predict(data)
    predicted_class = np.argmax(result)

    if predicted_class == 0:
        res_message = "Good"
    elif predicted_class == 1:
        res_message = "Moderate"
    elif predicted_class == 2:
        res_message = "Unhealthy for Sensitive Groups"
    elif predicted_class == 3:
        res_message = "Unhealthy"
    elif predicted_class == 4:
        res_message = "Very Unhealthy"
    elif predicted_class == 5:
        res_message = "Hazardous"

    return res_message


app.mount("/assets", StaticFiles(directory="view/assets"), name="assets")




# Model untuk payload registrasi pengguna
class UserRegistration(BaseModel):
    username: str
    password: str
    email: str

class UserLogin(BaseModel):
    username: str
    password: str

# Endpoint untuk registrasi pengguna
@app.post("/register")
def register_user(user: UserRegistration):
    try:
        # Memeriksa apakah pengguna sudah terdaftar
        cursor = mysql_connection.cursor()
        query = "SELECT COUNT(*) FROM user WHERE username = %s"
        cursor.execute(query, (user.username,))
        count = cursor.fetchone()[0]
        cursor.close()
        
        if count > 0:
            raise HTTPException(status_code=400, detail="Username already exists")

        # Membuat API key secara acak
        api_key = secrets.token_hex(16)

        # Menyimpan data pengguna dan API key ke database
        cursor = mysql_connection.cursor()
        query = "INSERT INTO user (username, password, email, api_key, level) VALUES (%s, %s, %s, %s, 'user')"
        values = (user.username, user.password, user.email, api_key)
        cursor.execute(query, values)
        mysql_connection.commit()
        cursor.close()

        return {"message": "User registered successfully", "api_key": api_key}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to register user: " + str(e))

# Endpoint untuk login pengguna
@app.post("/login")
def login_user(request: Request, credentials: UserLogin):
    try:
        # Memeriksa kredensial pengguna
        cursor = mysql_connection.cursor()
        query = "SELECT COUNT(*) FROM user WHERE username = %s AND password = %s"
        cursor.execute(query, (credentials.username, credentials.password))
        count = cursor.fetchone()[0]
        cursor.close()

        # Jika kredensial salah, raise HTTPException
        if count == 0:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        # Memeriksa level pengguna
        cursor = mysql_connection.cursor()
        query = "SELECT * FROM user WHERE username = %s"
        cursor.execute(query, (credentials.username,))
        user = cursor.fetchone()
        cursor.close()

        user_data = {
            "id": user[0],
            "username": user[1],
            "api_key": user[3],
            "email": user[4],
            "level": user[5]
        }

        # Tampilkan data pengguna dan redirect ke docs
        return user_data
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to login user: " + str(e))


# Documentation
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def welcome():
    with open("view/index.php", "r") as file:
        return file.read()

@app.get("/artikels")
def get_data(api_key: str):
    data = get_data_from_mysql(api_key)
    if data is not None:
        return {"data": data}
    else:
        return {"message": "Failed to retrieve data from MySQL"}

@app.post("/water")
def predict_water(api_key: str, item: WaterItem):
    # Check API key
    if not check_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")

    result = predict_water_quality(item.fc, item.oxy, item.ph, item.tss, item.temp, item.tpn, item.tp, item.turb)
    return {"result": result}


@app.post("/soil")
def predict_soil(api_key: str, item: SoilItem):
    # Check API key
    if not check_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")

    result = predict_soil_quality(item.nitrogen, item.phosphorus, item.potassium, item.ph)
    return {"result": result}


@app.post("/air")
def predict_air(api_key: str, item: AirItem):
    # Check API key
    if not check_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")

    result = predict_air_quality(item.co, item.ozon, item.no2, item.pm25)
    return {"result": result}

@app.get("/openapi.json", include_in_schema=False)
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="ENVy Endpoint",
        version="1.0.0",
        description="hmmm",
        routes=app.routes,
    )
    # Remove unwanted paths from the OpenAPI schema
    paths_to_exclude = ["/", "/openapi.json"]
    for path in paths_to_exclude:
        if path in openapi_schema["paths"]:
            del openapi_schema["paths"][path]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=port, timeout_keep_alive=1200)