# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

"Botón de Pago" — a Flask frontend that lets a client (identified by cédula/RIF + email) look up
their outstanding invoices in a Mikrowisp ISP-billing backend and pay them via Pago Móvil (Banco
Plaza through Vippo, or Banesco / Mercantil through Instapago). Zelle/TDC flows are referenced in
the README as goals but are not implemented in the current routes.

## Commands

Setup:
```bash
virtualenv .venv -p /usr/bin/python3
source .venv/bin/activate
pip install -r requirements.txt
cp src/.env.sample src/.env   # then fill in real endpoints/tokens, see below
```

Run the dev server (Flask debug server on 0.0.0.0:8000):
```bash
python src/app.py
```
Must be launched from the project root — `src/app.py` and everything under `src/routes`/`src/utils`
import using the `src.` package prefix (e.g. `from src.utils.logger import logger`).

Run the rate/bank-list refresh job manually (normally cron-scheduled):
```bash
python src/crontab.py
```
Note: `src/crontab.py` uses *unprefixed* imports (`from utils.enviar_correo import ...`,
`import config as config`) instead of `src.*`. This only resolves because running `python
src/crontab.py` puts `src/` itself on `sys.path[0]`. Don't try to import `src.crontab` from
elsewhere — it will fail; it's meant to be invoked as a standalone script.

There is no test suite, linter, or formatter configured in this repo — don't assume `pytest`,
`ruff`, etc. exist.

Production deploys via Apache + `mod_wsgi` (see `src/boton_pago_frontend.wsgi`, which hardcodes
`/var/www/boton_pago_frontend/` and a specific Python site-packages path — update both if the venv
Python version or deploy path changes). Full Apache vhost config, self-signed cert generation, and
the crontab entry for the rate-refresh job are documented in `README.md`.

## Configuration split

Two separate config sources are used for different purposes — don't put secrets in one or static
lists in the other:

- **`src/config.py`** — static, non-secret Python constants: `lista_id` (CI/RIF prefixes),
  `lista_phone` (mobile operator prefixes), `correos_tasa_bcv` (alert email recipients),
  `pm_bancoplaza` / `pm_banesco` / `pm_mercantil` (receiving-account tuples: phone, bank name, RIF,
  logo, disabled flag — set the last element `True` to take a bank offline), `contacto_WhatsApp`.
- **`src/.env`** (loaded once, early, in `src/app.py` before any `src.*` submodules are imported) —
  all secrets and environment-specific values: `FLASK_SECRET_KEY`, `PATH_BASE`, Mikrowisp
  (`TOKEN_MW`, `ENDPOINT_*`), Vippo (`APIKEY_VIPPO`, `ACCOUNT_VIPPO`, `ENDPOINT_BASE_VIPPO`, ...),
  Instapago (`KEYID_IP`, `PUBLICKEYID_IP`, `ENDPOINT_BASE_IP`, ...), SMTP creds, `LOG_FILE`/`LOG_LEVEL`,
  and `PORCENTAJE_DEUDA_MINIMA` (see below). `src/.env.sample` only documents a subset of keys —
  treat the full key list actually read via `os.getenv(...)` across `src/utils/*` and
  `src/routes/**` as the source of truth.
- File paths like the BCV rate cache and bank list are always built as
  `os.getenv("PATH_BASE") + os.getenv("FILE_...")`, i.e. `PATH_BASE` must end in the right separator
  and the env is otherwise not portable across machines without editing it.

## Request/blueprint architecture

Each Flask blueprint lives under `src/routes/<name>_bp/` and owns its own `templates/`, `static/`,
and (except `home_bp`) a `templates/form_fields.py` / `form_fields_*.py` defining its WTForms.
Blueprints are registered in `src/app.py`. The payment flow is a straight pipeline through them,
state threaded via `flask.session`:

1. **`home_bp`** (`/`) — login-like gate: user submits cédula + email. `api_mw.buscar_cliente`
   looks the client up in Mikrowisp, cross-checks the email, then stores `datos_cliente` in the
   session and calls `flask_login.login_user`. There's no password — the MW lookup + email match
   *is* the auth. `User` (in `home_bp/templates/form_fields.py`) is a bare `UserMixin` wrapping
   `datos_cliente` from the session; `load_user` in `app.py` reconstructs it from
   `session["datos_cliente"]`.
