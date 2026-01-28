# import os
# import logging
# from dotenv import load_dotenv
# from telegram import Update
# from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# # Import our AI engines
# from ai_engine_gemini import analyze_with_gemini
# from ai_engine_cnn import CNNBullyingDetector
# # Import the logger service
# from logger_service import log_incident

# # --- Setup ---
# load_dotenv()
# BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# IMAGE_FOLDER = "logged_images"

# # Create image folder if it doesn't exist
# if not os.path.exists(IMAGE_FOLDER):
#     os.makedirs(IMAGE_FOLDER)

# # Enable logging
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )
# logger = logging.getLogger(__name__)

# # Initialize CNN engine
# cnn_detector = CNNBullyingDetector()

# # --- Helper Function ---
# def format_response(analysis_json):
#     if not analysis_json:
#         return "⚠️ Guardian AI encountered an error during analysis. Please try again."

#     emoji = "🟢"
#     if analysis_json.get('is_bullying'):
#         sev = analysis_json.get('severity', 'Low').lower()
#         emoji = "🔴" if sev in ['high', 'critical'] else "🟠"

#     response = f"{emoji} **Guardian AI Analysis**\n\n"
#     response += f"**Verdict:** {'Cyberbullying Detected' if analysis_json['is_bullying'] else 'No Bullying Detected'}\n"
#     response += f"**Severity:** {analysis_json.get('severity', 'None')}\n"
#     response += f"**Category:** {analysis_json.get('category', 'None')}\n\n"
#     response += f"**📝 Analysis:**\n{analysis_json.get('reasoning', 'No reasoning provided.')}\n"
    
#     if analysis_json['is_bullying']:
#         response += "\n⚠️ *This incident has been logged. Please consider reporting this content.*"
        
#     return response

# # --- Bot Command Handlers ---

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Greets the user and explains the bot."""
#     user_name = update.effective_user.first_name
#     msg = (f"Hello {user_name}! I am **Guardian AI** 🛡️\n\n"
#            "I monitor real-time cyberbullying using Hybrid AI.\n"
#            "1. Send me any text to check for harmful intent.\n"
#            "2. Upload a chat screenshot, and I will analyze the context.")
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='Markdown')

# async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Handles text analysis and dual-logging."""
#     user_text = update.message.text
#     chat_id = update.effective_chat.id
    
#     status = await context.bot.send_message(chat_id=chat_id, text="🔍 Analyzing text with Hybrid AI...")

#     # Quick CNN check (for your project logs)
#     cnn_score = cnn_detector.predict_text(user_text)
#     logger.info(f"CNN Score: {cnn_score}")

#     # Deep Gemini Analysis
#     analysis = await analyze_with_gemini(text_input=user_text)
    
#     if analysis and analysis.get('is_bullying'):
#         log_incident(
#             user_id=update.effective_user.id,
#             input_type="Text",
#             verdict="Bullying Detected",
#             severity=analysis['severity'],
#             category=analysis['category'],
#             reasoning=analysis['reasoning']
#         )

#     reply = format_response(analysis)
#     await context.bot.delete_message(chat_id=chat_id, message_id=status.message_id)
#     await context.bot.send_message(chat_id=chat_id, text=reply, parse_mode='Markdown')

# async def handle_photo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Handles image analysis, cloud upload, and cleanup."""
#     chat_id = update.effective_chat.id
#     status = await context.bot.send_message(chat_id=chat_id, text="📥 Processing image and context...")

#     try:
#         # Download photo
#         photo_file = await update.message.photo[-1].get_file()
#         file_path = os.path.join(IMAGE_FOLDER, f"{photo_file.file_id}.jpg")
#         await photo_file.download_to_drive(file_path)

#         # Gemini Multimodal Analysis
#         analysis = await analyze_with_gemini(image_path=file_path)

#         if analysis and analysis.get('is_bullying'):
#             # This logs to Excel/Sheets AND uploads the image to Google Drive
#             log_incident(
#                 user_id=update.effective_user.id,
#                 input_type="Image",
#                 verdict="Bullying Detected",
#                 severity=analysis['severity'],
#                 category=analysis['category'],
#                 reasoning=analysis['reasoning'],
#                 image_path=file_path
#             )
#             # CLEANUP: Delete local image after cloud upload to save space
#             if os.path.exists(file_path):
#                 os.remove(file_path)
#                 logger.info(f"🗑️ Local image {file_path} deleted after cloud sync.")

#         reply = format_response(analysis)
#         await context.bot.delete_message(chat_id=chat_id, message_id=status.message_id)
#         await context.bot.send_message(chat_id=chat_id, text=reply, parse_mode='Markdown')

