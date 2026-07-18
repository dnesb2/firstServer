from fastapi import FastAPI, Request, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
import shutil
import os
from google import genai

app = FastAPI()

@app.post("/execute")
async def execute_script(request: Request):
    data = await request.json()
    
    # Put your script's execution logic here
    result = {"message": "Success", "received": data}
    
    return result


# using POST for uploading data (pic) which of course you place to send to AI
@app.post("/executeR")
async def execute_script(file: UploadFile = File(...)):
    client = genai.Client(api_key="AQ.Ab8RN6JH5ottS1H_QVSQZNV5_wU0ezTAK6Uo_R5MEfZbJ2cY-Q")
    # 1. Name where you want to save the incoming image on Railway
    server_filename = f"received_{file.filename}"
    
    # 2. Save the incoming file stream to the server's disk
    with open(server_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # 3. Your processing logic goes here
    # (e.g., edit the image, analyze it, etc.)
    uploaded_File = client.files.upload(file=file.filename)

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

