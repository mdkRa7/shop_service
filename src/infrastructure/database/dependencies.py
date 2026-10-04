from .session import session


async def get_session():
    async with session() as se:
        try:
            yield se
            await se.commit()
        except Exception:
            await se.rollback()
            raise

