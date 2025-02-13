from neo4j import GraphDatabase

class Interface:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)
        self._driver.verify_connectivity()

    def close(self):
        self._driver.close()

    def bfs(self, start, end):
        with self._driver.session() as session:
            session.run("""
              CALL gds.graph.exists('dataset_graph') YIELD exists
                WITH exists
                WHERE exists
                CALL gds.graph.drop('dataset_graph') YIELD graphName
                RETURN graphName
            """)

            session.run("""
               CALL gds.graph.project(
                'dataset_graph',
                ['Location'],
                {
                    TRIP: {
                    type: 'TRIP',
                    orientation: 'UNDIRECTED'
                    }
                }
                )
            """)

            result = session.run("""
                MATCH (source:Location {name: $startnode}), (target:Location {name: $lastnode})
                CALL gds.bfs.stream('dataset_graph', {
                sourceNode: source,
                targetNodes: [target]
                })
                YIELD path 
                RETURN path
            """, startnode=start, lastnode=end
    )

            return result.data()

            
    def pagerank(self, max_itr, weight):
        with self._driver.session() as session:
            session.run("""
              CALL gds.graph.exists('nycTripData') YIELD exists
                WITH exists
                WHERE exists
                CALL gds.graph.drop('nycTripData') YIELD graphName
                RETURN graphName
            """)

            session.run("""
                        CALL gds.graph.project(
                        'nycTripData',
                        'Location', 
                        {
                            TRIP: {  
                            properties: $weight
                     
                            }
                        }
                        )
                        YIELD graphName, nodeCount, relationshipCount;
                        """, max_itr
                =max_itr
                , weight
        =weight
        )
            
            result = session.run("""

                CALL gds.pageRank.stream('nycTripData', {
                maxIterations: $max_itr
        ,
                dampingFactor: 0.85,
                relationshipWeightProperty: $weight
        
                })
                YIELD nodeId, score
                WITH gds.util.asNode(nodeId) AS location, score
                ORDER BY score DESC
                LIMIT 1
                RETURN 'Max PageRank' AS Type, location.name AS Location, score

                UNION ALL

                CALL gds.pageRank.stream('nycTripData', {
                maxIterations: $max_itr
        ,
                dampingFactor: 0.85,
                relationshipWeightProperty: $weight
        
                })
                YIELD nodeId, score
                WITH gds.util.asNode(nodeId) AS location, score
                ORDER BY score ASC
                LIMIT 1
                RETURN 'Min PageRank' AS Type, location.name AS Location, score;
                """, max_itr
        =max_itr
        , weight
=weight
)
            
            json_result = []
            for record in result:
                json_result.append({
                    "name": record["Location"],
                    "score": record["score"]
                })
    
            
        return json_result