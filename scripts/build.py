import pathlib

SRC_DIR = pathlib.Path("src")
DIST_DIR = pathlib.Path("dist")

def build():
    for target in ["shadowrocket", "passwall", "clash"]:
        (DIST_DIR / target).mkdir(parents=True, exist_ok=True)

    for src_file in sorted(SRC_DIR.glob("*.txt")):
        name = src_file.stem
        sr_lines = []
        pw_domains = []
        pw_ips = []
        clash_lines = ["payload:"]

        for raw in src_file.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue

            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 2:
                continue

            rule_type, value = parts[0].upper(), parts[1]

            # Shadowrocket & Clash
            sr_lines.append(f"{rule_type},{value}")
            clash_lines.append(f"  - {rule_type},{value}")

            # Passwall / Passwall2 (Xray / Sing-box shunt syntax)
            if rule_type == "DOMAIN-SUFFIX":
                pw_domains.append(f"domain:{value}")
            elif rule_type == "DOMAIN":
                pw_domains.append(f"full:{value}")
            elif rule_type == "DOMAIN-KEYWORD":
                pw_domains.append(f"keyword:{value}")
            elif rule_type in ("IP-CIDR", "IP-CIDR6"):
                pw_ips.append(value)

        (DIST_DIR / "shadowrocket" / f"{name}.list").write_text("\n".join(sr_lines) + "\n", encoding="utf-8")
        (DIST_DIR / "passwall" / f"{name}_domain.txt").write_text("\n".join(pw_domains) + "\n", encoding="utf-8")
        (DIST_DIR / "passwall" / f"{name}_ip.txt").write_text("\n".join(pw_ips) + "\n", encoding="utf-8")
        (DIST_DIR / "clash" / f"{name}.yaml").write_text("\n".join(clash_lines) + "\n", encoding="utf-8")

if __name__ == "__main__":
    build()
