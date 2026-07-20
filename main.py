from fastapi import FastAPI, Request, HTTPException, UploadFile, Form, File
from fastapi.responses import FileResponse
import shutil
import os
from typing import Annotated
from google import genai
import json


# # Fetch the key from Railway's environment variables
#api_key_string = os.getenv("GEMINI_API_KEY")

#if not api_key_string:
#    raise ValueError("GEMINI_API_KEY environment variable is missing on Railway!")

# # Explicitly pass the key to the client
#client = genai.Client(api_key=api_key_string)
finalStr = ""
with open("private.txt", "r") as f:
    for l in f.read():
        if l == '+':
            finalStr = finalStr + '.' 
            continue
        else:
            finalStr = finalStr + l
print("key -> ", finalStr)
client = genai.Client(api_key=finalStr)
app = FastAPI()

@app.post("/execute")
async def execute_script(request: Request):
    data = await request.json()  
    
    # Put your script's execution logic here
    result = {"message": "Success, server is running", "received": data}
    
    return result

@app.post("/executeW")
async def execute_script(payload: Annotated[str, Form(...)], file: Annotated[UploadFile, File(...)]):
    global client

   
    # 1. Name where you want to save the incoming image on Railway
    server_filename = f"received_{file.filename}"
    
    # 2. Save the incoming file stream to the server's disk
    with open(server_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # 3. Your processing logic goes here
    # (e.g., edit the image, analyze it, etc.)
    data_dict = json.loads(payload)
    uploaded_File = client.files.upload(file=server_filename)
    #data = await request.json() 

   # print(data)
    # Convert your payload string back to a dictionary if needed
    
    
    # Put your script's execution logic here
    #result = {"message": "Success", "payload_received": data_dict}

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=[
            data_dict['Quest'],
            uploaded_File
        ]
    )
    
    return {
        "message": "Image received successfully!",
        "filename": file.filename,
        "content_type": file.content_type,
        "furtherInfo" : response.text
    }
    
    return result

@app.post("/executeQ")
async def execute_script(payload: Annotated[str, Form(...)]):
    global client

        
    # 3. Your processing logic goes her
    # (e.g., edit the image, analyze it, etc.)
    data_dict = json.loads(payload)
    #data = await request.json() 

   # print(data)
    # Convert your payload string back to a dictionary if needed
    
    
    # Put your script's execution logic here
    #result = {"message": "Success", "payload_received": data_dict}

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=[
            data_dict['Quest']
        ]
    )
    
    return {
        "message": "success",
        "furtherInfo" : response.text
    }
    
    return result


# using POST for uploading data (pic) which of course you place to send to AI
@app.post("/executeR")
async def execute_script(file: UploadFile = File(...)):
    global client
    # 1. Name where you want to save the incoming image on Railway
    server_filename = f"received_{file.filename}"
    
    # 2. Save the incoming file stream to the server's disk
    with open(server_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # 3. Your processing logic goes here
    # (e.g., edit the image, analyze it, etc.)
    uploaded_File = client.files.upload(file=server_filename)

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=[
            "Explain this pic",
            uploaded_File
        ]
    )
    
    return {
        "message": "Image received successfully!",
        "filename": file.filename,
        "content_type": file.content_type,
        "furtherInfo" : response.text
    }

@app.post("/executeA")
async def execute_script(file: UploadFile = File(...)):
    global client
    # 1. Name where you want to save the incoming image on Railway
    server_filename = f"received_{file.filename}"
    
    # 2. Save the incoming file stream to the server's disk
    with open(server_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # 3. Your processing logic goes here
    # (e.g., edit the image, analyze it, etc.)
    uploaded_File = client.files.upload(file=server_filename)

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=[
            "Answer based on audio",
            uploaded_File
        ]
    )
    
    return {
        "message": "Image received successfully!",
        "filename": file.filename,
        "content_type": file.content_type,
        "furtherInfo" : response.text
    }

# Change @app.post to @app.get
@app.get("/execute2")
async def execute_script():
    # Note: GET requests usually do not have a JSON body
    result = {"message": "Success! The GET request worked. this is Davon"}
    return result


#this sends back a video file
@app.get("/get_vid")
async def execute_script():
    # 1. Path to the video file on your Railway server
    video_path = "output.mp4" 
    
    # 2. Check if the video actually exists to prevent crashes
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video file not found")
        
    # 3. Return the file with the correct video media type
    return FileResponse(
        path=video_path, 
        media_type="video/mp4", 
        filename="downloaded_video.mp4"
    )

