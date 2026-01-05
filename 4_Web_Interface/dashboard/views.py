import json
import Pyro4 # Make sure to install this: pip install Pyro4
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from .models import AppUser, EventLog, SensorData

# --- CONNECTION TO YOUR RPC SERVER ---
# This matches the URI printed in your black window
RPC_URI = "PYRO:safehouse@127.0.0.1:9090"

def get_rpc():
    """Connects to the RPC Server"""
    return Pyro4.Proxy(RPC_URI)

@ensure_csrf_cookie
def index(request):
    return render(request, 'index.html')

# --- 1. REGISTER (Send to RPC) ---
@require_POST
def api_register(request):
    try:
        data = json.loads(request.body)
        
        # We call the RPC Server -> It prints and saves to DB
        rpc = get_rpc()
        response = rpc.register_user(
            data.get('name'),
            data.get('email'),
            data.get('password'),
            data.get('role'),
            data.get('permissions')
        )
        return JsonResponse(response)
    except Exception as e:
        print(f"❌ RPC Connection Error: {e}")
        return JsonResponse({"status": "error", "message": "RPC Server is Offline"})

# --- 2. LOGIN (Send to RPC) ---
@require_POST
def api_login(request):
    try:
        data = json.loads(request.body)
        
        # We ask RPC to check credentials -> It prints the attempt
        rpc = get_rpc()
        response = rpc.login_user(
            data.get('email'),
            data.get('password')
        )
        return JsonResponse(response)
    except Exception as e:
        return JsonResponse({"status": "error", "message": "RPC Server is Offline"})

# --- 3. HARDWARE ACTIONS (Lights/Doors -> Send to RPC) ---
@require_POST
def set_state(request):
    try:
        data = json.loads(request.body)
        
        # We tell RPC to update the device -> It prints the action
        rpc = get_rpc()
        response = rpc.update_device(
            data.get('id'),
            data.get('value')
        )
        return JsonResponse(response)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

# --- 4. SENSORS (Script -> Django -> RPC) ---
@require_POST
def api_sensor_input(request):
    try:
        data = json.loads(request.body)
        
        # We forward sensor data to RPC -> It prints it
        rpc = get_rpc()
        response = rpc.send_sensor_data(
            data.get('type'),
            data.get('value'),
            data.get('unit')
        )
        return JsonResponse(response)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

# --- 5. READ DATA (Read directly from DB for the History Table) ---
# The RPC server writes the data, but Django reads it back for the UI.
def api_get_logs(request):
    try:
        # Get last 20 logs
        logs = EventLog.objects.all().order_by('-timestamp')[:20]
        data = [{"device": l.device_id, "action": l.action, "time": l.timestamp.strftime("%H:%M:%S")} for l in logs]
        return JsonResponse({"status": "success", "logs": data})
    except:
        return JsonResponse({"status": "success", "logs": []})

def api_get_sensors(request):
    try:
        # Get last 20 sensor readings
        sensors = SensorData.objects.all().order_by('-timestamp')[:20]
        data = [{"type": s.sensor_type, "value": s.value, "unit": s.unit, "time": s.timestamp.strftime("%H:%M:%S")} for s in sensors]
        return JsonResponse({"status": "success", "data": data})
    except:
        return JsonResponse({"status": "success", "data": []})