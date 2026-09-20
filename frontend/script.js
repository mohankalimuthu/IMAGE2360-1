const API_URL = "https://image2360-1-ai.onrender.com";

const imageInput =
    document.getElementById("imageInput");

const uploadSection =
    document.getElementById("uploadSection");

const previewSection =
    document.getElementById("previewSection");

const originalImage =
    document.getElementById("originalImage");

const resultImage =
    document.getElementById("resultImage");

const removeButton =
    document.getElementById("removeButton");

const downloadButton =
    document.getElementById("downloadButton");

const loading =
    document.getElementById("loading");

const message =
    document.getElementById("message");

let selectedFile = null;

let resultURL = null;

imageInput.addEventListener(
    "change",
    function () {

        const file =
            imageInput.files[0];


        if (!file) {

            return;
        }


        const allowedTypes = [
            "image/jpeg",
            "image/png",
            "image/webp"
        ];


        if (
            !allowedTypes.includes(
                file.type
            )
        ) {

            showMessage(
                "Please select JPG, JPEG, PNG or WEBP.",
                "error"
            );

            return;
        }

        const maxSize =
            10 * 1024 * 1024;


        if (
            file.size > maxSize
        ) {

            showMessage(
                "Image must be below 10 MB.",
                "error"
            );

            return;
        }


        selectedFile =
            file;

        const imageURL =
            URL.createObjectURL(file);


        originalImage.src =
            imageURL;


        previewSection.classList.remove(
            "hidden"
        );


        removeButton.disabled =
            false;


        downloadButton.classList.add(
            "hidden"
        );


        resultImage.src =
            "";


        showMessage(
            "",
            ""
        );

    }
);

removeButton.addEventListener(
    "click",
    async function () {

        if (!selectedFile) {

            showMessage(
                "Please select an image first.",
                "error"
            );

            return;
        }


        const formData =
            new FormData();


        formData.append(
            "file",
            selectedFile
        );


        removeButton.disabled =
            true;

        loading.classList.remove(
            "hidden"
        );


        showMessage(
            "",
            ""
        );


        try {

            const response =
                await fetch(
                    `${API_URL}/remove-background`,
                    {
                        method: "POST",
                        body: formData
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Background removal failed."
                );
            }

            resultURL =
                `${API_URL}${data.download_url}`;


            resultImage.src =
                resultURL;


            downloadButton.classList.remove(
                "hidden"
            );


            showMessage(
                "Background removed successfully!",
                "success"
            );


        } catch (error) {

            console.error(
                error
            );


            showMessage(
                error.message ||
                "Server error. Make sure FastAPI is running.",
                "error"
            );

        } finally {

            loading.classList.add(
                "hidden"
            );

            removeButton.disabled =
                false;
        }

    }
);

downloadButton.addEventListener(
    "click",
    function () {

        if (!resultURL) {

            return;
        }


        const link =
            document.createElement("a");


        link.href =
            resultURL;

        link.download =
            "img2360_background_removed.png";


        document.body.appendChild(
            link
        );


        link.click();


        document.body.removeChild(
            link
        );

    }
);

function showMessage(
    text,
    type
) {

    message.textContent =
        text;


    if (type === "error") {

        message.style.color =
            "#dc2626";

    } else if (
        type === "success"
    ) {

        message.style.color =
            "#16a34a";

    } else {

        message.style.color =
            "";
    }

}