import uvicorn
from fastapi import FastAPI
from notetiktok.server.merge import resource_service

app = FastAPI()
app.include_router(resource_service)

# uvicorn notecoin_server:app --host '0.0.0.0' --port 8444 --reload
# uvicorn notecoin_server:app --host '0.0.0.0' --port 8444
# uvicorn notecoin_server: app - -host '0.0.0.0' - -port 8444

uvicorn.run(app, host='0.0.0.0', port=8446)
