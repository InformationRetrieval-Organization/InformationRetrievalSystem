from contextlib import asynccontextmanager
from fastapi import FastAPI
from information_retrieval.vector_space_model import build_vector_space_model
from information_retrieval.boolean_model import build_boolean_model
from preprocessing.preprocessing import preprocess_documents
from api.vector_space_api import router as vector_space_router
from api.boolean_api import router as boolean_router
from db.helper import init_database
from information_retrieval.globals import init
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("FastAPI app started.")

    await init_database()

    init()
    await preprocess_documents()
    await build_boolean_model()
    await build_vector_space_model()

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(vector_space_router)
app.include_router(boolean_router)

# Enable CORS for the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
