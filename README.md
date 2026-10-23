# jawara-billing

ISP Billing System (Sendi) — manajemen langganan, tagihan, pembayaran, autentikasi ke MikroTik/OLT via FreeRADIUS, dan integration API MikroTik.

## Fitur

- **Customer / Client** — simpan data pengguna, VLAN, status langganan
- **FreeRADIUS Auth** — AAA server: autentikasi pengguna jaringan
- **MikroTik API** — manajemen device 192.168.100.254:1998
- **OLT Management** — manage OLT/PON/ONU
- **Billing** — tagihan bulanan, pembayaran, status lunas/tempo
- **RBAC** — admin / operator / resseler

## Stacks

- **Backend**: FastAPI + SQLAlchemy + MariaDB (MySQL-compatible)
- **Frontend**: Vanilla HTML/CSS/JS SPA
- **Auth**: FreeRADIUS (AAA)
- **Network**: nft, ip, netplan (sudo ops)

## Quick Start

```bash
# 1. Clone & setup
make setup

# 2. Export config
cp .env.example .env
# edit .env (database, freeRADIUS, mikrotik)

# 3. Init database
make migrate

# 4. Start web panel
make run
```

## Roles

| Role | Access |
|---|---|
| admin | Full — all menus, user, tagihan, device |
| operator | Operational — reset IP, toggle VLAN, view log |
| resseler | Sales — paket/data promo, view langganan |

## Ports

| Port | Service |
|---|---|
| 793 | Web Panel (FastAPI) |
| 389 | FreeRADIUS |
| 3306 | MariaDB / MySQL |

## License

MIT © 2026 devmaker-id
