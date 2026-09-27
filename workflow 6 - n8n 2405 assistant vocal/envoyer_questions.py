"""Envoie les questions vocales de questions/ à l'assistant, dans l'ordre (une conversation).

    python3 envoyer_questions.py            # les 10 questions
    python3 envoyer_questions.py --a 1      # test de fumée : la première seulement

Chaque réponse vocale (voix Gradium) est enregistrée dans out/reponses/ ; écoutez-la avec
`afplay out/reponses/r01.wav`. Adresse du webhook lue dans .env.n8n-voice (preparer_n8n.py).
"""
import argparse
import secrets
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent


def webhook():
    env = HERE / ".env.n8n-voice"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            if line.startswith("N8N_VOICE_WEBHOOK="):
                return line.split("=", 1)[1]
    return None


def multipart(field, filename, data, content_type="audio/wav"):
    boundary = "----deadweight" + secrets.token_hex(8)
    body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{field}\"; filename=\"{filename}\"\r\n"
            f"Content-Type: {content_type}\r\n\r\n").encode() + data + f"\r\n--{boundary}--\r\n".encode()
    return body, f"multipart/form-data; boundary={boundary}"


def main():
    ap = argparse.ArgumentParser(description="Envoie les questions vocales à l'assistant n8n")
    ap.add_argument("--de", type=int, default=1)
    ap.add_argument("--a", type=int, default=10)
    ap.add_argument("--url", default=webhook())
    args = ap.parse_args()
    if not args.url:
        sys.exit("adresse du webhook inconnue : lancez preparer_n8n.py, ou passez --url")
    texts = (HERE / "questions" / "questions.txt").read_text(encoding="utf-8").splitlines()
    out = HERE / "out" / "reponses"
    out.mkdir(parents=True, exist_ok=True)
    for i in range(args.de, args.a + 1):
        audio = (HERE / "questions" / f"q{i:02d}.wav").read_bytes()
        body, ctype = multipart("voice_message", f"q{i:02d}.wav", audio)
        req = urllib.request.Request(args.url, data=body, method="POST", headers={"Content-Type": ctype})
        t0 = time.time()
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                answer, kind = r.read(), r.headers.get("Content-Type", "")
            name = f"r{i:02d}.wav" if "audio" in kind or answer[:4] == b"RIFF" else f"r{i:02d}.txt"
            (out / name).write_bytes(answer)
            status = f"200  {len(answer) // 1024:4d} Ko  {kind[:20]:20}  → out/reponses/{name}"
        except urllib.error.HTTPError as e:
            status = f"{e.code}  {e.read().decode(errors='replace')[:150]}"
        except (urllib.error.URLError, TimeoutError) as e:
            status = f"échec : {e}"
        print(f"Q{i:02d}  {time.time() - t0:5.1f} s  {status}\n     « {texts[i - 1]} »", flush=True)


if __name__ == "__main__":
    main()
