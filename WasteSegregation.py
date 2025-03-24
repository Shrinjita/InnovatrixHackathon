import streamlit as st
from PIL import Image
import io
from inference_sdk import InferenceHTTPClient

# --------------------------- #
# 🌍 ROBOFLOW INFERENCE CONFIG #
# --------------------------- #

# Initialize Roboflow Inference Client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="Kp1AqMurWRBXStFinPNM"   # Your Roboflow API Key
)

MODEL_ID = "waste-classification-uwqfy/1"  # Model ID and version


def waste_segregation():
    """Waste Segregation using Roboflow Inference SDK"""
    
    st.title("♻️ Waste Segregation Module")
    st.markdown("Upload an image of waste to classify it into categories using Roboflow Inference SDK.")

    # Upload Image
    uploaded_file = st.file_uploader("Upload Waste Image", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Convert image to bytes
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="JPEG")
        image_bytes = image_bytes.getvalue()

        # Save image temporarily for inference
        temp_image_path = "temp_image.jpg"
        with open(temp_image_path, "wb") as f:
            f.write(image_bytes)

        # Perform inference using Roboflow SDK
        with st.spinner("Classifying... 🔥"):
            try:
                result = CLIENT.infer(temp_image_path, model_id=MODEL_ID)

                # Parse Roboflow Inference Result
                predictions = result.get("predictions", [])

                if predictions:
                    # Display all detections
                    for idx, pred in enumerate(predictions):
                        class_name = pred.get("class", "Unknown")
                        confidence = pred.get("confidence", 0) * 100

                        st.subheader(f"Prediction {idx + 1}: {class_name}")
                        st.info(f"Confidence: {confidence:.2f}%")

                        # Recycling guidelines
                        guidelines = {
                            "Organic": "Compost or use as fertilizer.",
                            "Plastic": "Recycle at a plastic waste facility.",
                            "Metal": "Send to a scrap metal collection center.",
                            "Paper": "Recycle in paper mills.",
                            "E-waste": "Dispose at authorized e-waste centers.",
                            "Glass": "Recycle at glass recycling facilities."
                        }

                        if class_name in guidelines:
                            st.write(f"**Recycling Tip:** {guidelines[class_name]}")
                        else:
                            st.warning("No recycling tip available for this category.")
                else:
                    st.warning("No waste detected in the image.")

            except Exception as e:
                st.error(f"An error occurred: {e}")

        # Clean up temporary image
        import os
        os.remove(temp_image_path)
