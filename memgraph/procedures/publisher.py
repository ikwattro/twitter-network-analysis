from kafka import KafkaProducer
import json
import mgp
import os

KAFKA_IP = os.getenv("KAFKA_IP", "kafka")
KAFKA_PORT = os.getenv("KAFKA_PORT", "9092")


@mgp.read_proc
def create(created_objects: mgp.Any) -> mgp.Record():
    created_objects_info = {"vertices": [], "edges": []}

    for obj in created_objects:
        if obj["event_type"] == "created_vertex":
            created_object = {
                "id": obj["vertex"].id,
                "labels": [label.name for label in obj["vertex"].labels],
                "username": obj["vertex"].properties["username"],
                "rank": obj["vertex"].properties["rank"],
                "cluster": obj["vertex"].properties["cluster"],
            }
            created_objects_info["vertices"].append(created_object)
        else:
            created_objects_info["edges"].append(
                {
                    "id": obj["edge"].id,
                    "type": obj["edge"].type.name,
                    "source": obj["edge"].from_vertex.id,
                    "target": obj["edge"].to_vertex.id,
                }
            )

    kafka_producer = KafkaProducer(bootstrap_servers=KAFKA_IP + ":" + KAFKA_PORT)
    kafka_producer.send(
        "created_objects", json.dumps(created_objects_info).encode("utf8")
    )

    return mgp.Record()


@mgp.read_proc
def update_rank(node: mgp.Vertex, rank: float) -> mgp.Record():
    updated_objects_info = {"vertices": [], "edges": []}

    updated_object = {
        "id": node.id,
        "labels": [label.name for label in node.labels],
        "username": node.properties["username"],
        "rank": rank,
    }
    updated_objects_info["vertices"].append(updated_object)

    kafka_producer = KafkaProducer(bootstrap_servers=KAFKA_IP + ":" + KAFKA_PORT)
    kafka_producer.send(
        "created_objects", json.dumps(updated_objects_info).encode("utf8")
    )

    return mgp.Record()


@mgp.read_proc
def update_cluster(node: mgp.Vertex, community_id: int) -> mgp.Record():
    updated_objects_info = {"vertices": [], "edges": []}

    updated_object = {
        "id": node.id,
        "labels": [label.name for label in node.labels],
        "username": node.properties["username"],
        "cluster": community_id,
    }
    updated_objects_info["vertices"].append(updated_object)

    kafka_producer = KafkaProducer(bootstrap_servers=KAFKA_IP + ":" + KAFKA_PORT)
    kafka_producer.send(
        "created_objects", json.dumps(updated_objects_info).encode("utf8")
    )

    return mgp.Record()
