from servicenow import snow
from archer import archer

arch = archer()
snow = snow()

snowIssueDataArray = snow.getRecords(table='sn_grc_issue',query='',fields='issue_type,number,sys_id,short_description,description')

for issue in snowIssueDataArray:
    print('*****')
    print(issue)
    print('*****')

    rec = archer.recordBuilder(levelID=62)
    if(issue['short_description'] != ''):
        rec.addField(fieldID=2670,type=1,value=issue['short_description'])
    else:
        rec.addField(fieldID=2670,type=1,value='Short Description not available')
    if(issue['description'] != ''):
        rec.addField(fieldID=2265,type=1,value=issue['description'])
    else:
        rec.addField(fieldID=2265,type=1,value='Description not available')
    rec.addField(fieldID=28795,type=1,value=issue['sys_id'])
    recordId = arch.createRecords(rec.getJSON())
    snowJSON = {"u_archer_trackig_id":recordId}
    snow.updateRecord(table='sn_grc_issue',id=issue['sys_id'],record=snowJSON)
    print('___________________________________________________')
    
    