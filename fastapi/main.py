import uvicorn


if __name__ == "__main__":    
    print("Check http://127.0.0.1:8000/redoc OR \n http://127.0.0.1:8000/docs to play around!")
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)