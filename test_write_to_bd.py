import subprocess
import os
from stat import S_IREAD, S_IRGRP, S_IROTH
from peewee import *
import peewee
import datetime

user = 'postgres'
password = '123qweasd'
# password = '10081982'
db_name = 'test_db'
port = 5432

dbhandle = PostgresqlDatabase(
    db_name,
    user=user,
    password=password,
    host='localhost',
    port=port
)

### д.б. в файле моделей ###
class BaseModel(Model):
    class Meta:
        database = dbhandle

class Settings(BaseModel):
    #id = PrimaryKeyField(null=False)
    #event_type = CharField(max_length=20)
    #Status = TextField(default=None)
    #Color = TextField(default=None)
    #Info = TextField(default=None)
    #DateTime = TextField(default=None)

    id = PrimaryKeyField(null=False)
    uid = CharField(max_length=20)
    sensor_mode = CharField(max_length=20)
    pkoke = CharField(max_length=20)
    dev_id = IntegerField()
    fimvare_version = IntegerField()
    work_mode = IntegerField()
    fill_sensor = IntegerField()
    flip_sensor = IntegerField()
    temperature = IntegerField()
    last_comm_time = DateTimeField()
    latitude = DecimalField()
    longitude = DecimalField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    opsos_id = IntegerField()
    state = CharField(max_length=20)
    control_geolocation = BooleanField()
    hijacking = BooleanField()
    need_reair = BooleanField()
    need_replacement = BooleanField()

    class Meta:
        db_table = "sensors_sensorunit"

#######################
def add_unit_settings(uid1, sensor_mode1,pkoke1,dev_id1,
fimvare_version1,work_mode1,fill_sensor1,flip_sensor1,temperature1,
last_comm_time1,latitude1,longitude1,created_at1,updated_at1,
opsos_id1,state1,control_geolocation1,hijacking1,need_reair1,
need_replacement1):
    row = Settings(
    uid = uid1.lower().strip(),
    sensor_mode = sensor_mode1.lower().strip(),
    pkoke = pkoke1.lower().strip(),
    dev_id = dev_id1.lower().strip(),
    fimvare_version = fimvare_version1.lower().strip(),
    work_mode = work_mode1.lower().strip(),
    fill_sensor = fill_sensor1.lower().strip(),
    flip_sensor = flip_sensor1.lower().strip(),
    temperature = temperature1.lower().strip(),
    last_comm_time = last_comm_time1.lower().strip(),
    latitude = latitude1.lower().strip(),
    longitude = longitude1.lower().strip(),
    created_at = created_at1.lower().strip(),
    updated_at = updated_at1.lower().strip(),
    opsos_id = opsos_id1.lower().strip(),
    state = state1.lower().strip(),
    control_geolocation = control_geolocation1.lower().strip(),
    hijacking = hijacking1.lower().strip(),
    need_reair = need_reair1.lower().strip(),
    need_replacement = need_replacement1.lower().strip()
    )
    row.save()
    # else:
    #     cur_settings.Unit = unit
    #     cur_settings.Status = status
    #     cur_settings.Color = color
    #     cur_settings.Info = info
    #     cur_settings.DateTime = datetime
    #     cur_settings.save()

if __name__ == '__main__':
    try:
        dbhandle.connect()

        tables = dbhandle.get_tables()
        # Проверяем наличие таблицы с именем 'settings'
        if tables.count('sensors_sensorunit') == 0:
            print("Create table 'settings'")
        else:
            Settings.create_table()
            print("Table 'settings' is exist!")
        while True:
            #time = datetime.datetime.today().strftime("%Y-%m-%d-%H:%M:%S")
            #message = {}
            #message["unit"] = random.choice(units)
            #message["status"] = random.choice(status)
            #message["color"] = random.choice(color)
            #message["info"] = random.choice(info)
            #message["datetime"] = time

            #print("message", message)

            add_unit_settings(uid1 = 1, sensor_mode1 = 1,
                              pkoke1 = 1,
                              dev_id1 = 1,
                              fimvare_version1 = 1,
                              work_mode1 = 1,
                              fill_sensor1 = 1,
                              flip_sensor1 = 1,
                              temperature1 = 1,
                              last_comm_time1 = 1,
                              latitude1 = 1,
                              longitude1 = 1,
                              created_at1 = 1,
                              updated_at1 = 1,
                              opsos_id1 = 1,
                              state1 = 1,
                              control_geolocation1 = 1,
                              hijacking1 = 1,
                              need_reair1 = 1,
                              need_replacement1 = 1)
    except peewee.InternalError as px:
        print(str(px))