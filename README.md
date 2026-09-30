# National ID OCR

A Python-based OCR pipeline for extracting structured data from Egyptian national ID cards. The project combines image preprocessing, contour detection, perspective correction, and OCR to detect identifying fields such as the holder name, address, national ID number, gender, and birth date.

This repository currently focuses on the backend OCR API, which exposes a FastAPI endpoint for processing uploaded card images.

## Overview

The application performs the following steps:

- Loads an uploaded image
- Preprocesses and enhances the image for detection
- Finds the card contour in the image
- Applies perspective correction to normalize the card orientation
- Isolates key regions on the ID card
- Runs OCR over those regions
- Normalizes extracted values and returns structured output

## Features

- Egyptian national ID card preprocessing and field extraction
- OCR-based text recognition for card fields
- Perspective correction for skewed or rotated images
- Structured JSON response with extracted data
- FastAPI endpoint for image upload processing
- Docker support for containerized deployment

## Tech Stack

- Python 3.13
- FastAPI
- PaddleOCR
- OpenCV (`cv2`)
- NumPy
- Streamlit (present in dependencies but not the primary runtime path in this repo)

## Project Structure

```text
National_IDOCR/
├── backend/
│   ├── api/
│   │   └── routes.py         # FastAPI routes for image processing
│   └── app/
│       └── core/
│           ├── ingestion.py  # Image loading and pipeline setup
│           ├── preprocessing.py  # Image enhancement and field extraction
│           ├── ocr.py        # OCR wrapper logic
│           ├── extractor.py  # Region extraction and value conversion
│           ├── models.py     # Data models
│           └── worker.py     # Reusable processing worker
├── frontend/
│   └── app.py                # Frontend placeholder / scaffold
├── main.py                    # Entry extraction function used by the API
├── Dockerfile                 # Container configuration
├── pyproject.toml             # Python dependencies and project metadata
├── README.md                  # Project documentation
└── notebook.ipynb             # Notebook-based experimentation
```

## Prerequisites

- Python 3.13 recommended (matches `pyproject.toml`)
- `pip` or `uv`
- A system capable of running OpenCV and PaddleOCR dependencies
- For local development, a virtual environment is recommended

## Installation

### Option 1: Using `uv` (recommended)

```bash
cd National_IDOCR
uv sync
```

### Option 2: Using `pip`

```bash
cd National_IDOCR
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

> This project is configured with `pyproject.toml` and uses `uv` in the Docker setup, so `uv sync` is the simplest path for local development.

## Running the API

From the project root:

```bash
cd National_IDOCR
uv run uvicorn backend.api.routes:app --host 0.0.0.0 --port 8000 --reload --reload-dir backend
```

Or, if your environment is already activated:

```bash
python -m uvicorn backend.api.routes:app --host 0.0.0.0 --port 8000 --reload --reload-dir backend
```

Once started, the API will be available at:

- `http://localhost:8000/` — health/root endpoint
- `http://localhost:8000/CardProcessings` — upload an ID card image

## API Endpoint

### `GET /`

Returns a simple welcome message.

Example response:

```json
{
  "message": "Welcome to the ID OCR API"
}
```

### `POST /CardProcessings`

Uploads an ID card image and returns extracted structured data.

#### Request format

- `file`: multipart form file upload

#### Example using curl

```bash
curl -X POST "http://localhost:8000/CardProcessings" \
  -F "file=@/path/to/id_card.jpg"
```

#### Example response

```json
{
  "name": "John Doe",
  "address": "123 Example Street",
  "id_number": "12345678901234",
  "factory_number": "AB12345",
  "gender": "male",
  "birth_date": "1995/07/14",
  "english_id_number": "12345678901234",
  "photo": "base64-encoded-image-data"
}
```

## Docker

The project includes a Dockerfile for containerized execution.

Build the image:

```bash
docker build -t national-idocr .
```

Run the container:

```bash
docker run -p 8000:8000 national-idocr
```

The container starts the API on port `8000` and exposes the same FastAPI endpoint described above.

## How the Extraction Pipeline Works

The OCR flow is implemented in the core processing modules:

1. `CardIngest` loads the image data.
2. `CardPreprocess` cleans and enhances the image.
3. `CardDetector` finds the card contour.
4. `CardPerspective` corrects the image orientation.
5. `ProcessCard` isolates regions such as name, address, number, and photo.
6. `PaddleOCRWrapper` performs OCR on those regions.
7. `extract_id_card()` normalizes the results into an `IDCardData` object.

## Notes and Current Status

- The project is primarily a backend OCR engine and not a full production web application UI.
- The `frontend/` directory exists as a scaffold but does not yet provide a complete user interface.
- OCR accuracy depends heavily on image quality, lighting, card orientation, and document clarity.
- Good alignment and preprocessing are essential for reliable extraction.

## License

This project does not currently declare a license in the repository metadata. If you plan to reuse or distribute it, confirm the licensing terms with the repository owner before publishing.

## Contributing

Contributions are welcome. Common improvement areas include:

- improved preprocessing for noisy or low-quality scans
- better field-region detection for edge cases
- stronger validation of OCR output
- UI improvements for image upload and result display
- better Docker and deployment configuration

## Troubleshooting

### Import errors

Make sure dependencies are installed in the active environment:

```bash
uv sync
```

### OCR performance issues

Use clearer, high-contrast ID card photos with minimal perspective distortion for best results.

### Port conflicts

If port `8000` is already used, run the app on another port:

```bash
uv run uvicorn backend.api.routes:app --host 0.0.0.0 --port 8001
```

## Summary

National ID OCR is a focused image-processing and OCR project for extracting data from Egyptian national ID cards. It is best suited for backend processing workflows, image-based automation, and integration into other applications that need structured ID card extraction.
