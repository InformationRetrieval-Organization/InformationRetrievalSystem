from db.prisma_singleton import PrismaSingleton
from prisma import Prisma

class ServiceProvider:
  def __init__(self):
    self._prisma = None

  async def get_prisma(self) -> Prisma:
    if self._prisma is None:
      self._prisma = PrismaSingleton()
      await self._prisma.connect()  # Connect on first access
    return self._prisma.client
