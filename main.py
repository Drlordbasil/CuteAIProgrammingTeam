import logging
from conversation_manager import ConversationManager

# Configure logging at the start of your application
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        logging.info("Application starting...")
        manager = ConversationManager()
        manager.conversation_thread()  # This method initiates the conversation and development process.
        logging.info("Application finished successfully.")
    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
    finally:
        logging.info("Application shutdown.")

if __name__ == "__main__":
    main()
