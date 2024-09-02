# Google Pub/Sub Chat Application

This project demonstrates a simple chat application using Google Cloud Pub/Sub. The chat application allows two users to send messages to each other in real time.

## What `chat.py` Does

The `chat.py` script enables two users to chat with each other by publishing and subscribing to messages using Google Cloud Pub/Sub. The users (`user1` and `user2`) send messages to a common topic and listen for messages on their respective subscriptions.

- **User 1**: Publishes messages to `user1-user2` topic.
- **User 2**: Subscribes to messages on `user2-subscription`.
- **User 2**: Publishes messages to `user1-user2` topic.
- **User 1**: Subscribes to messages on `user1-subscription`.

## Understanding Google Pub/Sub

### Topics
- A **topic** is a named resource to which messages are sent by publishers.
- In this application, the topic `user1-user2` is used for communication between the two users.

### Subscriptions
- A **subscription** represents the stream of messages from a single, specific topic, to be delivered to the subscribing application.
- **User 1** subscribes to `user2-subscription`.
- **User 2** subscribes to `user1-subscription`.

## Setting Up Using Google Cloud Shell

### Step 1: Enable Google Cloud Pub/Sub API

Enable the Pub/Sub API for your Google Cloud project.

```
gcloud services enable pubsub.googleapis.com
```

### Step 2: Create a Service Account

Create a service account to interact with Pub/Sub.

```
gcloud iam service-accounts create my-pubsub-service-account \
    --description="Service account for Pub/Sub chat" \
    --display-name="Pub/Sub Service Account"
```

### Step 3: Assign Roles to the Service Account

Grant the necessary roles to the service account:
- `roles/pubsub.publisher`
- `roles/pubsub.subscriber`
- `roles/serviceusage.serviceUsageConsumer`

```
gcloud projects add-iam-policy-binding yopa-433507 \
    --member="serviceAccount:my-pubsub-service-account@yopa-433507.iam.gserviceaccount.com" \
    --role="roles/pubsub.publisher"

gcloud projects add-iam-policy-binding yopa-433507 \
    --member="serviceAccount:my-pubsub-service-account@yopa-433507.iam.gserviceaccount.com" \
    --role="roles/pubsub.subscriber"

gcloud projects add-iam-policy-binding yopa-433507 \
    --member="serviceAccount:my-pubsub-service-account@yopa-433507.iam.gserviceaccount.com" \
    --role="roles/serviceusage.serviceUsageConsumer"
```

### Step 4: Create a Key for the Service Account

Generate a key for the service account and download it as a JSON file.

```
gcloud iam service-accounts keys create ~/keyfile.json \
    --iam-account=my-pubsub-service-account@yopa-433507.iam.gserviceaccount.com
```

### Step 5: Set the GOOGLE_APPLICATION_CREDENTIALS Environment Variable

Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of your key file.

```
export GOOGLE_APPLICATION_CREDENTIALS="/home/your-username/keyfile.json"
```

### Step 6: Create the Pub/Sub Topic and Subscriptions

Create the topic `user1-user2` and the necessary subscriptions.

```
gcloud pubsub topics create user1-user2

gcloud pubsub subscriptions create user1-subscription --topic=user1-user2
gcloud pubsub subscriptions create user2-subscription --topic=user1-user2
```

### Step 7: Install Required Python Libraries

Install the Google Cloud Pub/Sub client library.

```
pip install google-cloud-pubsub
```

### Step 8: Run the Chat Application

Run the chat application for each user in separate terminals.

#### User 1

```
python chat.py 1
```

#### User 2

```
python chat.py 2
```

### Summary

This setup allows user1 and user2 to chat with each other using Google Cloud Pub/Sub. Each user publishes messages to a common topic and listens for messages on their respective subscriptions.