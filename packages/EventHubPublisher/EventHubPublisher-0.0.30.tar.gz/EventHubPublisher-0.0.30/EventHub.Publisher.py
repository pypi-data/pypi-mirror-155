import sys, os
from pathlib import Path

currentDirectory = os.getcwd()
#eventHubDirectory = currentDirectory + "\EventPublisher\EventHub"
#settingsDirectory = currentDirectory + "\EventPublisher\Settings"
eventPublisherDirectory = currentDirectory + "\EventPublisher"
#path = Path(currentDirectory) 
#absolutePath = str(path.parent.absolute())
sys.path.append(eventPublisherDirectory)
#sys.path.append(currentDirectory)
#sys.path.append(eventHubDirectory)
#sys.path.append(settingsDirectory)
#sys.path.append(absolutePath)

# change the current directory so we can read the settings.json
os.chdir(eventPublisherDirectory)

import EventHub.SendEvents as SendEvents
import EventPublisher.Publisher as Publisher

json = '{"environment":"Development", "eventType":"OrderWrittenSale", "clientCode":"fla-105-code", "accountName":"fla-105", "data":[{"entityId":"a"}]}'

respose = Publisher.run(json)
print(respose)