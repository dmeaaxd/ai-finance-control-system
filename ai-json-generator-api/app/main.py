import uvicorn

if __name__ == "__main__":
    uvicorn.run("routes:app", host="0.0.0.0", reload=True, port=8451)
