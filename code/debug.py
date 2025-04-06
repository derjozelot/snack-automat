import utime

# Einfach um Debugs zu printen, kp warum genau, aber ist cool

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
    log_entry = f"[{timestamp}] [{level}] {message}\n"

    with open('1.txt', 'a') as log_file:
        log_file.write(log_entry)
    
    print(log_entry)

if __name__ == "__main__":
    input("Hinweis: Diese Datei dient ausschließlich als Bibliothek und ist nicht für den direkten Zugriff bestimmt.\n\nDrücke Enter zum beenden...")
