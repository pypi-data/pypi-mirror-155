import argparse, JsonParser, traceback
from Settings.Configuration import Configuration
from EventHub.Response import Response
from EventHub.EventHubProducer import EventHubProducer

def run():
    events_json = JsonParser.parse(args.events)
    event_type = args.type
    client_code = args.code
    account_name = args.account
    env_name = args.env
    return send_events(event_type, env_name, client_code, account_name, events_json)

def send_events(event_type, env_name, client_code, account_name, events):
    try:
        configuration = Configuration()
        configuration.init(env_name)

        producer = EventHubProducer(configuration.get_connection_string(), configuration.get_eventhub_name())

        return send_batch_with_partition_key(event_type, event_type, client_code, account_name, events, producer)
    except Exception as eh_err:
        return Response(False, traceback.format_exc()).toJSON()  

def send_batch_with_partition_key(event_type, env_name, client_code, account_name, events, producer):
    try:
        if not isinstance(producer, EventHubProducer):
            raise Exception("producer is not valid.")

        if not event_type or event_type is None:
            raise Exception("event_type is not provided.")

        if not env_name or env_name is None:
            raise Exception("env_name is not provided.")

        if not account_name or account_name is None:
            raise Exception("account_name is not provided.")

        if not client_code or client_code is None:
            raise Exception("account_name is not provided.")

        if not isinstance(events, list):
            raise Exception("events is not valid.")

        producer.send_batch_with_partition_key(event_type, event_type, client_code, account_name, events)

        return Response(True, "").toJSON()
    except Exception as eh_err:
        return Response(False, traceback.format_exc()).toJSON()  

#Declare script parameters
parser = argparse.ArgumentParser()
parser.add_argument("--env", help="Sets environment. Development, Production, QA or Learn", type=str)
parser.add_argument("--code", help="Sets Storis client code", type=str)
parser.add_argument("--events", help="Sets Storis client code")
parser.add_argument("--account", help="Sets Storis Account name")
parser.add_argument("--type", help="Sets Storis Event type")

args, unknown = parser.parse_known_args()


    
