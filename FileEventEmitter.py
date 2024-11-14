from uuid import uuid4
import json
def EventMaker(car_id, dtime, latitude=131, longitude=37, objId=0, tilt=0.,
                   block=0., damage=0., reason='', fpath=''):

    mId, lId, eId = str(uuid4()), str(uuid4()), str(uuid4())
    if tilt > 0:
        eType = "ET_INFRA_POSTPOINTCONDITION"
        eLevel = "CAUTION" if tilt < 10 else "WARNING"
        tail_event = f"objectId: {objId}, tilt: {tilt}, "
    elif block > 0: # 30~50 Caution
        eLevel = "CAUTION" if block < 50 else "WARNING"
        eType = "ET_INFRA_SAFETYSIGN"
        tail_event = f"objectId: {objId}, block: {block}, "
    elif damage > 0: # 20~30 Caution
        eLevel = "CAUTION" if damage < 30 else "WARNING"
        eType = "ET_INFRA_SAFETYCONDITION"
        tail_event = f"objectId: {objId}, damage: {damage}, "
    else:
        eType = "ET_INFRA_STOPPEDVEHICLE" if reason == 'vehicle' else "ET_INFRA_OBSTACLE"
        eLevel = "NORMAL" if eType == "ET_INFRA_STOPPEDVEHICLE" else "CRITICAL"
        tail_event = f"reason: {reason}, "
    # stop/etc/MONITOR-CAR-0X/~~~.png
    if fpath != '':
        if reason == "vehicle": fpath = f'stop/car/{car_id}/{fpath}'
        elif reason == "object": fpath = f'stop/etc/{car_id}/{fpath}'

    tail_event += f"file: {fpath}" + "}"

    lati = float("{:.8f}".format(latitude))
    longi = float("{:.8f}".format(longitude))

    event = dict()
    event["messageId"] = mId
    event["messageTime"] = dtime
    event["vehicleId"] = car_id
    event["locationData"] = {
        "locationId": lId,
        "locationTime": dtime,
        "latitude": lati,
        "longitude": longi,
        "speed": 0,
        "heading": 0,
        "accX": 0,
        "accY": 0,
        "accZ": 0,
        "routeSequenceNum": 0,
        "routeLinkId": "5000000014"
    }
    event["eventData"] = {
        "eventId": eId,
        "eventType": eType,
		"eventTime": dtime,
        "eventLevel": eLevel,
        "eventValue": "{" + f"timestamp: {dtime}, latitude: {lati}, longitude: {longi}, "

    }
    event["eventData"]["eventValue"] += tail_event

    return json.dumps(event)
