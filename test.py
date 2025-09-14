import asyncio
import test_files

async def main():

    await test_files.main()

    return


if __name__ == "__main__":
    asyncio.run(main())