#     except Exception as e:
#         logger.error(f"Image Error: {e}")
#         await context.bot.edit_message_text(chat_id=chat_id, message_id=status.message_id, text="❌ Failed to process the image.")

# # --- Execution ---
# if __name__ == '__main__':
#     application = ApplicationBuilder().token(BOT_TOKEN).build()

#     application.add_handler(CommandHandler('start', start))
#     application.add_handler(MessageHandler(filters.Regex(r'(?i)^(hi|hello|hey)$'), start))
#     application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text_message))
#     application.add_handler(MessageHandler(filters.PHOTO, handle_photo_message))

#     print("🛡️ Guardian AI Pro (v2026) is Online...")
#     application.run_polling()




# import os
# import logging
# from dotenv import load_dotenv
# from telegram import Update
# from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# # Import our AI engines
# from ai_engine_gemini import analyze_with_gemini
# from ai_engine_cnn import CNNBullyingDetector
# # Import the logger service
# from logger_service import log_incident

# # --- Setup ---
# load_dotenv()
# BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# IMAGE_FOLDER = "logged_images"

# # Ensure image folder exists
# if not os.path.exists(IMAGE_FOLDER):
#     os.makedirs(IMAGE_FOLDER)

# # Enable detailed logging in your terminal
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )
# logger = logging.getLogger(__name__)

# # Initialize CNN legacy engine
# cnn_detector = CNNBullyingDetector()

# # --- Helper Function: Format Bot Response ---
# def format_response(analysis_json):
#     """Formats the JSON result into a clean, human-readable message."""
#     if not analysis_json:
#         return "⚠️ Guardian AI encountered an error. Please check your API connection."

#     emoji = "🟢"
#     if analysis_json.get('is_bullying'):
#         sev = str(analysis_json.get('severity', 'Low')).lower()
#         emoji = "🔴" if sev in ['high', 'critical'] else "🟠"

#     # Using standard text to avoid "Parse Entity" errors in Telegram
#     response = f"{emoji} GUARDIAN AI VERDICT\n\n"
#     response += f"Verdict: {'Cyberbullying Detected' if analysis_json['is_bullying'] else 'No Bullying Detected'}\n"
#     response += f"Severity: {analysis_json.get('severity', 'None')}\n"
#     response += f"Category: {analysis_json.get('category', 'None')}\n\n"
#     response += f"Detailed Analysis: {analysis_json.get('reasoning', 'N/A')}"
    
#     return response

# # --- Bot Handlers ---

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Greets the user and explains the bot's purpose."""
#     user_name = update.effective_user.first_name
#     msg = (f"Hello {user_name}! I am Guardian AI 🛡️\n\n"
#            "I monitor real-time cyberbullying using Hybrid AI.\n"
#            "1. Send me any text to check for harmful intent.\n"
#            "2. Upload a chat screenshot for deep context analysis.")
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

# async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Analyzes text and logs bullying incidents to Local + Cloud."""
#     user_text = update.message.text
#     chat_id = update.effective_chat.id
    
#     status = await context.bot.send_message(chat_id=chat_id, text="🔍 Analyzing text with Hybrid AI...")

#     # Quick CNN check (for local project logs/metrics)
#     cnn_score = cnn_detector.predict_text(user_text)
#     logger.info(f"CNN Bullying Probability: {cnn_score:.4f}")

#     # Deep Analysis with Gemini Pro
#     analysis = await analyze_with_gemini(text_input=user_text)
    
#     if analysis and analysis.get('is_bullying'):
#         log_incident(
#             user_id=update.effective_user.id,
#             input_type="Text",
#             verdict="Bullying Detected",
#             severity=analysis['severity'],
#             category=analysis['category'],
#             reasoning=analysis['reasoning']
#         )

#     reply = format_response(analysis)
#     await context.bot.delete_message(chat_id=chat_id, message_id=status.message_id)
#     await context.bot.send_message(chat_id=chat_id, text=reply)

# async def handle_photo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Handles images, uploads to Cloud Drive, logs data, and cleans up local storage."""
#     chat_id = update.effective_chat.id
#     status = await context.bot.send_message(chat_id=chat_id, text="📥 Processing image and context...")

#     try:
#         # 1. Download the photo locally
#         photo_file = await update.message.photo[-1].get_file()
#         file_path = os.path.join(IMAGE_FOLDER, f"{photo_file.file_id}.jpg")
#         await photo_file.download_to_drive(file_path)

#         # 2. Analyze the image with Gemini
#         analysis = await analyze_with_gemini(image_path=file_path)

