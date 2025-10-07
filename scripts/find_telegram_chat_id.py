#!/usr/bin/env python3
"""
Telegram Chat ID Bulucu
HTTP API token'i ile chat ID'nizi otomatik bulur
"""

import requests
import sys

def find_chat_id(token):
    """Token ile chat ID bul"""
    print("🔍 Telegram Chat ID aranıyor...\n")
    
    # getUpdates API'si
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if not data.get("ok"):
            print(f"❌ Hata: {data.get('description', 'Bilinmeyen hata')}")
            print("\n💡 Token'i kontrol edin!")
            return None
        
        results = data.get("result", [])
        
        if not results:
            print("⚠️  Henüz mesaj bulunamadı!")
            print("\n📱 ŞİMDİ YAPMANIZ GEREKEN:")
            print("   1. Telegram'da bot'unuza gidin")
            print("   2. /start yazın")
            print("   3. Bu scripti tekrar çalıştırın\n")
            return None
        
        # Son mesajdan chat ID al
        last_message = results[-1]
        chat = last_message.get("message", {}).get("chat", {})
        chat_id = chat.get("id")
        first_name = chat.get("first_name", "")
        username = chat.get("username", "")
        
        if chat_id:
            print("✅ CHAT ID BULUNDU!\n")
            print("=" * 50)
            print(f"📍 Chat ID: {chat_id}")
            print(f"👤 İsim: {first_name}")
            if username:
                print(f"🔗 Kullanıcı Adı: @{username}")
            print("=" * 50)
            print(f"\n📋 .env dosyasına ekleyin:")
            print(f"   TELEGRAM_CHAT_ID={chat_id}\n")
            return chat_id
        else:
            print("❌ Chat ID bulunamadı!")
            return None
            
    except requests.exceptions.Timeout:
        print("❌ Zaman aşımı! İnternet bağlantınızı kontrol edin.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Bağlantı hatası: {e}")
        return None
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
        return None


def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║           📱 TELEGRAM CHAT ID BULUCU                        ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    # Token iste
    print("🤖 Telegram HTTP API Token'inizi girin:")
    print("   (Örnek: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz)\n")
    
    token = input("Token: ").strip()
    
    if not token:
        print("❌ Token boş olamaz!")
        sys.exit(1)
    
    print()
    chat_id = find_chat_id(token)
    
    if chat_id:
        print("🎉 Başarılı! Şimdi .env dosyasını güncelleyebilirsiniz.")
    else:
        print("\n💡 İpucu:")
        print("   - Token doğru mu?")
        print("   - Bot'a mesaj gönderiyor musunuz?")


if __name__ == "__main__":
    main()
