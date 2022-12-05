from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
import os
import atexit
import sdk
import uvicorn
from utils.db import uri, user, password
from pathlib import Path

driver = sdk.Metadata(uri, user, password)

def exit_application():
    driver.close()
atexit.register(exit_application)

app = FastAPI()

@app.get("/metadata_portal/")
async def home():
    html_string = Path('dataPortalDocumentation.html').read_text()
    return(HTMLResponse(html_string))

@app.get("/get_datasets")
async def datasets():
    result = driver.get_datasets()
    return(result)

@app.get("/get_species")
async def species():
    result = driver.get_species()
    return(result)

@app.get("/get_metadata")
async def metadata(dataset_name: str):
    metadata = driver.get_dataset_metadata(dataset_name)
    distribution = driver.get_dataset_distribution(dataset_name)
    publisher = driver.get_dataset_publisher(dataset_name)
    license = driver.get_dataset_license(dataset_name)
    provider = driver.get_dataset_provider(dataset_name)
    contactPoint = driver.get_dataset_contact_point(dataset_name)
    IDs = ['dataset','distribution','publisher','license','provider','contactPoint']
    result = dict(zip(IDs, (metadata, distribution, publisher, license, provider, contactPoint)))
    return(result)

@app.get("/search_species")
async def search_species(species: str):
    metadata = driver.get_species_datasets(species)
    return(metadata)

@app.get("/search_country")
async def search_country(country: str): 
    metadata = driver.get_country_datasets(country)
    return(metadata)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
