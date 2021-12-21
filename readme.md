# Development 

## Dependencies

Use `pip install -r requirements.txt` to install required packages

If more dependencies are added, run `pip freeze > requirements.txt` to regenerate the requirements.txt required for Azure.

## Running the application

Use `uvicorn main:app --reload` to run the application. 

While running, open http://localhost:8000/docs or http://localhost:8000/redoc to view the API documentation

# Production

All changes pushed to main are automatically published to an Azure web app found at https://stasa-farmers-market.azurewebsites.net/