import csv
import random
import time
from kafka import KafkaProducer

# Khởi tạo Kafka Producer
producer = KafkaProducer(
    bootstrap_servers="localhost:29092",
)
print(producer)
import json


# Đọc dữ liệu từ file CSV và đẩy lên Kafka
def push_data_to_kafka(file_path, topic_name):
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            # Tạo bản ghi với các trường yêu cầu
            record = {
                "student_code": int(row[0]),
                "activity": row[1],
                "numberOfFile": int(row[2]),
                "timestamp": row[3],
            }
            producer.send(topic_name, value=json.dumps(record).encode("utf-8"))
            print("Sent record:", record)
            time.sleep(1)  # Đợi mỗi giây trước khi gửi dòng tiếp theo


if __name__ == "__main__":
    file_path = "../data/log_action.csv"
    kafka_topic = "vdt2024"
    push_data_to_kafka(file_path, kafka_topic)
