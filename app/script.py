from evaluations_api.api import Ged,Preds,Countries,Metrics,Scheduler
#scheduler = Scheduler("http://0.0.0.0:8003")

scheduler_hostname = "http://0.0.0.0:8003"
scheduler = Scheduler(scheduler_hostname)

ged = Ged(scheduler_hostname,"http://0.0.0.0:8001")
preds = Preds(scheduler_hostname,"http://0.0.0.0:8002")
metrics = Metrics(scheduler_hostname,"http://0.0.0.0:8004")

countries = Countries("http://0.0.0.0:8002")

data = ged.points(432,-1)
dates = {ftr["properties"]["date_start"] for ftr in data["features"]}

print(len(data["features"]))
print(min(dates))
print(max(dates))
