import asyncio
from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient

class EventHubProducer:
    def __init__(self, connection_string, eventhub_name):
        if not connection_string or connection_string is None:
            raise Exception("Event HUB connection string is not configured. Make sure it is added to settings.json")
        if not eventhub_name or eventhub_name is None:
            raise Exception("Event HUB name is not configured. Make sure it is added to settings.json")

        self.connection_string = connection_string
        self.eventhub_name = eventhub_name

    def create_event_data(self, event_body, client_code, account_name, event_type):
        event_data = EventData(str(event_body))
        event_data.properties = {'event_type': event_type, 'client_code': client_code, 'account_name': account_name}
        return event_data

    async def create_batch_with_partition_key(self, partition_key, event_type, client_code, account_name, events):
        #Create batch with partition key
        event_data_batch_with_partition_key = await self.producer.create_batch(partition_key=partition_key)

        #Add events to the batch.
        length = len(events)
        for index in range(0, length):
            event_data = self.create_event_data(events[index], client_code, account_name, event_type)
            event_data_batch_with_partition_key.add(event_data)

        return event_data_batch_with_partition_key

    def send_batch_with_partition_key(self, partition_key, event_type, client_code, account_name, events):  
        self.producer = EventHubProducerClient.from_connection_string(
            conn_str=self.connection_string, 
            eventhub_name=self.eventhub_name)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        event_data_batch_with_partition_key = loop.run_until_complete(self.create_batch_with_partition_key(partition_key, event_type, client_code, account_name, events))
        event_hub_send_batch_result = loop.run_until_complete(self.producer.send_batch(event_data_batch_with_partition_key))
        loop.close()
        
        return event_hub_send_batch_result
