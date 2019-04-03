from crontab import CronTab

cron = CronTab(user=True)  
job = cron.new(command='python3 /home/vatsal/Documents/IIIT/Sem-2/IAS/Hackathon_2/example1.py')  
job.minute.every(1)

cron.write()