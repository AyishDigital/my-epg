from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

# Senarai semua saluran & jadual ulangan (6 jam setiap slot)
senarai_saluran = [
    {
        "channel_id": "mekkah",
        "channel_name": "LIVE MAKKAH",
        "slots": [
            {"start_hour": 0, "end_hour": 6, "title": "Siaran Langsung Makkah (Sesi 1)"},
            {"start_hour": 6, "end_hour": 12, "title": "Siaran Langsung Makkah (Sesi 2)"},
            {"start_hour": 12, "end_hour": 18, "title": "Siaran Langsung Makkah (Sesi 3)"},
            {"start_hour": 18, "end_hour": 24, "title": "Siaran Langsung Makkah (Sesi 4)"}
        ]
    },
    {
        "channel_id": "alquran",
        "channel_name": "Al-Quran Live",
        "slots": [
            {"start_hour": 0, "end_hour": 6, "title": "Al-Quran Live (Sesi 1)"},
            {"start_hour": 6, "end_hour": 12, "title": "Al-Quran Live (Sesi 2)"},
            {"start_hour": 12, "end_hour": 18, "title": "Al-Quran Live (Sesi 3)"},
            {"start_hour": 18, "end_hour": 24, "title": "Al-Quran Live (Sesi 4)"}
        ]
    }
]

tv = ET.Element("tv")

jumlah_hari = 3
tarikh_semasa = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

for saluran in senarai_saluran:
    channel_id = saluran["channel_id"]
    channel_name = saluran["channel_name"]
    slot_rancangan = saluran["slots"]

    # Daftar elemen <channel>
    channel = ET.SubElement(tv, "channel", id=channel_id)
    display_name = ET.SubElement(channel, "display-name", lang="ms")
    display_name.text = channel_name

    # Jana jadual berulang untuk beberapa hari
    for hari in range(jumlah_hari):
        tarikh_tapak = tarikh_semasa + timedelta(days=hari)

        for slot in slot_rancangan:
            waktu_mula = tarikh_tapak + timedelta(hours=slot["start_hour"])

            if slot["end_hour"] == 24:
                waktu_tamat = tarikh_tapak + timedelta(days=1, hours=0)
            else:
                waktu_tamat = tarikh_tapak + timedelta(hours=slot["end_hour"])

            start_str = waktu_mula.strftime("%Y%m%d%H%M%S") + " +0800"
            stop_str = waktu_tamat.strftime("%Y%m%d%H%M%S") + " +0800"

            programme = ET.SubElement(
                tv,
                "programme",
                start=start_str,
                stop=stop_str,
                channel=channel_id
            )
            title = ET.SubElement(programme, "title", lang="ms")
            title.text = slot["title"]

tree = ET.ElementTree(tv)
tree.write("epg.xml", encoding="utf-8", xml_declaration=True)
print("Fail epg.xml berjaya dijana untuk semua saluran!")
