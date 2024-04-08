from prisma import Prisma

class PrismaSingleton:
  def __init__(self):
    self.client = None

  async def connect(self):
    if self.client is None:
      self.client = Prisma()
      await self.client.connect()

  async def disconnect(self):
    if self.client is not None:
      await self.client.disconnect()
      self.client = None
