import shutil
import uuid
import os
import uvicorn
from pathlib import Path

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)

from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import FileResponse

from bg_remover import BackgroundRemover

app = FastAPI(
    title="IMG2360 AI Car Background Remover",
    description=(
        "AI-powered car background removal "
        "using WithoutBG API"
    ),
    version="1.0.0"
)


# ==================================================
# CORS
# ==================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)

UPLOAD_DIR = Path(
    "uploads"
)

OUTPUT_DIR = Path(
    "outputs"
)


UPLOAD_DIR.mkdir(
    exist_ok=True
)

OUTPUT_DIR.mkdir(
    exist_ok=True
)


try:

    remover = BackgroundRemover()

    print(
        "WithoutBG client initialized successfully."
    )


except Exception as error:

    remover = None

    print(
        f"Background remover initialization error: "
        f"{error}"
    )

@app.get("/")
def home():

    return {

        "status":
            "success",

        "project":
            "IMG2360",

        "service":
            "WithoutBG",

        "message":
            "AI Car Background Remover API is running"
    }

@app.get("/health")
def health():

    return {

        "status":
            "healthy",

        "background_remover":
            remover is not None
    }

@app.post(
    "/remove-background"
)
async def remove_background(

    file: UploadFile =
        File(...)
):

    if remover is None:

        raise HTTPException(

            status_code=500,

            detail=(
                "Background remover is not "
                "configured. Check API key."
            )
        )


    allowed_types = {

        "image/jpeg",

        "image/png",

        "image/webp",

        "image/avif",

        "image/heic",

        "image/tiff",

        "image/bmp",

        "image/gif"
    }


    if (
        file.content_type
        not in allowed_types
    ):

        raise HTTPException(

            status_code=400,

            detail=(
                "Unsupported image format."
            )
        )

    file_id = uuid.uuid4().hex


    extension = (
        Path(
            file.filename or ""
        ).suffix.lower()
    )


    if not extension:

        extension = ".jpg"


    input_filename = (
        f"{file_id}{extension}"
    )


    output_filename = (
        f"{file_id}_car_cutout.png"
    )


    input_path = (
        UPLOAD_DIR
        / input_filename
    )


    output_path = (
        OUTPUT_DIR
        / output_filename
    )


    try:


        with open(
            input_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )


        result = (
            remover.remove_background(

                str(input_path),

                str(output_path)
            )
        )


        # ------------------------------------------
        # Response
        # ------------------------------------------

        return {

            "success":
                True,

            "message":
                "Car background removed successfully.",

            "filename":
                output_filename,

            "download_url":
                f"/download/{output_filename}",

            "preview_url":
                f"/download/{output_filename}",

            "input_dimensions":
                result.get(
                    "input_dimensions"
                ),

            "processed_dimensions":
                result.get(
                    "processed_dimensions"
                ),

            "was_downscaled":
                result.get(
                    "was_downscaled"
                ),

            "shadow_type":
                result.get(
                    "shadow_type"
                )
        }


    except ValueError as error:

        raise HTTPException(

            status_code=400,

            detail=str(error)
        )


    except RuntimeError as error:

        raise HTTPException(

            status_code=502,

            detail=str(error)
        )


    except Exception as error:

        print(
            f"Unexpected processing error: "
            f"{error}"
        )


        raise HTTPException(

            status_code=500,

            detail=(
                "Unexpected error while "
                "processing the image."
            )
        )


    finally:

        if input_path.exists():

            try:

                input_path.unlink()

            except Exception:

                pass

@app.get(
    "/download/{filename}"
)
def download_file(
    filename: str
):

    file_path = (
        OUTPUT_DIR
        / filename
    )


    if not file_path.exists():

        raise HTTPException(

            status_code=404,

            detail="File not found."
        )


    return FileResponse(

        path=file_path,

        media_type="image/png",

        filename=filename
    )

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )