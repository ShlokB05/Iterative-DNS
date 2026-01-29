# Recursive DNS System (LS / RS / TS1 / TS2 / AS)

This project implements a simplified **recursive DNS resolution system** using multiple servers with a local server cache:

- **LS** (Local Server / Resolver)
- **RS** (Root Server)
- **TS1** (Top-Level Server 1)
- **TS2** (Top-Level Server 2)
- **AS** (Authoritative Server)
- **Client** (requests hostname lookups)

The system resolves hostnames to IP addresses using iterative delegation (`ns`) and authoritative answers (`aa`), and supports negative responses (`nx`).

---

## Project Components

| Component | File | Role |
|----------|------|------|
| Client | `client.py` | Sends hostname queries to LS and writes `resolved.txt` |
| LS | `ls.py` | Resolver; queries RS/TS/AS and optionally caches results |
| RS | `rs.py` | Root server; delegates to TS/AS depending on DB |
| TS1 | `ts1.py` | TLD server; responds `aa`/`nx` based on DB |
| TS2 | `ts2.py` | TLD server; responds `aa`/`nx` based on DB |
| AS | `as.py` | Authoritative server; responds `aa`/`nx` based on DB |

---

## Overview:
Each server loads its own local database file on startup:
    If a match is found, the response must contain the **domain name exactly as stored** in that server’s database. If a match is not found, then the client recieves a response that states that the server was not found. 


## How to Run

### Start servers:

1) Start the two TS servers first, then RS, then LS, then AS, and finally the client. It is highly recommended to start all 6 servers locally with a shared port, however, this project does work across different server instances. 

command to run:
    python3 <ServerName>.py port