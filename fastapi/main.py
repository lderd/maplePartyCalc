import os
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from PIL import Image
import requests
from dotenv import load_dotenv
import boto3
import secrets

app = FastAPI()
load_dotenv()

apilayer_api_key = os.environ.get("APILAYER_KEY")
aws_access_key=os.environ.get("AWS_ACCESS_KEY")
aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
bucket_name=os.environ.get("AWS_BUCKET_NAME")

@app.get("/calc", response_class=FileResponse)
def calc():
    return FileResponse("./static/calc.html")

@app.get("/word", response_class=FileResponse)
def word():
    return FileResponse("./static/word.html")

@app.get("/imgToText", response_class=FileResponse)
def ImgToText():
    return FileResponse("./static/imgToText.html")

@app.post("/imgToText")
async def ImgToTextPost(file: UploadFile):
    img = Image.open(file.file)
    filename = secrets.token_urlsafe(16) + ".png"
    img.save(f'./images/{filename}', "png")
    # s3 작업
    s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key, # 본인 소유의 키를 입력
    aws_secret_access_key=aws_secret_access_key, # 본인 소유의 키를 입력
    region_name="us-east-2",
    )
    s3_client.upload_file(f'./images/{filename}', bucket_name, filename)
    # s3 작업

    # img to text
    url = f"https://api.apilayer.com/image_to_text/url?url=https://myimagetotextproject.s3.us-east-2.amazonaws.com/{filename}"
    payload = {}
    headers= {"apikey": apilayer_api_key}
    response = requests.request("GET", url, headers=headers, data = payload).json()
    
    os.remove(f'./images/{filename}')

    return response