# Metadata API 
The GBADs Metadata API allows users to query the GBADs data catalogue. This repository contains information about how to access the metadata graph using the API. 

## The Stack 
These are the components of the API: 
- Web Framework:
    - async: FastAPI (Micro-Webframework)
- Neo4j Database Connector: Neo4j Python Driver
- Database: Neo4j Aura

## Set-Up

To install and run this application you need to install FastAPI and other Python modules: 
- pip install fastapi
- pip install uvicorn
- pip install neo4j
- pip install json 
- pip install pathlib

Then you can run the API on port 8000: 

python3 main.py

This will need to be run in the background to stay running and let you use the shell. 

To access the API in your web browser start with the command: 
http://localhost:9000/metadata_portal/

This will provide you with some information about commands that can be run and a Quick API guide to gtt started

### Future Directions
This API is not complete. Improvements that still need to be made include: 
- Add error handling 
- Add ability to MATCH regardless of case and/if the query contains string
- Add in ability to extract standards used from metadata 
- Add in distribution of each datasource in the GBADs KE 
- Add commenting in the code 

## Notes:
To access Neo4j Aura you will need a file called db.py to use the SDK and run the API locally. This file contains password information - if you would like to use it please contact Kassy Raymond.