# import os
# import pandas as pd
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload
# from datetime import datetime

# # --- CONFIGURATION ---
# LOG_FILE_LOCAL = "guardian_log.xlsx"
# CREDS_FILE = "google_creds.json"
# SHEET_NAME = "Guardian AI Logs"
# # This is the ID from the folder link you shared
# FOLDER_ID = "1j99t0AjIVldhbrnNCdTWkSkpnDaiNQUf" 
# SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# def upload_to_drive(file_path):
#     """Uploads an image to your specific Google Drive folder."""
#     try:
#         creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
#         drive_service = build('drive', 'v3', credentials=creds)
        
#         file_metadata = {
#             'name': os.path.basename(file_path),
#             'parents': [FOLDER_ID] # This saves it into your folder
#         }
#         media = MediaFileUpload(file_path, mimetype='image/jpeg')
        
#         file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
#         file_id = file.get('id')
        
#         # This makes the link viewable in your sheet
#         drive_service.permissions().create(fileId=file_id, body={'type': 'anyone', 'role': 'reader'}).execute()
        
#         return f"https://drive.google.com/uc?id={file_id}"
#     except Exception as e:
#         print(f"❌ Drive Upload Error: {e}")
#         return "Upload Failed"

# def log_incident(user_id, input_type, verdict, severity, category, reasoning, image_path=None):
#     """Logs data to Local Excel and Cloud Sheet with image links."""
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     cloud_link = "N/A"

#     if image_path and os.path.exists(image_path):
#         print(f"🚀 Syncing image to Google Drive folder...")
#         cloud_link = upload_to_drive(image_path)

#     # 1. LOG TO LOCAL EXCEL
#     new_data = {
#         "Timestamp": [timestamp],
#         "User_ID": [str(user_id)],
#         "Type": [input_type],
#         "Verdict": [verdict],
#         "Severity": [severity],
#         "Category": [category],
#         "Reasoning": [reasoning],
#         "Image_Link": [cloud_link]
#     }
#     df_new = pd.DataFrame(new_data)

#     try:
#         if not os.path.isfile(LOG_FILE_LOCAL):
#             df_new.to_excel(LOG_FILE_LOCAL, index=False, engine='openpyxl')
#         else:
#             with pd.ExcelWriter(LOG_FILE_LOCAL, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
#                 existing_df = pd.read_excel(LOG_FILE_LOCAL)
#                 df_new.to_excel(writer, index=False, header=False, startrow=len(existing_df) + 1)
#         print("✅ Local Log Updated.")
#     except Exception as e:
#         print(f"❌ Local Excel Error: {e}")

#     # 2. LOG TO GOOGLE SHEETS
#     try:
#         creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
#         client = gspread.authorize(creds)
#         sheet = client.open(SHEET_NAME).sheet1
        
#         if not sheet.get_all_values():
#             headers = ["Timestamp", "User_ID", "Type", "Verdict", "Severity", "Category", "Reasoning", "Image_Link"]
#             sheet.append_row(headers)

#         sheet.append_row([timestamp, str(user_id), input_type, verdict, severity, category, reasoning, cloud_link])
#         print("☁️ Cloud Sheet Updated.")
#     except Exception as e:
#         print(f"❌ Google Sheets Error: {e}")




import os
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

LOG_FILE_LOCAL = "guardian_log.xlsx"
CREDS_FILE = "google_creds.json"
SHEET_NAME = "Guardian AI Logs"
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

def log_incident(user_id, input_type, verdict, severity, score, category, reasoning, image_path=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. --- LOG TO LOCAL EXCEL ---
    new_data = {
        "Timestamp": [timestamp], "User_ID": [str(user_id)], "Type": [input_type],
        "Verdict": [verdict], "Severity": [severity], "Harm_Score": [f"{score}%"],
        "Category": [category], "Reasoning": [reasoning],
        "Local_Image": [image_path if image_path else "N/A"]
    }
    df_new = pd.DataFrame(new_data)

    try:
        if not os.path.isfile(LOG_FILE_LOCAL):
            df_new.to_excel(LOG_FILE_LOCAL, index=False, engine='openpyxl')
        else:
            with pd.ExcelWriter(LOG_FILE_LOCAL, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                existing_df = pd.read_excel(LOG_FILE_LOCAL)
                df_new.to_excel(writer, index=False, header=False, startrow=len(existing_df) + 1)
        print("✅ Local Log Updated.")
    except Exception as e:
        print(f"❌ Local Excel Error: {e}")

    # 2. --- LOG TO GOOGLE SHEETS ---
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
        client = gspread.authorize(creds)
        sheet = client.open(SHEET_NAME).sheet1
        # Convert reasoning to a single string to avoid 'list_value' errors in Sheets
        clean_reasoning = str(reasoning)
        sheet.append_row([timestamp, str(user_id), input_type, verdict, severity, f"{score}%", category, clean_reasoning])
        print("☁️ Cloud Log Updated.")
    except Exception as e:
        print(f"❌ Cloud Sync Error: {e}")