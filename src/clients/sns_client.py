import os

import aioboto3


class SNSClient:
    """Wrapper class for sns implementations."""

    def __init__(
            self,
            service_name,
            region_name,
            aws_access_key_id,
            aws_secret_access_key,
    ):
        self.session = aioboto3.Session()
        self.service_name = service_name
        self.region_name = region_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

    async def send_message(self, phone: str, message: str):
        async with self.session.client(
            service_name=self.service_name,
            region_name=self.region_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        ) as sns:
            await sns.publish(
                PhoneNumber=phone,
                Message=message,
                Subject='CatchApp',
            )


sns_client = SNSClient(
    service_name='sns',
    region_name='us-east-2',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
)
