# Data Processing Pipeline for Real Time Graph Analytics
A scalable real-time graph analytics pipeline using Kubernetes, Kafka, and Neo4j for efficient data ingestion and processing.

## Introduction
This project explores **graph-based data analytics** using **Neo4j, Docker, Kubernetes, and Kafka**, leveraging the **NYC Yellow Cab Trip dataset**. The objective is to build a **scalable, distributed data processing pipeline** for graph analytics, demonstrating the potential of graph databases in transportation and urban planning.

The project consists of two main phases:

- **Phase 1:** Implement graph processing algorithms (**PageRank & BFS**) in a **Dockerized Neo4j environment**.
- **Phase 2:** Scale the system using **Kubernetes & Kafka**, enabling real-time data ingestion and distributed analytics.

## Repository Structure
```
|-- src/
    |-- main/
        |-- python/
            |-- interface.py
            |-- data_loader.py
            |-- tester.py
|-- config/
    |-- neo4j-service.yaml
    |-- neo4j-values.yaml
    |-- zookeeper-setup.yaml
    |-- kafka-setup.yaml
    |-- kafka-neo4j-connector.yaml
|-- docker/
    |-- Dockerfile
|-- CSE511-Project1-Report.pdf
|-- README.md
```

## Technologies Used
- **Neo4j 5.5.0**: Graph database for storing and processing trip data.
- **Graph Data Science (GDS) Plugin**: Enables advanced analytics such as **PageRank and BFS**.
- **Docker**: Encapsulates the environment for reproducibility.
- **Kubernetes (Minikube)**: Manages containerized deployments.
- **Kafka**: Handles real-time data streaming.
- **Python 3.x**: Used for interfacing with Neo4j and data processing.
- **Zookeeper**: Coordinates Kafka brokers.

## Phase 1: Standalone Graph Processing with Neo4j
### Environment Setup
A **Docker container** was created to run Neo4j with the required configurations. The **Dockerfile** installs:
- Neo4j and the Graph Data Science Plugin.
- Required Python libraries (`neo4j`, `pandas`, `pyarrow`).
- Data ingestion and processing scripts.

### Data Ingestion & Schema
The **NYC Yellow Cab Trip dataset** was modeled as a **graph**:
- **Nodes:** Represent pickup/drop-off locations.
- **Edges:** Represent taxi trips, containing **distance, fare, and timestamps** as properties.

### Graph Algorithms Implemented
#### 1. **PageRank**
- Identifies key locations (hubs) based on trip connectivity.
- Uses a damping factor of **0.85** for ranking calculations.

#### 2. **Breadth-First Search (BFS)**
- Explores optimal routes between locations.
- Useful for analyzing traffic patterns and bottlenecks.

## Phase 2: Distributed Graph Processing with Kubernetes & Kafka
To scale the processing pipeline, the system was **migrated to Kubernetes** and **Kafka was introduced for real-time data ingestion**.

### Key Enhancements
1. **Zookeeper & Kafka Deployment:**
   - Zookeeper coordinates Kafka brokers.
   - Kafka enables real-time streaming of taxi trip data.

2. **Neo4j Deployment in Kubernetes:**
   - Managed using **Helm charts**.
   - Persistent storage configured to maintain database state.

3. **Kafka-Neo4j Integration:**
   - Kafka topics store trip data as events.
   - Kafka Connect transforms and streams data into **Neo4j as graph relationships**.

## Running the Project
### 1. Setting up the Docker Environment
```sh
docker build -t neo4j-graph-analytics .
docker run -p 7474:7474 -p 7687:7687 -d neo4j-graph-analytics
```
Access Neo4j at: [http://localhost:7474](http://localhost:7474)

### 2. Running the Data Loader
```sh
python data_loader.py
```


### 3. Deploying with Kubernetes
Start Minikube:
```sh
minikube start
```
Apply Kubernetes configurations:
```sh
kubectl apply -f zookeeper-setup.yaml
kubectl apply -f kafka-setup.yaml
kubectl apply -f neo4j-service.yaml
kubectl apply -f kafka-neo4j-connector.yaml
```
Expose Neo4j service:
```sh
kubectl port-forward service/neo4j-service 7474:7474
```

## Debugging & Testing
Run the test suite:
```sh
python tester.py
```
**Tests Include:**
- **Data Integrity Check:** Verifies nodes and relationships.
- **PageRank Validation:** Confirms ranking accuracy.
- **BFS Pathfinding:** Ensures correct traversal.

## Contribution
Feel free to fork this repository and contribute improvements! Open issues or pull requests if you encounter problems.

## License
MIT License

---
If you have any issues running the project, please raise an issue on the repository.
