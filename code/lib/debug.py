# Diese Datei ist einfach um Fehler zu finden und um den ganzen Prozess zu loggen
# Die Datei ist nicht wirklich eine Library, aber trotzdem praktisch

#
# JJK Electronics©
#


import utime
import uos as os

# Hiermit kann man einschalten ob 'DEBUG' getaggte Logs angezeigt werden sollen oder nicht
debug = True

ALLOWED_LEVELS = ["INFO", "BOOT", "INIT", "SYSTEM", "ERROR", "WARN", "SECURITY", "DEBUG"]

# INFO für alles andere
# BOOT für Boot Logs
# INIT für Initialisierungen
# SYSTEM für Systemmeldungen
# ERROR für Fehler
# WARN für Warnungen
# SECURITY einfach so
# DEBUG für Debug

def get_timestamp():

    t = utime.localtime() # t = time
    return f"{t[0]:04d}-{t[1]:02d}-{t[2]:02d} {t[3]:02d}:{t[4]:02d}:{t[5]:02d}"

def println(message, level="INFO"):

    if level not in ALLOWED_LEVELS:
        level = "INFO" 
    
    if level == "DEBUG" and not debug:
        return
    
    timestamp = get_timestamp()
    #print(f"[{timestamp}] [{level}] {message}")
    log_entry = f"[{timestamp}] [{level}] {message}"

    with open('logs/latest.log', 'a') as log_file:
        log_file.write(log_entry + "\n")
    
    print(log_entry)

def save_log():
    log_dir = "/logs"
    latest_log = log_dir + "/latest.log"

    try:
        os.stat(latest_log)
    except OSError:
        return  # Datei existiert nicht

    i = 1
    while True:
        new_log = f"{log_dir}/{i}.log"
        try:
            os.stat(new_log)
            i += 1
        except OSError:
            break

    os.rename(latest_log, new_log)
    print(f"Log wurde umbenannt in: {new_log}")

if __name__ == "__main__":
    input("Hinweis: Diese Datei dient ausschließlich als Bibliothek und ist nicht für den direkten Zugriff bestimmt.\n\nDrücke Enter zum beenden...")
