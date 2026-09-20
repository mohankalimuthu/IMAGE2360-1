const API_URL = "http://127.0.0.1:8000";


// --------------------------------------------------
// Elements
// --------------------------------------------------

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


// --------------------------------------------------
// Selected file
// --------------------------------------------------

let selectedFile = null;

let resultURL = null;


// --------------------------------------------------
// Image selection
// --------------------------------------------------

imageInput.addEventListener(
    "change",
    function () {

        const file =
            imageInput.files[0];


        if (!file) {

            return;
        }


        // Validate type

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


        // Validate size

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


        // Show original image

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


// --------------------------------------------------
// Remove background
// --------------------------------------------------

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


        // UI state

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


            // Result URL

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


// --------------------------------------------------
// Download
// --------------------------------------------------

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


// --------------------------------------------------
// Message
// --------------------------------------------------

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