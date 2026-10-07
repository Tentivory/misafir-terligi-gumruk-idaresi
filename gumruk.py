#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Misafir Terliği Gümrük İdaresi.

Kapı eşiğinde beyan alır, risk skorlar, hat belirler.
Bağımlılık yok. Patates yok. Anlam isteğe bağlı.
"""

from __future__ import annotations

import argparse
import hashlib

DAMGA = (
    "Kayyum Grok | 07 Ekim 2026 | Tentivory mühür: terlik serbest, ciddiyet şartlı"
)


def risk_skoru(numara: int, renk: str, sahip: str) -> int:
    ham = f"{numara}|{renk.strip().lower()}|{sahip.strip().lower()}".encode("utf-8")
    ozet = hashlib.sha256(ham).hexdigest()
    return int(ozet[:4], 16) % 100


def hat_belirle(skor: int) -> tuple[str, str]:
    if skor < 20:
        return (
            "YEŞİL HAT",
            "Terlik masum. İçeri al, çay ikram et, numarasını sorma.",
        )
    if skor < 55:
        return (
            "SARI HAT",
            "Topuk aşınmış. Ek beyan: bu terlik ev terliği mi, rol mü yapıyor?",
        )
    if skor < 85:
        return (
            "KIRMIZI HAT",
            "Sol tek. Diğer yarı kayınvalide çayı süresince aranacak.",
        )
    return (
        "EL KONULDU",
        "Bu terlik misafir değil, evin gizli ortağı. Antrede gözaltı.",
    )


def muayene(sahip: str, numara: int, renk: str, cift: bool) -> str:
    skor = risk_skoru(numara, renk, sahip)
    notlar = []
    if not cift:
        skor = min(99, skor + 17)
        notlar.append("Tek terlik beyanı şüpheli. Risk +17.")
    else:
        notlar.append("Çift beyan edildi. Gümrük biraz yumuşadı, az yumuşadı.")
    if numara >= 45:
        notlar.append("Büyük numara: paspas iki kez selam durdu.")
    if numara <= 36:
        notlar.append("Küçük numara: terlik kaybolduğunu iddia edebilir, dinleme.")
    hat, metin = hat_belirle(skor)
    satirlar = [
        "MİSAFİR TERLİĞİ GÜMRÜK İDARESİ",
        "Eşik Memurluğu — vardiya: çay demlenene kadar",
        f"Beyan sahibi : {sahip}",
        f"Numara       : {numara}",
        f"Renk         : {renk}",
        f"Çift         : {'evet' if cift else 'hayır, ve bu sorun'}",
        f"Risk skoru   : {skor}/99",
        f"Hat          : {hat}",
        metin,
        *notlar,
        "---",
        DAMGA,
        "Ciddi değildir. Ciddiye alınırsa gümrük kapanır, çay açık kalır.",
    ]
    return "\n".join(satirlar)


def main() -> None:
    parser = argparse.ArgumentParser(description="Kapı eşiği terlik gümrüğü")
    parser.add_argument("--sahip", default="dayı", help="terliği getiren kişi")
    parser.add_argument("--numara", type=int, default=42, help="ayak numarası")
    parser.add_argument("--renk", default="lacivert", help="terlik rengi")
    parser.add_argument("--cift", action="store_true", help="çift beyan edildi")
    args = parser.parse_args()
    if args.numara < 20 or args.numara > 60:
        raise SystemExit("Bu numara terlik değil, söylenti. 20-60 arası beyan et.")
    print(muayene(args.sahip, args.numara, args.renk, args.cift))


if __name__ == "__main__":
    main()
