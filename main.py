import uvicorn
from enum import Enum
import datetime
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Query
from fastapi import FastAPI, HTTPException, Depends, status, Request, Depends
import tensorflow as tf
import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
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
water_model = tf.keras.models.load_model('./model/Water.h5')
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
# Mengatur CORS (Cross-Origin Resource Sharing) untuk mengizinkan permintaan dari semua sumber (origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Memuat konfigurasi dari file .env
load_dotenv()

# Konfigurasi Google Cloud Storage
bucket_name = os.getenv("BUCKET_NAME")
service_account_file = os.getenv("SERVICE_ACCOUNT_FILE")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath(service_account_file)

storage_client = storage.Client()

# Konfigurasi MySQL
mysql_host = os.getenv("MYSQL_HOST")
mysql_user = os.getenv("MYSQL_USER")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_database = os.getenv("MYSQL_DATABASE")

# Model untuk data artikel
class Article(BaseModel):
    title: str
    content: str

# Fungsi untuk mengunggah file ke Google Cloud Storage
def upload_to_gcs(file: UploadFile):
    # Generate nama file unik dengan timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    file_name = f"{timestamp}-{file.filename}"

    # Upload file ke Google Cloud Storage
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_file(file.file, content_type=file.content_type)

    # Dapatkan URL publik gambar
    url = blob.public_url

    return url

# Fungsi untuk menyimpan data artikel ke database
def save_article_to_database(title: str, content: str, image_url: str):
    connection = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )
    cursor = connection.cursor()

    # Query untuk menyimpan data artikel ke tabel "articles"
    query = "INSERT INTO artikel (title, content, image_url) VALUES (%s, %s, %s)"
    values = (title, content, image_url)

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()

# Check API key from MySQL
def check_api_key(api_key):
    cursor = mysql_connection.cursor()
    query = "SELECT COUNT(*), level FROM user WHERE api_key = %s GROUP BY level LIMIT 1;"
    cursor.execute(query, (api_key,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        count, level = result
        return count > 0, level
    else:
        return False, None

#artikel
@app.post("/upload-article")
async def upload_article_with_curl(api_key: str, title: str, content: str, file: UploadFile = File(...)):
    success, level = check_api_key(api_key)
    if not success or level != "admin":
        raise HTTPException(status_code=403, detail="Insufficient privileges")

    try:
        # Membuat instance Article dari data yang diterima
        article = Article(title=title, content=content)

        # Mengunggah gambar ke Google Cloud Storage
        image_url = upload_to_gcs(file)

        # Menyimpan data artikel ke database
        save_article_to_database(article.title, article.content, image_url)

        return {"message": "Artikel berhasil diunggah"}
    except Exception as e:
        return {"message": str(e)}

# fungsi untuk menghapus gambar dari bucket
def delete_from_gcs(image_url: str):
    # Dapatkan nama file dari URL gambar
    file_name = image_url.split("/")[-1]

    # Hapus file dari Google Cloud Storage
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.delete()

# fungsi untuk menghapus artikel dari database dan menghapus gambar
def delete_article_from_database(article_id: int):
    connection = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )
    cursor = connection.cursor()

    # Dapatkan URL image artikel yang akan dihapus
    query = "SELECT image_url FROM artikel WHERE id = %s"
    cursor.execute(query, (article_id,))
    result = cursor.fetchone()
    if result:
        image_url = result[0]
        # Hapus artikel dari database
        query = "DELETE FROM artikel WHERE id = %s"
        cursor.execute(query, (article_id,))
        connection.commit()
        cursor.close()
        connection.close()
        # Hapus gambar dari bucket
        delete_from_gcs(image_url)
    else:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Article not found")

# hapus artikel
@app.delete("/artikels/{artikel_id}")
def delete_artikel(artikel_id: int, api_key: str):
    # Periksa API key
    if not check_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")

    try:
        # Hapus artikel dari database dan gambar dari bucket
        delete_article_from_database(artikel_id)
        return {"message": "Artikel berhasil dihapus"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# update artikel
@app.put("/artikels/{artikel_id}")
def update_artikel(artikel_id: int, api_key: str, title: str, content: str, file: UploadFile = File(None)):
    # Periksa kunci API
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

        # Dapatkan artikel yang akan diperbarui dari database
        query = "SELECT * FROM artikel WHERE id = %s"
        cursor.execute(query, (artikel_id,))
        artikel = cursor.fetchone()

        if artikel is None:
            raise HTTPException(status_code=404, detail="Artikel not found")

        # Perbarui judul dan konten artikel
        query = "UPDATE artikel SET title = %s, content = %s"
        values = (title, content)

        # Perbarui gambar artikel jika ada
        if file is not None:
            # Menghapus gambar sebelumnya dari bucket
            if artikel[3]:
                delete_from_gcs(artikel[3])

            # Mengunggah gambar baru ke Google Cloud Storage
            image_url = upload_to_gcs(file)

            # Perbarui URL gambar di database
            query += ", image_url = %s"
            values += (image_url,)
        
        query += " WHERE id = %s"
        values += (artikel_id,)
        
        cursor.execute(query, values)
        connection.commit()

        # Tutup kursor dan koneksi
        cursor.close()
        connection.close()

        return {"message": "Artikel updated successfully"}
    except mysql.connector.Error as error:
        print("Error while connecting to MySQL", error)
        raise HTTPException(status_code=500, detail="Failed to update artikel")

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

# mendapatkan data artikel
@app.get("/artikels")
def get_data(api_key: str):
    data = get_data_from_mysql(api_key)
    if data is not None:
        return {"data": data}
    else:
        return {"message": "Failed to retrieve data from MySQL"}

# Predict water quality
def predict_water_quality(fc, oxy, ph, tss, temp, tpn, tp, turb):
    res_message = "Undefined"
    data = np.array([[fc, oxy, ph, tss, temp, tpn, tp, turb]])
    result = water_model.predict(data)
    predicted_class = np.argmax(result)

    #if predicted_class == 0:
        #res_message = "Very Bad"
    if predicted_class == 0:
        res_message = "Bad"
    elif predicted_class == 1:
        res_message = "Medium"
    elif predicted_class == 2:
        res_message = "Good"
    elif predicted_class == 3:
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
    #elif predicted_class == 2:
        #res_message = "Sehat"

    return res_message


# Predict air quality
def predict_air_quality(co, ozon, no2, pm25):
    res_message = "Undefined"
    data = np.array([[co, ozon, no2, pm25]])
    result = air_model.predict(data)
    predicted_class = np.argmax(result)

    if predicted_class == 5:
        res_message = "Good"
    elif predicted_class == 4:
        res_message = "Moderate"
    elif predicted_class == 3:
        res_message = "Unhealthy for Sensitive Groups"
    elif predicted_class == 2:
        res_message = "Unhealthy"
    elif predicted_class == 1:
        res_message = "Very Unhealthy"
    elif predicted_class == 0:
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
        description="Capstone Project Bangkit 2023 - ENVy",
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