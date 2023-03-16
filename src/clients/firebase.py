"""Firebase client for push notifications."""
import logging
import os

import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate(os.environ.get("FIREBASE_PATH"))
firebase_admin.initialize_app(cred)


logger = logging.getLogger(__name__)


class FirebaseClient:
    """Firebase Client for sending push notifications to Android and iOS devices based on events."""

    def __init__(
            self,
            fcm_token: str,
            title: str,
            body: str,
    ):
        self.fcm_token = fcm_token
        self.title = title
        self.body = body

    def send_ios_push_notification(self):
        """Send notification to ios device."""
        message = messaging.Message(
            data={
                'title': self.title,
                'body': self.body,
                'sound': 'default'
            },
            token=self.fcm_token,
            apns=messaging.APNSConfig(
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(sound='default')
                )
            )
        )

        try:
            messaging.send(message)
        except Exception as e:
            logger.exception(f"Push Notification failed to send. Error: {str(e)}")

    def send_android_push_notification(self):
        """Send notification to android device."""
        message = messaging.Message(
            data={
                'title': self.title,
                'body': self.body
            },
            token=self.fcm_token,
            android=messaging.AndroidConfig(
                priority='high',
                notification=messaging.AndroidNotification(
                    title=self.title,
                    body=self.body,
                    sound='default'
                )
            )
        )

        try:
            messaging.send(message)
        except Exception as e:
            logger.exception(f"Push Notification failed to send. Error: {str(e)}")
