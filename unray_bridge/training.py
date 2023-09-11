from unray_bridge.bridge import Bridge

def train(algo, ip = 'localhost', port = 10011):
    print("[Bridge] Starting instance...")
    bridge = Bridge(ip, port) # Bridge control 
    print("[Bridge] Created!")

    bridge.start() # Begin Connection
    