import socketio
from fastapi import FastAPI
import uvicorn

# Socket.IO async server
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*"
)

# FastAPI app
fastapi_app = FastAPI()

@fastapi_app.get("/")
async def home():
    return {"message": "Server running ✅"}

# Combine both
app = socketio.ASGIApp(sio, fastapi_app)

# ---------------- SOCKET EVENTS ---------------- #

@sio.event
async def connect(sid, environ):
    print("User connected:", sid)

@sio.event
async def message(sid, data):
    print("User:", data)

    # 🔥 simple AI chatbot logic
    text = data.lower()

    if "hi" in text or "hello" in text:
        reply = "Hello! How can I help you?"
    elif "price" in text:
        reply = "Please tell me which product price?"
    elif "name" in text:
        reply = "I am your AI assistant 🤖"
    elif "bye" in text:
        reply = "Goodbye 👋"
    else:
        reply = "I didn't understand, please ask clearly."

    await sio.emit("response", {"msg": reply}, to=sid)

@sio.event
async def disconnect(sid):
    print("User disconnected:", sid)

# ---------------- RUN SERVER ---------------- #

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)