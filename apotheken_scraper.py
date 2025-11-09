import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
import time

def scrape_Maps(standort, limit=100):
    """
    Sucht auf Google Maps, scrollt und extrahiert Name und Website mit aktualisierten Selektoren.
    """
    driver = webdriver.Chrome()
    driver.get("https://www.google.com/maps")
    wait = WebDriverWait(driver, 20) # Wartezeit etwas erhöht

    try:
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "searchboxinput")))
        search_box.send_keys(f"Apotheke in {standort}")
        search_box.send_keys(Keys.ENTER)
        
        # Warten, bis das Scroll-Panel (der "Feed") geladen ist
        results_panel = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='feed']")))
        time.sleep(3) # Kurze Pause, damit erste Ergebnisse rendern
    except TimeoutException:
        print("Fehler: Das Suchfeld oder die Ergebnisliste konnte nicht gefunden werden.")
        driver.quit()
        return []

    apotheken = []
    gefundene_namen = set() 

    while len(apotheken) < limit:
        # AKTUALISIERTER SELEKTOR für jeden einzelnen Eintrag in der Liste
        results = driver.find_elements(By.CSS_SELECTOR, "div.Nv2PK")
        
        if not results:
            print("Konnte keine Ergebnis-Einträge mit 'div.Nv2PK' finden. Breche ab.")
            break

        for result in results:
            try:
                # AKTUALISIERTER SELEKTOR für den Namen
                name_element = result.find_element(By.CSS_SELECTOR, "div.qBF1Pd")
                name = name_element.text
                
                if name in gefundene_namen:
                    continue

                website_button = result.find_elements(By.CSS_SELECTOR, "a[data-value='Website']")
                website_url = website_button[0].get_attribute('href') if website_button else 'N/A'
                
                print(f"Gefunden: {name}")
                apotheken.append({'Name': name, 'Website': website_url})
                gefundene_namen.add(name)

                if len(apotheken) >= limit:
                    break
            except Exception:
                continue
        
        if len(apotheken) >= limit:
            print(f"Limit von {limit} Apotheken erreicht.")
            break

        last_height = driver.execute_script("return arguments[0].scrollHeight", results_panel)
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", results_panel)
        time.sleep(2.5)
        new_height = driver.execute_script("return arguments[0].scrollHeight", results_panel)

        if new_height == last_height:
            print("Ende der Ergebnisliste erreicht.")
            break
            
    driver.quit()
    return apotheken[:limit]

def find_email_on_website(url, driver):
    """
    Besucht eine URL und sucht nach einer E-Mail-Adresse.
    """
    if not url or url == 'N/A':
        return 'Keine Website gefunden'
    
    try:
        driver.get(url)
        time.sleep(2)
        email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_regex, driver.page_source)
        
        for email in emails:
            if not email.endswith(('.png', '.jpg', '.gif', '.webp')):
                return email
        return 'Keine E-Mail gefunden'
    except WebDriverException:
        return 'Fehler beim Laden der Website'

# === HAUPTSKRIPT ===
if __name__ == "__main__":
    standort = "Oetwil am See"
    # Die Funktion wird nun mit dem Standardlimit von 200 aufgerufen
    apotheken_basis_daten = scrape_Maps(standort, limit=100)
    
    if not apotheken_basis_daten:
        print("Keine Apotheken gefunden. Das Skript wird beendet.")
    else:
        print(f"\n{len(apotheken_basis_daten)} Apotheken gefunden. Suche nun nach E-Mails...")
        email_driver = webdriver.Chrome()
        vollstaendige_daten = []

        for i, apotheke in enumerate(apotheken_basis_daten):
            print(f"({i+1}/{len(apotheken_basis_daten)}) Suche E-Mail für: {apotheke['Name']}...")
            email = find_email_on_website(apotheke['Website'], email_driver)
            apotheke['E-Mail'] = email
            vollstaendige_daten.append(apotheke)

        email_driver.quit()

        df = pd.DataFrame(vollstaendige_daten)
        dateiname = f"apotheken_daten_{standort}.csv"
        df.to_csv(dateiname, index=False, encoding='utf-8-sig')
        print(f"\nAlle Daten wurden erfolgreich in '{dateiname}' gespeichert.")
        print(df.head()) # Zeigt die ersten paar Zeilen des Ergebnisses an