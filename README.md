# Instructions to run 

1. Install the requirements
```
pip install -r requirements.txt
```
2. Run using uvicorn
```
uvicorn earth_pulse_API:app --reload
```

The endpoints have to be used with the image_path so that the user can run the app for any image of choice instead of having it hardcoded 
Example: 
```
http://127.0.0.1:8000/attributes/S2L2A_2022-06-09.tiff
```
