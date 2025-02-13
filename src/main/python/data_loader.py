import pyarrow.parquet as pq
import pandas as pd
from neo4j import GraphDatabase
import time


class DataLoader:

    def __init__(self, uri, user, password):
        """
        Connect to the Neo4j database and other init steps
        
        Args:
            uri (str): URI of the Neo4j database
            user (str): Username of the Neo4j database
            password (str): Password of the Neo4j database
        """
        # Remove `encrypted=True` for a local setup
        self.driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)
        self.driver.verify_connectivity()

    def close(self):
        """
        Close the connection to the Neo4j database
        """
        self.driver.close()

    def load_transform_file(self, file_path):
        """
        Load the parquet file and transform it into nodes and relationships in Neo4j.

        Args:
            file_path (str): Path to the parquet file to be loaded
        """
        # Read the parquet file
        trips = pq.read_table(file_path).to_pandas()

        # Filter relevant columns and perform data cleaning
        trips = trips[['tpep_pickup_datetime', 'tpep_dropoff_datetime', 'PULocationID', 'DOLocationID', 'trip_distance', 'fare_amount']]

        # Define Bronx location IDs
        bronx = [3, 18, 20, 31, 32, 46, 47, 51, 58, 59, 60, 69, 78, 81, 94, 119, 126, 136, 147, 159, 167, 168, 169, 174, 182, 183, 184, 185, 199, 200, 208, 212, 213, 220, 235, 240, 241, 242, 247, 248, 250, 254, 259]
        
        # Filter rows for trips within the Bronx
        trips = trips[trips['PULocationID'].isin(bronx) & trips['DOLocationID'].isin(bronx)]
        trips = trips[trips['trip_distance'] > 0.1]
        trips = trips[trips['fare_amount'] > 2.5]

        # Convert datetime columns to string format compatible with Neo4j datetime
        trips['tpep_pickup_datetime'] = trips['tpep_pickup_datetime'].dt.strftime('%Y-%m-%dT%H:%M:%S')
        trips['tpep_dropoff_datetime'] = trips['tpep_dropoff_datetime'].dt.strftime('%Y-%m-%dT%H:%M:%S')

        # Connect to Neo4j and load the data
        with self.driver.session() as session:
            # Create unique location nodes
            locations = set(trips['PULocationID']).union(set(trips['DOLocationID']))
            for loc in locations:
                session.run(
                    """
                    MERGE (l:Location {name: $locationID})
                    """,
                    locationID=int(loc)
                )

            # Create trip relationships
            for _, row in trips.iterrows():
                session.run(
                    """
                    MATCH (start:Location {name: $PULocationID})
                    MATCH (end:Location {name: $DOLocationID})
                    MERGE (start)-[:TRIP {
                        distance: $distance,
                        fare: $fare,
                        pickup_dt: datetime($pickup_dt),
                        dropoff_dt: datetime($dropoff_dt)
                    }]->(end)
                    """,
                    PULocationID=int(row['PULocationID']),
                    DOLocationID=int(row['DOLocationID']),
                    distance=float(row['trip_distance']),
                    fare=float(row['fare_amount']),
                    pickup_dt=row['tpep_pickup_datetime'],
                    dropoff_dt=row['tpep_dropoff_datetime']
                )


def main():
    total_attempts = 10
    attempt = 0

    # Try to connect to the database multiple times in case it is still initializing
    while attempt < total_attempts:
        try:
            # Use the provided URI and credentials for local Neo4j
            data_loader = DataLoader("bolt://localhost:7687", "neo4j", "project1phase1")
            data_loader.load_transform_file("yellow_tripdata_2022-03.parquet")
            data_loader.close()
            
            print("Data loaded successfully!")
            break  # Exit the loop if the data loads successfully

        except Exception as e:
            print(f"(Attempt {attempt+1}/{total_attempts}) Error: ", e)
            attempt += 1
            time.sleep(10)


if __name__ == "__main__":
    main()
