from prisma import Prisma


class PrismaSingleton:
    def __init__(self):
        """
        Initialize the PrismaSingleton class
        """
        self.client = None

    async def connect(self):
        """
        Connect to the Prisma client
        """
        if self.client is None:
            self.client = Prisma()
            await self.client.connect()

    async def disconnect(self):
        """
        Disconnect from the Prisma client
        """
        if self.client is not None:
            await self.client.disconnect()
            self.client = None
