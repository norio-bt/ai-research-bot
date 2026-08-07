import os
import datetime
import requests

def generate_research_data():
    print("AIによる自動リサーチを開始します...")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise Exception("GEMINI_API_KEYが設定されていません。")
    
    model_name = "gemini-3.1-flash-lite"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
    
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": "最近のトレンドについて、簡潔にまとめてください。"}
                ]
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    
    res_data = response.json()
    if "candidates" in res_data and len(res_data["candidates"]) > 0:
        return res_data["candidates"][0]["content"]["parts"][0]["text"].strip()
    else:
        raise Exception("AIから有効な応答が得られませんでした。")

if __name__ == "__main__":
    try:
        report_content = generate_research_data()
        
        os.makedirs("outputs", exist_ok=True)
        
        today = datetime.date.today().isoformat()
        filename = f"outputs/research_report_{today}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report_content)
            
        print(f"レポートを保存しました: {filename}")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        exit(1)