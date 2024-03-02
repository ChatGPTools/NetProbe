import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
import re
import socket

def ottieni_ip_interno():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        IP = s.getsockname()[0]
    except Exception as e:
        messagebox.showerror("Errore", f"Non è stato possibile ottenere l'IP interno: {e}")
        IP = 'Non rilevabile'
    finally:
        s.close()
    return IP

def estrai_notizie_e_ip():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Attenzione", "Inserire un URL valido.")
        return
    try:
        # Estrazione del nome host dall'URL
        hostname = url.split("//")[-1].split("/")[0]
        # Risoluzione dell'indirizzo IP del server utilizzando il nome host
        ip_pubblico = socket.gethostbyname(hostname)

        risposta = requests.get(url)
        risposta.raise_for_status()
        titoli = re.findall(r'<title>(.*?)</title>', risposta.text, re.DOTALL)
        ip_interno = ottieni_ip_interno()
        risultato_text.delete(1.0, tk.END)
        risultato_text.insert(tk.END, f"IP Pubblico del Server: {ip_pubblico}\n")
        risultato_text.insert(tk.END, f"IP Interno: {ip_interno}\n")
        risultato_text.insert(tk.END, "Titoli Estratti:\n")
        for titolo in titoli:
            risultato_text.insert(tk.END, f"{titolo.strip()}\n")
    except Exception as e:  # Cattura un'eccezione più generica per gestire sia errori di rete che errori HTTP
        messagebox.showerror("Errore", f"Errore durante la richiesta: {e}")


def informazioni_ip():
    ip = ip_entry.get()
    if not ip:
        messagebox.showwarning("Attenzione", "Inserire un indirizzo IP valido.")
        return
    try:
        url = f"http://ipinfo.io/{ip}/json"
        risposta = requests.get(url)
        risposta.raise_for_status()
        informazioni = risposta.json()
        risultato_text.delete(1.0, tk.END)
        risultato_text.insert(tk.END, f"Informazioni per l'IP {ip}:\n")
        for chiave, valore in informazioni.items():
            risultato_text.insert(tk.END, f"{chiave}: {valore}\n")
    except requests.RequestException as e:
        messagebox.showerror("Errore", f"Errore durante la richiesta dell'IP {ip}: {e}")

root = tk.Tk()
root.title("Web Scraping e IP Info GUI")
root.geometry("600x600")

# Configurazione dell'interfaccia per il web scraping di notizie e IP
tk.Label(root, text="URL Notizie:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)
tk.Button(root, text="Estrai Titoli e IP", command=estrai_notizie_e_ip).pack(pady=5)

# Configurazione dell'interfaccia per le informazioni IP
tk.Label(root, text="Indirizzo IP:").pack(pady=5)
ip_entry = tk.Entry(root, width=50)
ip_entry.pack(pady=5)
tk.Button(root, text="Ottieni Informazioni IP", command=informazioni_ip).pack(pady=5)

# Area di testo per i risultati
risultato_text = scrolledtext.ScrolledText(root, height=15)
risultato_text.pack(pady=10)

root.mainloop()
