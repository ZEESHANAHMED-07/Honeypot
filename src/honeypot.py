#!/usr/bin/env python3
import asyncio, json, logging, signal, sys, time
from logging.handlers import RotatingFileHandler

LOG_PATH = "logs/honeypot.jsonl"
SERVICES = {
    "ssh":    {"port": 2222, "banner": b"SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.7\r\n"},
    "telnet": {"port": 2323, "banner": b"login: "},
    "http":   {"port": 8081, "banner": b"HTTP/1.1 400 Bad Request\r\nServer: nginx\r\nContent-Length: 0\r\n\r\n"},
}
READ_LIMIT = 2048        # read up to 2 KB per connection
IDLE_TIMEOUT = 10        # seconds

# ----- logging setup -----
logger = logging.getLogger("honeypot")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(LOG_PATH, maxBytes=5_000_000, backupCount=5)
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def log_event(event: dict):
    event.setdefault("ts", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    logger.info(json.dumps(event, ensure_ascii=False))
    print("LOG EVENT:", event)  # <-- debug print so you see it live

# create log file immediately & write startup marker
open(LOG_PATH, "a").close()
log_event({"event": "init", "msg": "honeypot starting"})

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, service_name: str):
    peer_ip, peer_port, *_ = writer.get_extra_info("peername") or ("?", 0)
    try:
        # Send a fake banner to look legit
        writer.write(SERVICES[service_name]["banner"])
        await writer.drain()

        # Read a bit of data with timeout
        try:
            data = await asyncio.wait_for(reader.read(READ_LIMIT), timeout=IDLE_TIMEOUT)
        except asyncio.TimeoutError:
            data = b""

        # Store an event per connection
        log_event({
            "event": "connection",
            "service": service_name,
            "dst_port": SERVICES[service_name]["port"],
            "src_ip": peer_ip,
            "src_port": peer_port,
            "bytes_rx": len(data),
            "preview": data[:128].decode(errors="replace")
        })
    except Exception as e:
        log_event({"event": "error", "service": service_name, "err": repr(e)})
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass

async def main():
    servers = []
    for name, cfg in SERVICES.items():
        server = await asyncio.start_server(
            lambda r, w, n=name: handle_client(r, w, n),
            host="0.0.0.0",
            port=cfg["port"],
            reuse_port=True,
        )
        log_event({"event": "start", "service": name, "port": cfg["port"]})
        servers.append(server)

    # graceful shutdown
    stop = asyncio.Event()
    for sig in (signal.SIGINT, signal.SIGTERM):
        asyncio.get_running_loop().add_signal_handler(sig, stop.set)

    # serve forever until a stop signal
    await stop.wait()
    for srv in servers:
        srv.close()
        await srv.wait_closed()
    log_event({"event": "stop"})

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
