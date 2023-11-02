import asyncio
from app import Server
from core.unconfirmed_transations import start_job
import threading


def start_uvicorn():
    server = Server()
    server.serve()


if __name__ == '__main__':

    # Create a thread to run the FastAPI server
    fastapi_thread = threading.Thread(target=start_uvicorn)

    # Start the FastAPI server thread
    fastapi_thread.start()

    asyncio.run(start_job())




