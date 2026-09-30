import urllib.request
import json

BASE = "http://127.0.0.1:8000/api"

def test_endpoint(name, url, method="GET", data=None):
    try:
        req = urllib.request.Request(url, method=method)
        req.add_header("Content-Type", "application/json")
        body = json.dumps(data).encode("utf-8") if data else None
        with urllib.request.urlopen(req, data=body, timeout=5) as res:
            status = res.status
            content = json.loads(res.read().decode("utf-8"))
            print(f"[PASS] {name}: Status {status}, Keys: {list(content.keys()) if isinstance(content, dict) else len(content)}", flush=True)
            return True
    except Exception as e:
        print(f"[FAIL] {name}: {e}", flush=True)
        return False

if __name__ == "__main__":
    print("Testing All Cyclopath AI Endpoints...", flush=True)
    test_endpoint("Root", "http://127.0.0.1:8000/")
    test_endpoint("Cyclones", f"{BASE}/cyclones")
    test_endpoint("Infrastructure", f"{BASE}/infrastructure")
    test_endpoint("Risk Summary", f"{BASE}/risk/summary")
    test_endpoint("Simulation Run", f"{BASE}/simulation", method="POST", data={"wind_speed_kmh": 180, "rainfall_mm": 400, "storm_surge_m": 5.0})
    test_endpoint("AI Agent Query", f"{BASE}/agent/query", method="POST", data={"query": "Which hospitals need backup power?", "district": "Puri", "language": "en"})
    test_endpoint("Route Optimize", f"{BASE}/routes/optimize", method="POST", data={"start_lat": 19.821, "start_lng": 85.845, "end_lat": 20.231, "end_lng": 85.778})
    test_endpoint("Alerts Feed", f"{BASE}/alerts")
    test_endpoint("Latest Report", f"{BASE}/reports/latest")
    test_endpoint("Health Observability", f"{BASE}/health")
    test_endpoint("Data Sources", f"{BASE}/data-sources")
    print("All Integration Tests Completed!", flush=True)
