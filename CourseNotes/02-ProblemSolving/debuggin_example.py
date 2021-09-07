working = True

def print_status():
    if working:
        print("Hard at work.")
    else:
        print("Watching the Seahawks!")

for hour in range(8,24):
    print(f"Hour {hour}: ")
    print_status()
    # why are you always at work??