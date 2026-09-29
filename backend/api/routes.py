from fastapi import FastAPI, File,UploadFile
from backend.app.core.models import IDCardData
from main import extract_id_card
import base64

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to the ID OCR API"}




@app.post("/CardProcessings")
async def process_card(file: UploadFile = File(...)):
    contents = await file.read()
    id_card_data = extract_id_card(contents)
    return IDCardData(
        name=id_card_data.name,
        address=id_card_data.address,
        id_number=id_card_data.id_number,
        factory_number=id_card_data.factory_number,
        gender=id_card_data.gender,
        birth_date=id_card_data.birth_date,
        english_id_number=id_card_data.english_id_number,
        photo=id_card_data.photo
    )
    