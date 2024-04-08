# Tiny Scanner

Tiny Scanner est un scanner de port simple écrit en Python. Il permet de vérifier si les ports TCP/UDP sur une machine distante sont ouverts ou fermés.

## Fonctionnalités

- Scan de ports TCP.
- Scan de ports UDP avec détection basique des ports fermés via les réponses ICMP.
- Prise en charge de la spécification d'un seul port ou d'une plage de ports à scanner.
- Définition d'un timeout pour les connexions TCP et les écoutes UDP.

## Prérequis

- Python 3.x
- Privilèges root (pour les scans UDP, nécessaires pour créer des sockets RAW)

## Utilisation

Pour utiliser Tiny Scanner, exécutez le script depuis la ligne de commande avec les paramètres appropriés.

### Paramètres

- `-u, --udp` : Spécifie l'adresse de l'hôte pour un scan UDP.
- `-t, --tcp` : Spécifie l'adresse de l'hôte pour un scan TCP.
- `-p, --port` : Spécifie le port ou la plage de ports à scanner. Les plages de ports doivent être séparées par un tiret (e.g., `80-90`).

### Exemples

Scan d'un port TCP spécifique :

```sh
python3 tinyscanner.py -t 127.0.0.1 -p 22
```

Scan d'une plage de ports UDP :

```sh
sudo python3 tinyscanner.py -u 127.0.0.1 -p 1-1000
```

### Remarques

- Le scan UDP utilise des sockets RAW pour écouter les réponses ICMP. Cela nécessite des privilèges root pour exécuter le script.
- Les scans UDP ne peuvent pas toujours déterminer avec précision si un port est ouvert en raison de la nature sans connexion de l'UDP et du filtrage possible des paquets ICMP par des pare-feu.
- Pour les scans UDP, un timeout de 5 secondes est utilisé pour les réponses ICMP. Vous pouvez ajuster ce délai en modifiant la variable `timeout` dans la fonction `scan_udp_port(host, port, timeout=5)` du script, ligne 34.
- Les performances de ce script peuvent être améliorées en utilisant des threads pour les scans de ports multiples.