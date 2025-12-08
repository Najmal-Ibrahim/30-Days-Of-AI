import json
#THE RAW DATA (Imagine this came from a server log file)
server_log = """
[INFO] User admin logged in from IP 192.168.1.1
[WARNING] Failed login attempt from IP 203.0.113.5
[INFO] System update completed
[WARNING] Suspicious activity detected from IP 10.0.0.55
"""
def process_logs():
    print("---STRATING THE LOG ANALYSIS---")
     # 2. LISTS 
    
    suspicious_events =[]
    
    #3.SPLITING
    log_lines = server_log.strip().split('\n')

     #4.LOOP
    for line in log_lines:
      
      #5.LOGIC
      if "WARNING" in line:
        #extract the IP addresss
        ip_address =line.split('IP')[1]
        #DICTIONARY(THE STRUCTURED DATA)
        event_data={
          "type":"Security Alert",
          "ip":ip_address,
          "status":"Risky"
        }
        #add this to our list
        suspicious_events.append(event_data)
    #7.OUTPUT
    print(f"Found{len(suspicious_events)} threats.")
    #Convert our list to a JSON string
    print(json.dumps(suspicious_events,indent=2))

if __name__=="__main__":
  process_logs()

