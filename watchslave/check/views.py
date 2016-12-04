from django.shortcuts import render
from django.template.loader import render_to_string
# Create your views here.
from django.http import HttpResponse
import urllib2,subprocess,json
from .models import ping_db,monitor_db
from celery.task.schedules import crontab
from celery.decorators import periodic_task

def run_ping(request):
	target=request.GET.get('target')
	if "/" in target:
		target2 = target.split("/")[0]
		target=target2
	reply=subprocess.check_output("ping -c 5 "+str(target), shell=True)
        packet_loss = reply.split('received,')[1]
	data = packet_loss.split(',')
	final = {}
	final['packet_loss']=data[0].split('%')[0]
	final['rtt']=data[1]
	if 'packet' in data[1]:
		return HttpResponse("")
	else:
		json_data = json.dumps(final)
		add_ping_log(str(target),json_data)
		return HttpResponse(json_data)

def get_ping_logs(request):
	target=request.GET.get('target')	
	all_logs=ping_db.objects.filter(target=target)
	content = {}
	for logs in all_logs:
		content[str(logs.timestamp)]=logs.result
	final = json.dumps(content)
	return HttpResponse(final)

def add_ping_log(target,respo):
	ping= ping_db(target=target,result=respo)
	ping.save()

def ping(target):
        reply=subprocess.check_output("ping -c 2 "+str(target), shell=True)
        packet_loss = reply.split('received,')[1]
        data = packet_loss.split(',')
        final = {}
        final['packet_loss']=data[0].split('%')[0]
        final['rtt']=data[1]
        json_data = json.dumps(final)
        add_ping_log(str(target),json_data)
import datetime
def cron_ping():
        targets=monitor_db.objects.filter(test=ping)
        for target in targets:
                ping(target)


def loading_test(request):
        target=request.GET.get('target')
        result=subprocess.check_output('curl -w "time_namelookup:%{time_namelookup},time_connect:%{time_connect},time_appconnect:%{time_appconnect},time_pretransfer:%{time_pretransfer},time_redirect:%{time_redirect},time_starttransfer:%{time_starttransfer},time_total:%{time_total}" -o /dev/null -s '+target, shell=True)
        final={}
        content = result.split(",")
        for items in content:
                final[items.split(":")[0]]=float(items.split(":")[1])
        return HttpResponse(json.dumps(final))

def get_ninety_number(target, concurrent_connections):
	result = subprocess.check_output("ab  -c " + str(concurrent_connections) + " -n 1000 " + str(target) + "/ " + " 2> /dev/null" + " | grep \"90%\" | awk ' { print $2 }'", shell=True)

	return str(result)

def max_user_count(request):
	target=request.GET.get('target')
	current_connections = 100
	value = get_ninety_number(target, current_connections)
	
	value = int(value.strip())
	while value < 1500 :
		current_connections = current_connections + 100
		if value >= 1500:
			break
		value = get_ninety_number(target, current_connections)
#	return HttpResponse(str(value))
	return HttpResponse(str(current_connections))
