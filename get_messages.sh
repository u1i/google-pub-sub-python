# create subscription mytopic01
# gcloud pubsub subscriptions create mysub01 --topic=mytopic01

gcloud pubsub subscriptions pull mysub01 --limit=10 --auto-ack
