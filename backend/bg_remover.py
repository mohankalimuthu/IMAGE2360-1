from pathlib import Path

from PIL import Image

from config import (
    UPLOAD_DIR,
    OUTPUT_DIR,
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE_MB
)

from api_client import WithoutBGClient


class BackgroundRemover:

    def __init__(self):

        self.upload_directory = Path(
            UPLOAD_DIR
        )

        self.output_directory = Path(
            OUTPUT_DIR
        )


        self.upload_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True
        )


        self.api_client = WithoutBGClient()

    def validate_file(
        self,
        file_path: str
    ):

        path = Path(
            file_path
        )


        if (
            path.suffix.lower()
            not in ALLOWED_EXTENSIONS
        ):

            raise ValueError(
                "Unsupported file type."
            )


        file_size_mb = (
            path.stat().st_size
            / (1024 * 1024)
        )


        if (
            file_size_mb
            > MAX_FILE_SIZE_MB
        ):

            raise ValueError(
                f"File size must be below "
                f"{MAX_FILE_SIZE_MB} MB."
            )

        try:

            with Image.open(
                path
            ) as image:

                image.verify()


        except Exception:

            raise ValueError(
                "Invalid or corrupted image."
            )


    def remove_background(
        self,
        input_path: str,
        output_path: str
    ):

        self.validate_file(
            input_path
        )


        result = (
            self.api_client
            .remove_car_background(
                input_path,
                output_path
            )
        )


        return result