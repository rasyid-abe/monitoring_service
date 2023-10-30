from apscheduler.schedulers.background import BackgroundScheduler
from apps.home.jobs.alert import AlertJobs
from apps.home.jobs.auto_switch import AutoSwitchJobs
from apps.home.jobs.cdc import CDCJobs
from apps.home.jobs.nifi import NifiJobs
from apps.home.jobs.etl_caller import start
from apps.home.jobs.validity_and_recovery_jobs import ValidityAndRecoveryJobs

def start_jobs():
    scheduler = BackgroundScheduler()

    cron_recovery = {'month': '*', 'day': '*', 'hour': '*', 'minute':'*/15'}
    cron_alert = {'month': '*', 'day': '*', 'hour': '*', 'minute':'*/10'}
    cron_nifi = {'month': '*', 'day': '*', 'hour': '*', 'minute':'*/15'}
    cron_cdc = {'month': '*', 'day': '*', 'hour': '4', 'minute':'0'}
    cron_auto_switch_report = {'month': '*', 'day': '*', 'hour': '*', 'minute':'*/10'}

    #Add our task to scheduler.
    scheduler.add_job(ValidityAndRecoveryJobs.data_recovery, 'cron', **cron_recovery)
    scheduler.add_job(AlertJobs.alert_check, 'cron', **cron_alert)
    # scheduler.add_job(NifiJobs.nifi_restart, 'cron', **cron_nifi)
    scheduler.add_job(CDCJobs.check, 'cron', **cron_cdc)
    scheduler.add_job(AutoSwitchJobs.check, 'cron', **cron_auto_switch_report)
    scheduler.add_job(start, 'interval', seconds=10)

    #And finally start.
    scheduler.start()
