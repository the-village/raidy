import raidy
import asyncio
token = "token"
group_id = id

async def main():

    raid = raidy.FullRaid(token=token, group_id=group_id, message_raid="TEST", symbols=5)
    await raid.run()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(main()))
