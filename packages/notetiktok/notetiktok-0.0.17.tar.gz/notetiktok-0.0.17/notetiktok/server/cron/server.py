import uvicorn
from fastapi import FastAPI

app = FastAPI()
app.include_router(account_account)

# uvicorn notecoin_server:app --host '0.0.0.0' --port 8444 --reload
# uvicorn notecoin_server:app --host '0.0.0.0' --port 8444
# uvicorn notecoin_server: app - -host '0.0.0.0' - -port 8444

uvicorn.run(app, host='0.0.0.0', port=8444)
