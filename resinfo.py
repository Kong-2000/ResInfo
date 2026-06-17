import urllib.request
import urllib.parse
import json

import os

API_KEY = os.environ.get("RESROBOT_API_KEY")
if not API_KEY:
    print("Missing API key.")
    print("Set it with: setx RESROBOT_API_KEY \"your-key-here\"  (Windows)")
    print("        or: export RESROBOT_API_KEY=\"your-key-here\"  (Mac/Linux)")
    print("Get a free key at https://www.trafiklab.se")
    exit(1)

BASE_URL = "https://api.resrobot.se/v2.1"

def _get(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def _transport_type(entry):
    product = entry.get("ProductAtStop") or entry.get("Product")
    if not product:
        return "Unknown"
    if isinstance(product, list):
        product = product[0]
    cls = str(product.get("cls", ""))
    name = product.get("name", "").lower()
    if cls in ("1", "2") or "tåg" in name or "sj" in name or "train" in name or "x2000" in name:
        return "Train"
    if cls == "4" or "pendel" in name or "commuter" in name:
        return "Commuter"
    if cls == "8" or "spårvagn" in name or "tram" in name:
        return "Tram"
    if cls == "16" or "tunnelbana" in name or "metro" in name:
        return "Metro"
    if cls == "32" or "buss" in name or "bus" in name:
        return "Bus"
    if cls == "64" or "färja" in name or "ferry" in name:
        return "Ferry"
    return product.get("catOut", "Unknown")[:8]

def _find_stop(name):
    encoded = urllib.parse.quote(name)
    url = f"{BASE_URL}/location.name?input={encoded}&format=json&accessId={API_KEY}"
    data = _get(url)
    stops = data.get("stopLocationOrCoordLocation", [])
    results = []
    for item in stops:
        stop = item.get("StopLocation")
        if stop:
            results.append(stop)
    return results

def _choose_station():
    while True:
        name = input("\nEnter station (e.g. Stockholm, Gothenburg): ").strip()
        if not name:
            print("  Please enter a name.")
            continue
        stops = _find_stop(name)
        if not stops:
            print("  No stations found. Try again.")
            continue
        print("\n  Stations found:")
        for i, s in enumerate(stops[:5], 1):
            print(f"  {i}. {s['name']}")
        while True:
            val = input("  Choose [1-5]: ").strip()
            if val.isdigit() and 1 <= int(val) <= len(stops[:5]):
                return stops[int(val) - 1]
            print("  Invalid choice.")

def get_departures():
    stop = _choose_station()
    stop_id = stop["extId"]
    stop_name = stop["name"]
    url = f"{BASE_URL}/departureBoard?id={stop_id}&format=json&accessId={API_KEY}&maxJourneys=20"
    data = _get(url)
    departures = data.get("Departure", [])
    if not departures:
        print("  No departures found.")
        return
    print(f"\n  Departures from {stop_name}")
    print("  " + "-" * 85)
    print(f"  {'Time':<7} {'Type':<11} {'Line':<12} {'Destination':<45} {'Status'}")
    print("  " + "-" * 85)
    for d in departures:
        time = d.get("time", "")[:5]
        name = d.get("name", "")[:11]
        direction = d.get("direction", "")
        rt = d.get("rtTime", "")[:5]
        status = f"Delayed {rt}" if rt and rt != time else "On time"
        typ = _transport_type(d)[:10]
        print(f"  {time:<7} {typ:<11} {name:<12} {direction:<45} {status}")
    print()

def get_arrivals():
    stop = _choose_station()
    stop_id = stop["extId"]
    stop_name = stop["name"]
    url = f"{BASE_URL}/arrivalBoard?id={stop_id}&format=json&accessId={API_KEY}&maxJourneys=20"
    data = _get(url)
    arrivals = data.get("Arrival", [])
    if not arrivals:
        print("  No arrivals found.")
        return
    print(f"\n  Arrivals to {stop_name}")
    print("  " + "-" * 85)
    print(f"  {'Time':<7} {'Type':<11} {'Line':<12} {'From':<45} {'Status'}")
    print("  " + "-" * 85)
    for a in arrivals:
        time = a.get("time", "")[:5]
        name = a.get("name", "")[:11]
        origin = a.get("origin", "")
        rt = a.get("rtTime", "")[:5]
        status = f"Delayed {rt}" if rt and rt != time else "On time"
        typ = _transport_type(a)[:10]
        print(f"  {time:<7} {typ:<11} {name:<12} {origin:<45} {status}")
    print()

def print_menu():
    print("\n" + "=" * 52)
    print("  ResInfo  -  Sweden Travel Information")
    print("=" * 52)
    print("  1. Departures from a station")
    print("  2. Arrivals to a station")
    print("  q. Quit")
    print("=" * 52)

def main():
    print_menu()
    while True:
        choice = input("\nChoose [1-2] or q: ").strip().lower()
        if choice == "q":
            print("  Goodbye!")
            break
        elif choice == "1":
            get_departures()
        elif choice == "2":
            get_arrivals()
        else:
            print("  Invalid choice. Type 1, 2 or q.")

if __name__ == "__main__":
    main()
