from fastapi import FastAPI, Request, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from chatgpt import MyOpenAI
# Uncomment to deploy
# from starlette.middleware.wsgi import WSGIMiddleware

app = FastAPI()

#  Notes - End of Step 3 (Setup)
#  Preparing the application to be used with Angular and
#  deployed to a server.

#  What are the allowed origins for the users.  Localhost:4200 is
#  the Angular desktop development environment

origins = [
    "http://localhost:4200",
    "https://kineticseas.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers in the request
)

# router = APIRouter()
# Uncomment to deploy.  This assumes the all class to the /fastapi folder will come
# here.
# app.include_router(router, prefix="/fastapi")


@app.post("/chat/")
async def chat(request: Request):
    # Configure the OpenAI library with your API key
    # Create a file on your filesystem with the openai key.
    post_data = await request.json()
    return MyOpenAI.chat(post_data['content'])


@app.post("/clear/")
async def chat_chat():
    return MyOpenAI.clear_chat()