2. **`pagos_bp`** (`/pagos`) — shows the client's total debt converted to Bs using a BCV rate that's
   read once per process from a cached file (`api_vippo.leer_tasa_bcv`, backed by
   `src/utils/tasa_bcv.txt`, module-level `tasa_bcv` global). Disables payment if the account is
   `RETIRADO` or has no debt. On submit, stores `monto_bs` in the session and redirects to bank
   selection.
3. **`pagomovil_bp/route_bancos.py`** (`/pagomovil_bancos`) — picks which Pago Móvil receiving bank
   (Mercantil, Banesco, or Banco Plaza — displayed in that order), driven by `config.pm_mercantil` /
   `config.pm_banesco` / `config.pm_bancoplaza` and one `SubmitField` per bank in
   `form_fields_bancos.py`.
4. **`pagomovil_bp/route_bancoplaza.py`**, **`route_banesco.py`**, **`route_mercantil.py`** — one
   near-identical route module per receiving bank; each collects the payer's Pago Móvil transfer
   details (payer ID, phone, issuing bank, reference, amount, date) via the shared
   `templates/form_fields_reportes.py` / `pagomovil_reportes.html`, then:
   - validates the transfer against the bank's gateway — Banco Plaza uses `api_vippo.validar_pago`;
     Banesco and Mercantil share `api_instapago.validar_pago`, which takes the merchant's own
     receiving-bank code as a `receiptbank` argument (`RECEIPTBANK_IP` for Banesco,
     `RECEIPTBANK_MERCANTIL_IP` for Mercantil) since both go through the same Instapago account,
   - on success, looks up unpaid invoices via `api_mw.buscar_facturas`,
   - pays them via `api_mw.pagar_facturas`, distributing any overpayment onto the last invoice and
     tagging each MW payment with `idtransaccion = "<order>-<yyyymmddhhmmss>-<n>"` and a
     bank-specific `pasarela`: `"API-pm_vippo"` (Banco Plaza), `"API-pm_instapago_banesco"`,
     `"API-pm_instapago_mercantil"`.
   - These three route files duplicate the validate→search→pay sequence; when fixing a bug in one,
     check whether the same bug exists in the others. `tools/claude/nuevopm.md` documents the recipe
     that was followed to add Mercantil as a third bank — reuse/update it when adding another one.
5. **`pagomovil_bp/route_generarqr.py`** — separate JSON endpoint that generates an Instapago QR
   code for a given amount (used by the QR modal in the UI, currently wired up for Banesco only, via
   the flat `RECEIPTBANK_IP` env var rather than the per-bank `receiptbank` param above).

`src/utils/connect_api.py` (`conectar(headers, body, params, endpoint, metodo, cedula)`) is the
single HTTP wrapper used by every API integration; it logs request/response/exception at DEBUG and
returns a `(status, payload)` tuple where `status` is `"success"` / `"error"` / `"except"` — every
caller up the stack matches on this convention instead of raising, so preserve it when touching
these code paths.

### Partial-payment tolerance

`PORCENTAJE_DEUDA_MINIMA` (env var) lets a client pay slightly less than the full debt.
`api_mw.buscar_facturas` computes `deuda_minima = monto_deuda * (1 - PORCENTAJE_DEUDA_MINIMA/100)`;
payments between `deuda_minima` and the full debt are accepted, and `pagar_facturas` then adds the
shortfall/overage onto the last invoice's amount so MW's per-invoice bookkeeping still reconciles.

### Cached external data, refreshed out-of-band

BCV exchange rate (`src/utils/tasa_bcv.txt`) and the Vippo issuing-bank list
(`src/utils/lista_bancos.txt`) are **not** fetched live during a payment request — they're read from
these text files at runtime (`api_vippo.leer_tasa_bcv` / `leer_listabancos`) and only refreshed by
`src/crontab.py`, run out-of-process on a schedule (README suggests every 4h on weekdays via cron).
If either fetch/parse fails, `crontab.py` emails every address in `config.correos_tasa_bcv` via
`src/utils/enviar_correo.py`. If you change the format Vippo returns rates/banks in, update both the
parsing in `crontab.py` and the reading in `api_vippo.py` together.

### Logging

`src/utils/logger.py` configures a single root file handler writing to
`<PATH_BASE><LOG_FILE><NOMBRE_PROYECTO>_<ddmmyyyy>.log` (level from `LOG_LEVEL`); `werkzeug` and
`urllib3` loggers are forced to `CRITICAL` to keep the log focused on app-level messages. Almost
every log line is prefixed `USER: <cedula> - ...` by convention — keep that prefix when adding log
statements so logs stay greppable per client.