#         if analysis:
#             # 3. Log to Excel + Google Sheets (Includes Drive Upload)
#             log_incident(
#                 user_id=update.effective_user.id,
#                 input_type="Image",
#                 verdict="Bullying Detected" if analysis['is_bullying'] else "Safe",
#                 severity=analysis['severity'],
#                 category=analysis['category'],
#                 reasoning=analysis['reasoning'],
#                 image_path=file_path
#             )
            
#             # 4. STORAGE CLEANUP: Delete local image after it is safe in the Cloud
#             if os.path.exists(file_path):
#                 os.remove(file_path)
#                 logger.info(f"🗑️ Space Saved: Local image {file_path} deleted after cloud sync.")

#         reply = format_response(analysis)
#         await context.bot.delete_message(chat_id=chat_id, message_id=status.message_id)
#         await context.bot.send_message(chat_id=chat_id, text=reply)

#     except Exception as e:
#         logger.error(f"Image Error: {e}")
#         await context.bot.edit_message_text(chat_id=chat_id, message_id=status.message_id, text="❌ Failed to process the image.")

# # --- Execution Entry Point ---
# if __name__ == '__main__':
#     # Build the bot application
#     application = ApplicationBuilder().token(BOT_TOKEN).build()

#     # Register Handlers
#     application.add_handler(CommandHandler('start', start))
#     application.add_handler(MessageHandler(filters.Regex(r'(?i)^(hi|hello|hey)$'), start))
#     application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text_message))
#     application.add_handler(MessageHandler(filters.PHOTO, handle_photo_message))

#     print("🛡️ Guardian AI Pro (v2026) is Online and Syncing to Cloud...")
#     application.run_polling()



import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from ai_engine_gemini import analyze_with_gemini
from ai_engine_cnn import CNNBullyingDetector
from logger_service import log_incident

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
IMAGE_FOLDER = "logged_images"
if not os.path.exists(IMAGE_FOLDER): os.makedirs(IMAGE_FOLDER)

logging.basicConfig(level=logging.INFO)
cnn_detector = CNNBullyingDetector()

def format_report(analysis):
    """Creates a visually engaging, clean report for the user."""
    is_bullying = analysis.get('is_bullying', False)
    score = analysis.get('harm_score', 0)
    
    status = "🚨 CYBERBULLYING DETECTED" if is_bullying else "✅ CONTENT IS SAFE"
    
    msg = f"🛡️ **GUARDIAN AI: OFFICIAL REPORT**\n"
    msg += f"━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"📌 **Status:** {status}\n"
    msg += f"📊 **Harm Score:** {score}%\n"
    msg += f"🌡️ **Severity:** {analysis.get('severity', 'None')}\n"
    msg += f"🏷️ **Category:** {analysis.get('category', 'N/A')}\n\n"
    
    msg += f"🔍 **ANALYSIS DETAILS:**\n"
    msg += f"{analysis.get('reasoning', '• No further details provided.')}\n\n"

    # Indian Government Reporting Bridge (Score > 60%)
    if is_bullying and score >= 60:
        msg += f"⚖️ **OFFICIAL ACTION RECOMMENDED**\n"
        msg += f"Because this score exceeds 60%, we recommend reporting to:\n\n"
        msg += f"🌐 **National Portal:** [cybercrime.gov.in](https://cybercrime.gov.in)\n"
        msg += f"📞 **Helpline:** 1930\n"
        msg += f"🚨 **Note:** Use the saved image in your local folder as evidence."
    return msg

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    status_msg = await context.bot.send_message(chat_id=chat_id, text="🔍 Guardian AI is analyzing context...")

    file_path = None
    input_type = "Text"

    if update.message.photo:
        input_type = "Image"
        photo = await update.message.photo[-1].get_file()
        file_path = os.path.join(IMAGE_FOLDER, f"{photo.file_id}.jpg")
        await photo.download_to_drive(file_path)
        analysis = await analyze_with_gemini(image_path=file_path)
    else:
        analysis = await analyze_with_gemini(text_input=update.message.text)

    if analysis:
        log_incident(
            update.effective_user.id, input_type,
            "Bullying" if analysis['is_bullying'] else "Safe",
            analysis['severity'], analysis['harm_score'],
            analysis['category'], analysis['reasoning'], file_path
        )

    # We remove 'MarkdownV2' mode to avoid "Can't parse entities" formatting crashes
    await context.bot.delete_message(chat_id=chat_id, message_id=status_msg.message_id)
    await context.bot.send_message(chat_id=chat_id, text=format_report(analysis))

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO | (filters.TEXT & ~filters.COMMAND), handle_message))
    print("🛡️ Guardian AI (Dual-Log System) is Live...")
    app.run_polling()