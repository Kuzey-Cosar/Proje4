from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

def verileri_hazirla():
    klasor_yolu = os.path.dirname(os.path.abspath(__file__))
    dosya_yolu = os.path.join(klasor_yolu, "logs.json")
    
    with open(dosya_yolu, "r", encoding="utf-8") as f:
        ham_veri = json.load(f)

    islenmis_ucuslar = {}

    for zaman_kaydi in ham_veri:
        if "konumBilgileri" in zaman_kaydi:
            for iha in zaman_kaydi["konumBilgileri"]:
                takim_no = str(iha["takim_numarasi"])
                
                if takim_no not in islenmis_ucuslar:
                    islenmis_ucuslar[takim_no] = {
                        "id": takim_no,
                        "pilot": f"Takım {takim_no}", 
                        "rota": []
                    }
                
                nokta = {
                    "x": iha["iha_enlem"],
                    "y": iha["iha_boylam"],
                    "z": iha["iha_irtifa"]
                }
                islenmis_ucuslar[takim_no]["rota"].append(nokta)
    
    return list(islenmis_ucuslar.values())

TUM_UCUSLAR = verileri_hazirla()
print(f"Veriler işlendi! Toplam {len(TUM_UCUSLAR)} farklı takım/İHA bulundu.")

@app.route('/ucus-sorgula', methods=['GET'])

def ucus_getir():
    istenen_id = request.args.get('id')

    if not istenen_id:
        return jsonify({"mesaj": "Lütfen bir Takım ID (Örn: 1) gönderin!"}), 400

    bulunan_ucus = None
    for ucus in TUM_UCUSLAR:
        if ucus["id"] == istenen_id:
            bulunan_ucus = ucus
            break

    if bulunan_ucus:
        return jsonify(bulunan_ucus) 
    else:
        return jsonify({"mesaj": "Bu numaralı takım bulunamadı!"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)