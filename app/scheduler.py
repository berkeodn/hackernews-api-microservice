from apscheduler.schedulers.background import BackgroundScheduler
from etl.etl_job import run_etl

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_etl, 'interval', minutes=5)
    scheduler.start()
