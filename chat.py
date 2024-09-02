import sys
import time
import threading
from google.cloud import pubsub_v1

project_id = "xxx-12345"
topic_id = "user1-user2"
subscription_id = None

if len(sys.argv) != 2 or sys.argv[1] not in ["1", "2"]:
    print("Usage: python chat.py <username>")
    print("<username> should be either '1' or '2'")
    sys.exit(1)

username = sys.argv[1]
subscription_id = f"user{3-int(username)}-subscription"  # Ensures user1 subscribes to user2-subscription and vice-versa

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()
topic_path = publisher.topic_path(project_id, topic_id)
subscription_path = subscriber.subscription_path(project_id, subscription_id)

# Function to listen for messages
def listen_for_messages():
    def callback(message):
        data = message.data.decode("utf-8")
        message_user, msg = data.split(": ", 1)
        if message_user != f"user{username}":
            print(f"Received from {message_user}: {msg}")
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...")

    with subscriber:
        try:
            streaming_pull_future.result()
        except KeyboardInterrupt:
            streaming_pull_future.cancel()

# Ensure the topic and subscription exist
try:
    publisher.create_topic(request={"name": topic_path})
except Exception as e:
    pass  # Ignore if the topic already exists

try:
    subscriber.create_subscription(request={"name": subscription_path, "topic": topic_path})
except Exception as e:
    pass  # Ignore if the subscription already exists

# Start listening to messages in a separate thread
listener_thread = threading.Thread(target=listen_for_messages)
listener_thread.start()

# Loop to send messages
while True:
    message = input(f"You (user {username}): ")
    full_message = f"user{username}: {message}"
    future = publisher.publish(topic_path, full_message.encode("utf-8"))
    future.result()  # Ensure the message is published before proceeding


