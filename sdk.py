# Functions to perform Neo4j database functions on the metadata graphdb 

# Author: Kassy Raymond

# Date of Last Update: December 2nd, 2022

from neo4j import GraphDatabase
from json import dumps

class Metadata:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user,password))
    
    def close(self):
        self.driver.close()
    
    def get_datasets(self):
        with self.driver.session() as session:
            result = session.read_transaction(self.return_datasets)
            return(result)

    def return_datasets(self, tx):
        dataset = []
        query = (
            'MATCH (n:dataset) '
            'RETURN n.name AS name'
        )
        result = tx.run(query)
        for line in result:
            dataset.append(line['name'])
        dataset_dict = dict({'name': dataset})
        return(dataset_dict)
    
    def get_species(self):
        with self.driver.session() as session:
            result = session.read_transaction(self.return_species)
            return(result)

    def return_species(self, tx):
        species = []
        query = (
            'MATCH (n:Category) '
            'RETURN n.name AS name'
        )
        result = tx.run(query)
        for line in result:
            species.append(line['name'])
        species_dict = dict({'name': species})
        return(species_dict)

    def get_species_datasets(self, category):
        with self.driver.session() as session:
            datasets = session.write_transaction(self.return_species_datasets, category)
        return(datasets)
    
    def return_species_datasets(self, tx, category):
        query = ('MATCH (n:Category)-[]-()-[]-(d:dataset) '  
                'WHERE toLower(n.name) CONTAINS toLower($category) '
                'RETURN DISTINCT(d) AS data'
        )
        result = tx.run(query, category = category)
        dict = {'dataset': [self.serialize_metadata(line) for line in result]}
        return(dict)
    
    def get_dataset_metadata(self, name):
        with self.driver.session() as session:
            metadata = session.write_transaction(self.return_dataset_metadata, name)
        return(metadata)
    
    def return_dataset_metadata(self, tx, name):
        query = ('MATCH (n:dataset {name: $name}) '
                        'RETURN n AS data'
                        )
        result = tx.run(query, name = name)
        for record in result:
            dict = {
                'name': record['data']['name'],
                'datePublished': record['data']['datePublished'],
                'datasetTimeInterval': record['data']['datasetTimeInterval'],
                'citation': record['data']['citation'],
                'description': record['data']['description'],
                'id': record['data']['id'] 
            }
        return(dict)
    
    def get_dataset_distribution(self, name):
        with self.driver.session() as session:
            distribution = session.write_transaction(self.return_dataset_distribution, name)
        return(distribution)
    
    def return_dataset_distribution(self, tx, name):
        query = ('MATCH (n:dataset {name: $name})-[]-(d:distribution) '
                        'RETURN d AS distribution'
        )
        result = tx.run(query, name = name)
        for record in result:
            dict = {
                'name': record['distribution']['name'],
                'identifier': record['distribution']['identifier'],
                'description': record['distribution']['description'],
                'fileFormat': record['distribution']['fileFormat'],
                'contentSize': record['distribution']['contentSize']
            }
        return(dict)
    
    def get_dataset_publisher(self, name):
        with self.driver.session() as session:
            publisher = session.write_transaction(self.return_dataset_publisher, name)
        return(publisher)

    def return_dataset_publisher(self, tx, name):
        query = ('MATCH (n:dataset {name: $name})-[]-(p:publisher) '
                'RETURN p AS publisher'
        )
        result = tx.run(query, name = name)
        for record in result:
            dict = {
                'name': record['publisher']['name']
            }
        return(dict)

    def get_dataset_contact_point(self, name):
        with self.driver.session() as session:
            contactPoint = session.write_transaction(self.return_dataset_contact_point, name)
        return(contactPoint)

    def return_dataset_contact_point(self, tx, name):
        query = ('MATCH (n:dataset {name: $name})-[]-(cp:contactPoint) '
                'RETURN cp AS contactPoint'
        )
        result = tx.run(query, name = name)
        for record in result:
            dict = {
                'name': record['contactPoint']['name']
            }
        return(dict)
    
    def get_dataset_provider(self, name):
        with self.driver.session() as session:
            provider = session.write_transaction(self.return_dataset_provider, name)
        return(provider)
    
    def return_dataset_provider(self, tx, name):
        query = ('MATCH (n:dataset {name: $name})-[]-(p:provider) '
                'RETURN p AS provider'
        )
        result = tx.run(query, name = name)
        for record in result:
            dict = {
                'name': record['provider']['name']
            }
        return(dict)
    
    def get_dataset_license(self, name):
        with self.driver.session() as session:
            license = session.write_transaction(self.return_dataset_license, name)
        return(license)

    def return_dataset_license(self, tx, name):
        query = ('MATCH (n:dataset {name: $name})-[]-(l:license) '
                'RETURN l AS license'
        )
        result = tx.run(query, name = name)
        for record in result: 
            dict = {
                'name': record['license']['name'],
                'url': record['license']['url']
            }
        return(dict)
    
    def get_country_datasets(self, country):
        with self.driver.session() as session:
            metadata = session.write_transaction(self.return_country_dataset, country)
            return(metadata)

    def serialize_metadata(self, record):
        dataset = {
            'name': record['data']['name'],
            'datePublished': record['data']['datePublished'],
            'datasetTimeInterval': record['data']['datasetTimeInterval'],
            'citation': record['data']['citation'],
            'description': record['data']['description'],
            'id': record['data']['id'] 
         }
        return(dataset)
    
    def return_country_dataset(self, tx, country):
        query = ('MATCH (n:Area)-[]-()-[]-()-[]-(d:dataset) '
                'WHERE toLower(n.name) CONTAINS toLower($name) '
                'RETURN d AS data'
        )
        try:
            result = tx.run(query, name = country)
            dict = {'dataset': [self.serialize_metadata(line) for line in result]}
            return(dict)
        except:
            return('Provide a valid country.')


    

    

    
