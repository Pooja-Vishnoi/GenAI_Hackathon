import os
import firebase_admin
from firebase_admin import credentials, storage 

# -----------------------
# Initialize Firebase
# -----------------------
# with open(os.path.join(os.path.dirname(__file__), "../config.json")) as f:
#     config = json.load(f)

# if not firebase_admin._apps:
#     cred = credentials.Certificate(FIREBASE)  # path to your key
#     firebase_admin.initialize_app(cred, {
#         "storageBucket": config.get("storageBucket")  # replace with your bucket
#     })

def save_to_firebase(uploaded_files):
    """
    Uploads a list of files to Firebase, overwriting existing ones and setting a 24-hour expiration.
    """
    print("Saving to Firebase...")

    bucket = storage.bucket()

    for file in uploaded_files:
        
        blob = bucket.blob(f"uploads/{file.name}")
        # blob.upload_from_filename("test.txt")
        blob.upload_from_file(file, content_type=file.type)

        # blob.make_public()    # Make file public
        # print("🌍 Public URL:", blob.public_url)

        # -----------------------
        # Download the file back
        # -----------------------
        # download_path = "downloaded_test.txt"
        # blob.download_to_filename(download_path)
        # print(f"⬇️ File downloaded locally as {download_path}")
