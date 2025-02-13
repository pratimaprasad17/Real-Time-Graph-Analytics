# Base image: ubuntu:22.04
FROM ubuntu:22.04

# ARGs
# https://docs.docker.com/engine/reference/builder/#understand-how-arg-and-from-interact
ARG TARGETPLATFORM=linux/amd64,linux/arm64
ARG DEBIAN_FRONTEND=noninteractive

# Install OpenJDK 17
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Neo4j installation and cleanup
RUN apt-get update && \
    apt-get install -y wget gnupg software-properties-common && \
    
    wget -O - https://debian.neo4j.com/neotechnology.gpg.key | apt-key add - && \
    echo 'deb https://debian.neo4j.com stable latest' > /etc/apt/sources.list.d/neo4j.list && \
    apt-get update && \
    apt-get install -y neo4j=1:5.5.0 python3-pip git && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install necessary Python libraries
RUN python3 -m pip install --upgrade pip && \
    pip install neo4j pandas pyarrow

# Set the Neo4j password to "project1phase1" and configure the server for remote access
RUN sed -i 's/#server.default_listen_address/server.default_listen_address/' /etc/neo4j/neo4j.conf && \
    echo "dbms.security.procedures.unrestricted=gds.*" >> /etc/neo4j/neo4j.conf && \
    echo "dbms.security.procedures.allowlist=gds.*" >> /etc/neo4j/neo4j.conf
    
RUN neo4j-admin dbms set-initial-password project1phase1

RUN wget -P /var/lib/neo4j/plugins https://graphdatascience.ninja/neo4j-graph-data-science-2.3.1.jar

# Download the dataset to the container
RUN wget -P / https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-03.parquet

# Clone the repository using the personal access token
# Change the below line to clone your repo
RUN git clone <Repo Containing data_loader.py>
RUN cp /cse511/data_loader.py /data_loader.py

#COPY data_loader.py /data_loader.py
# Run the data loader script after making it executable

RUN chmod +x /data_loader.py && \
    neo4j start && \
    python3 /data_loader.py && \
    neo4j stop

# Expose Neo4j ports
EXPOSE 7474 7687

# Start Neo4j service and show logs on container run
CMD ["/bin/bash", "-c", "neo4j start && tail -f /dev/null"]


