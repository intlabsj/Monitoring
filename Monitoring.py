import os, time, sys
import multiprocessing
from AnomalyDetector import StopEventEmitter
import shutil
from confluent_kafka import Producer

def checkFolder(car_id, m):
    if m == "car": e = "vehicle"
    elif m == "etc": e = "object"
    else: e = m

    fpath = os.path.abspath(f"data/input/stop/{m}/MONITOR-CAR-0{car_id}")
    while True:
        flist = os.listdir(fpath)
        for fl in flist:
            if fl == "log": continue
            if fl == "test": continue
            if e == "person":
                pass
            else:
                stime = time.strftime("%Y-%m-%d %H_%M_%S", time.localtime(int(fl.split('_')[0])))
                stime += '.' + fl.split('_')[1][:3]
                se = StopEventEmitter(f"MONITOR-CAR-0{car_id}", os.path.join(fpath, fl), stime)
                event = se.MakeStopEvent(e)

                producer = Producer({'bootstrap.servers': "172.18.192.102:9092"})
                producer.produce(topic="event", value=event)
                producer.flush()

                print(event)

            if os.path.exists(os.path.join(fpath, "log/", fl)):
                shutil.rmtree(os.path.join(fpath, "log/", fl))
            shutil.move(os.path.join(fpath, fl), os.path.join(fpath, "log/"))

if __name__ == "__main__":
    car_id = 1

    if car_id < 5:
        carProcess = multiprocessing.Process(target=checkFolder, args=(car_id, 'car'))
        etcProcess = multiprocessing.Process(target=checkFolder, args=(car_id, 'etc',))
        perProcess = multiprocessing.Process(target=checkFolder, args=(car_id, 'person'))

        carProcess.start()
        etcProcess.start()
        perProcess.start()

    else:
        car_id = 5
        checkFolder(car_id=car_id, m="none")