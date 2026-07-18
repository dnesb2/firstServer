from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/execute")
async def execute_script(request: Request):
    data = await request.json()
    
    # Put your script's execution logic here
    result = {"message": "Success", "received": data}
    
    return result
