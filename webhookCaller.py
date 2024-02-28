import requests
import loggerManager


logger = loggerManager.get_module_logger("webhookCaller.py")


def sendWebhook(url, payload):    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        logger.info("Webhook called successfully!")
    else:
        logger.error(f"Failed to call webhook. Status code: {response.status_code}")