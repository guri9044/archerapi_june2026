from servicenow import snow
from archer import archer
import logging
import os
import datetime
import json

if not os.path.exists("Logs"):
    os.makedirs("Logs")
currentDate = datetime.datetime.now().strftime("%Y-%m-%d")
logFileName = os.path.join("Logs",f"ArcherServiceNowIntegration.{currentDate}.log")
arch = archer()
snow = snow()

# Configure logging
loggerMain = logging.getLogger(__name__)
mainHandler = logging.FileHandler(logFileName)
mainHandler.setLevel(logging.INFO)
mainHandler.setFormatter(logging.Formatter("%(asctime)s - [%(levelname)s] - %(message)s"))
loggerMain.addHandler(mainHandler)
with open('config.json','r')as f:
    config = json.load(f)

# ServiceNow Issues to Archer Findings integration
stamappingConfig = config['mapping']['snowToArcher']
snowIssueDataArray = snow.getRecords(table=stamappingConfig['source'],query='',fields=stamappingConfig['sourceFields'])
success = 0
failed = 0
for issue in snowIssueDataArray:
    print('*****')
    print(issue)
    loggerMain.info(f"ServiceNow Issue : {issue}")
    print('*****')

    rec = arch.recordBuilder(levelID=stamappingConfig['targetLevelId'])
    for mapping in stamappingConfig['mappings']:
        snowField = mapping['snow']
        if((mapping['archerType'] == 1 or mapping['archerType'] == 2 or mapping['archerType'] == 3) and issue[snowField] != ''):
            rec.addField(fieldID=mapping['archer'],type=mapping['archerType'],value=issue[snowField])
        
        elif((mapping['archerType'] == 1 or mapping['archerType'] == 2 or mapping['archerType'] == 3) and issue[snowField] == ''):
            rec.addField(fieldID=mapping['archer'],type=mapping['archerType'],value=f'{snowField} value not available in ServiceNow')

        elif(mapping['archerType'] == 4 and issue[snowField] != ''):
            if(issue[snowField] in mapping['valueListMapping']):
                targetVLID = mapping['valueListMapping'][issue[snowField]]
            else:
                targetVLID = mapping['valueListMapping']['default']
            input = {
                "ValuesListIds" : [targetVLID]
            }
            rec.addField(fieldID=mapping['archer'],type=mapping['archerType'],value=input)
        
        elif(mapping['archerType'] == 4 and issue[snowField] == ''):
            targetVLID = mapping['valueListMapping']['default']
            input = {
                "ValuesListIds" : [targetVLID]
            }
            rec.addField(fieldID=mapping['archer'],type=mapping['archerType'],value=input)
    print(rec.getJSON())
    # recordId = arch.createRecords(rec.getJSON())
    # if(recordId != None):
    #     success+=1
    #     snowJSON = {"u_archer_trackig_id":recordId}
    #     snow.updateRecord(table='sn_grc_issue',id=issue['sys_id'],record=snowJSON)
    # else:
    #     failed+=1
    # print(f"Total records processed: {success+failed}")
    # print(f"Success : {success}")
    # print(f"Failed : {failed}")    
    # print('___________________________________________________')
    
    