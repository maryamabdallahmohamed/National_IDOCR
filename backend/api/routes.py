from contextlib import asynccontextmanager

from fastapi import FastAPI, File, UploadFile, Request
from main import extract_id_card
from backend.app.core.worker import IDCardWorker
import base64
import cv2


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.id_card_worker = IDCardWorker()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Welcome to the ID OCR API"}




@app.post("/CardProcessings")
async def process_card(request: Request, file: UploadFile = File(...)):
    contents = await file.read()
    id_card_data = extract_id_card(contents, request.app.state.id_card_worker)

    encoded_photo = cv2.imencode(".jpg", id_card_data.photo)[1].tobytes()

    return {
        "name": id_card_data.name,
        "address": id_card_data.address,
        "id_number": id_card_data.id_number,
        "factory_number": id_card_data.factory_number,
        "gender": id_card_data.gender,
        "birth_date": id_card_data.birth_date,
        "english_id_number": id_card_data.english_id_number,
        "photo": base64.b64encode(encoded_photo).decode("ascii")
    }
    