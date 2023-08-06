import sys, os, JsonParser, SupportedEvents, traceback
from os.path import dirname, abspath
from EventHub.Response import Response

sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append(dirname(dirname(abspath(__file__))))

import EventHub.SendEvents as SendEvents

def validate_event_type(event_type):
    if not event_type in SupportedEvents.EVENTS:
        raise Exception(event_type + " is not valid event type. Valid events are: " + JsonParser.serialize(SupportedEvents.EVENTS))

def run(eventData):
    try:
        event = JsonParser.parse(eventData)
        env_name = JsonParser.get_by_key(event, "environment")
        event_type = JsonParser.get_by_key(event, "eventType")
        client_code = JsonParser.get_by_key(event, "clientCode")
        account_name = JsonParser.get_by_key(event, "accountName")
        events_data = JsonParser.get_by_key(event, "data")

        #validate event type
        validate_event_type(event_type)

        return SendEvents.send_events(event_type, env_name, client_code, account_name, events_data)
    except Exception as eh_err:
        return Response(False, traceback.format_exc()).toJSON()

## for testing 
if sys.stdin and len(sys.argv) > 1:
    print(SendEvents.run())
    print('Events were sent.')


