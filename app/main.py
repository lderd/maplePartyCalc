import os
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from PIL import Image
import requests
import boto3
import secrets
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    apilayer_api_key: str = Field("", alias="APILAYER_KEY")
    aws_access_key: str = ""
    aws_secret_access_key: str = ""
    bucket_name: str = Field("", alias="AWS_BUCKET_NAME")
    dirname: str = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__))))


settings = Settings()

app = FastAPI()


@app.get("/calc", response_class=FileResponse)
def calc():
    return FileResponse(f"{settings.dirname}/static/calc.html")

@app.get("/word", response_class=FileResponse)
def word():
    return FileResponse(f"{settings.dirname}/static/word.html")

@app.get("/allinone", response_class=FileResponse)
def word():
    return FileResponse(f"{settings.dirname}/static/allInOne.html")

@app.get("/imgToText", response_class=FileResponse)
def ImgToText():
    return FileResponse(f"{settings.dirname}/static/imgToText.html")

@app.post("/imgToText")
async def ImgToTextPost(file: UploadFile):
    try :
        img = Image.open(file.file)
        filename = secrets.token_urlsafe(16) + ".png"
        img.save(f'{settings.dirname}/images/{filename}', "png")
        # s3 작업
        s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.aws_access_key, # 본인 소유의 키를 입력
        aws_secret_access_key=settings.aws_secret_access_key, # 본인 소유의 키를 입력
        region_name="us-east-2",
        )
        s3_client.upload_file(f'{settings.dirname}/images/{filename}', settings.bucket_name, filename)
        # s3 작업

        # img to text
        url = f"https://api.apilayer.com/image_to_text/url?url=https://myimagetotextproject.s3.us-east-2.amazonaws.com/{filename}"
        payload = {}
        headers= {"apikey": settings.apilayer_api_key}
        response = requests.request("GET", url, headers=headers, data = payload).json()
        
        os.remove(f'{settings.dirname}/images/{filename}')
    except :
        return {"all_text": "문제가 발생했습니다 다시 시도해 주세요"}

    return response