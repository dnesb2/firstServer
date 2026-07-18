from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/execute")
async def execute_script(request: Request):
    data = await request.json()
    
    # Put your script's execution logic here
    result = {"message": "Success", "received": data}
    
    return result

# Change @app.post to @app.get
@app.get("/execute2")
async def execute_script():
    # Note: GET requests usually do not have a JSON body
    result = {"message": "Success! The GET request worked. this is Davon"}
    return result
