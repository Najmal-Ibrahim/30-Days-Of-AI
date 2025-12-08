import datetime
import os

def log_progress():
    now=datetime.datetime.now()
    goal="Breaking into AI Engineering at Puch AI"
    print(f"--- LOG ENTRY ---")
    print(f"timestasmp: {now}")
    print(f"traget:{goal}")
    print("System:RTX 1080 (6GB)-Ready to Optimization")
    print("-"*20)

if __name__=="__main__":
    log_progress()    