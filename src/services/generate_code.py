import random


class GenerateCodeService:
    """Service to generate code."""

    async def generate_code(self) -> str:
        """Generate code from 1000 to 9999."""
        return str(random.randint(1000, 9999))

    async def get_message_with_generated_code(self, code) -> str:
        """Return message with generated code"""
        return f'Your verification code is: {code}'


generate_code_service = GenerateCodeService()
