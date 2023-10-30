from apps.home.Models.apps import *
from apps.home.Models.airflow import *
from apps.home.Models.etl_history import *
from apps.home.Models.recovery_history import *
from apps.home.apis.nifi_apis import NifiApis
from django.utils import timezone
from datetime import time


class ValidityAndRecoveryJobs:

    @classmethod
    def data_recovery(cls):

        # get validity and recovery scheduler data        
        schedules = ValidityAndRecoveryScheduler.objects.all()

        # get current time
        current_time = timezone.localtime()
        current_time = (current_time.hour * 60) + current_time.minute   

        # get data yang akan di eksekusi
        for item in schedules:

            if item.cron_state == -1:
                continue

            print('[Validity & Recovery] checking : ' + item.etl_name)
            print('')

            start_at = item.start_at
            start_at = (start_at.hour * 60) + start_at.minute

            end_at = item.end_at
            end_at = (end_at.hour * 60) + end_at.minute
            
            # cek jika ada proses masuk ke rentang waktu cron
            if current_time >= start_at and current_time < end_at:
                # get processors
                nifi_processor_groups = cls.get_nifi_processor_group()
                etl_processors = NifiApis.get_nifi_processors(nifi_processor_groups[item.etl_name])
                recovery_processors = NifiApis.get_nifi_processors(nifi_processor_groups[item.recovery_name])
                
                if item.cron_state == 0:

                    # mematikan proses ETL berjalan
                    print('[Validity & Recovery] Stopping ETL for : ' + item.etl_name)
                    cls.change_processor_status(etl_processors, 'STOPPED')

                    # melakukan recovery selang 10 menit
                    if current_time >= (start_at + 5):
                        print('[Validity & Recovery] Starting recovery for : ' + item.recovery_name)
                        cls.change_processor_status(recovery_processors, 'RUNNING')
                        
                        # penanda recovery sedang dilakukan
                        item.cron_state = 1
                        item.save()
            else:
                # proses recovery masih berlangsung
                if item.cron_state == 1:
                    # get processors
                    nifi_processor_groups = cls.get_nifi_processor_group()
                    etl_processors = NifiApis.get_nifi_processors(nifi_processor_groups[item.etl_name])
                    recovery_processors = NifiApis.get_nifi_processors(nifi_processor_groups[item.recovery_name])
                
                    # matikan proses recovery
                    print('[Validity & Recovery] Stopping recovery for : ' + item.recovery_name)
                    cls.change_processor_status(recovery_processors, 'STOPPED')
                    
                    if current_time >= (end_at + 5):
                        # menyalakan kembali ETL
                        print('[Validity & Recovery] Starting ETL for : ' + item.etl_name)
                        cls.change_processor_status(etl_processors, 'RUNNING')
                    
                        item.cron_state = 0
                        item.save()

    @classmethod
    def get_nifi_processor_group(cls):
        # get nifi processor groups
        _, _, raw_nifi_processor_groups = NifiApis.get_nifi_status()

        nifi_processor_groups = {}
        for item in raw_nifi_processor_groups:
            nifi_processor_groups[item['name']] = item['id']
        
        return nifi_processor_groups

    @classmethod
    def change_processor_status(cls, processors, action):
        """
        action = 1 : start
        action = 0 : stop
        """

        # update nifi
        for item in processors:
            processorId = item['id']
            version = item['version']
            clientId = item['clientId']
            
            _ = NifiApis.update_nifi_processor(processorId, version, clientId, action)
