import requests

from config import (
    WITHOUTBG_API_KEY,
    WITHOUTBG_CAR_URL
)


class WithoutBGClient:

    def __init__(self):

        if not WITHOUTBG_API_KEY:

            raise ValueError(
                "WITHOUTBG_API_KEY is missing. "
                "Add it to the .env file."
            )

        self.api_key = WITHOUTBG_API_KEY


    def remove_car_background(
        self,
        image_path: str,
        output_path: str
    ):

        try:

            with open(
                image_path,
                "rb"
            ) as image_file:

                response = requests.post(

                    WITHOUTBG_CAR_URL,

                    headers={
                        "X-API-Key":
                            self.api_key
                    },

                    files={
                        "file":
                            image_file
                    },

                    data={

                        "shadow_type":
                            "none",


                        "reconstruct_windows":
                            "true"
                    },

                    timeout=180
                )


        except requests.exceptions.Timeout:

            raise RuntimeError(
                "WithoutBG API request timed out."
            )


        except requests.exceptions.RequestException as error:

            raise RuntimeError(
                f"WithoutBG connection error: {error}"
            )


        if response.status_code != 200:

            if response.status_code == 401:

                raise RuntimeError(
                    "Invalid WithoutBG API key."
                )

            elif response.status_code == 402:

                raise RuntimeError(
                    "WithoutBG credits are insufficient."
                )

            elif response.status_code == 403:

                raise RuntimeError(
                    "WithoutBG credits have expired."
                )

            elif response.status_code == 413:

                raise RuntimeError(
                    "Image is larger than 20 MB."
                )

            elif response.status_code == 415:

                raise RuntimeError(
                    "Unsupported image format."
                )

            elif response.status_code == 422:

                raise RuntimeError(
                    "WithoutBG rejected the request."
                )

            elif response.status_code == 429:

                raise RuntimeError(
                    "WithoutBG rate limit reached. "
                    "Please try again later."
                )

            else:

                raise RuntimeError(
                    f"WithoutBG API error: "
                    f"{response.status_code} - "
                    f"{response.text}"
                )


        with open(
            output_path,
            "wb"
        ) as output_file:

            output_file.write(
                response.content
            )


        return {
            "output_path": output_path,

            "input_dimensions":
                response.headers.get(
                    "X-Input-Dimensions"
                ),

            "processed_dimensions":
                response.headers.get(
                    "X-Processed-Dimensions"
                ),

            "was_downscaled":
                response.headers.get(
                    "X-Was-Downscaled"
                ),

            "shadow_type":
                response.headers.get(
                    "X-Shadow-Type"
                )
        }