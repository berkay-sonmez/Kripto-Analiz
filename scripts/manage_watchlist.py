"""
Watchlist Yönetici
İzleme listenize coin ekleme/çıkarma
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def show_current_watchlist():
    """Mevcut watchlist'i göster"""
    from src.config.my_watchlist import MY_WATCHLIST
    
    print("\n📋 Mevcut İzleme Listeniz:")
    print("-" * 50)
    for i, symbol in enumerate(MY_WATCHLIST, 1):
        print(f"{i:2}. {symbol}")
    print(f"\nToplam: {len(MY_WATCHLIST)} coin")


def add_coins():
    """Yeni coin ekle"""
    print("\n➕ Yeni Coin Ekleme")
    print("-" * 50)
    print("Eklemek istediğiniz coin sembollerini virgülle ayırarak girin:")
    print("Örnek: ATOM,NEAR,FTM")
    print("(İptal için boş bırakın)")
    
    coins_input = input("\nCoinler: ").strip().upper()
    
    if not coins_input:
        print("❌ İşlem iptal edildi.")
        return
    
    new_coins = [c.strip() for c in coins_input.split(",") if c.strip()]
    
    if not new_coins:
        print("❌ Geçerli coin girilmedi.")
        return
    
    # Watchlist dosyasını güncelle
    watchlist_file = Path("src/config/my_watchlist.py")
    
    with open(watchlist_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Listeyi bul ve güncelle
    from src.config.my_watchlist import MY_WATCHLIST
    
    added = []
    for coin in new_coins:
        if coin not in MY_WATCHLIST:
            MY_WATCHLIST.append(coin)
            added.append(coin)
    
    if added:
        # Dosyayı güncelle
        list_str = '[\n    # Major Coins\n'
        for i, coin in enumerate(MY_WATCHLIST):
            if i == 0 or (i > 0 and coin in ["BTC", "ETH", "BNB"]):
                list_str += f'    "{coin}",\n'
            else:
                list_str += f'    "{coin}",\n'
        list_str += ']'
        
        new_content = content.replace(
            content[content.find('MY_WATCHLIST = ['):content.find(']', content.find('MY_WATCHLIST = ['))+1],
            f'MY_WATCHLIST = {list_str}'
        )
        
        print(f"\n✅ {len(added)} coin eklendi: {', '.join(added)}")
        print("\n💡 Değişiklikler uygulandı!")
    else:
        print("\n⚠️  Tüm coinler zaten listede mevcut.")


def remove_coins():
    """Coin çıkar"""
    show_current_watchlist()
    
    print("\n➖ Coin Çıkarma")
    print("-" * 50)
    print("Çıkarmak istediğiniz coin sembollerini virgülle ayırarak girin:")
    print("Örnek: DOGE,SHIB")
    print("(İptal için boş bırakın)")
    
    coins_input = input("\nCoinler: ").strip().upper()
    
    if not coins_input:
        print("❌ İşlem iptal edildi.")
        return
    
    remove_list = [c.strip() for c in coins_input.split(",") if c.strip()]
    
    from src.config.my_watchlist import MY_WATCHLIST
    
    removed = []
    for coin in remove_list:
        if coin in MY_WATCHLIST:
            MY_WATCHLIST.remove(coin)
            removed.append(coin)
    
    if removed:
        print(f"\n✅ {len(removed)} coin çıkarıldı: {', '.join(removed)}")
        print("\n💡 Değişiklikler uygulandı!")
    else:
        print("\n⚠️  Belirtilen coinler listede bulunamadı.")


def main():
    """Ana menü"""
    while True:
        print("\n" + "=" * 50)
        print("📋 WATCHLIST YÖNETİCİSİ")
        print("=" * 50)
        print("\n1. Mevcut listeyi göster")
        print("2. Yeni coin ekle")
        print("3. Coin çıkar")
        print("4. Çıkış")
        
        choice = input("\nSeçiminiz (1-4): ").strip()
        
        if choice == "1":
            show_current_watchlist()
        elif choice == "2":
            add_coins()
        elif choice == "3":
            remove_coins()
        elif choice == "4":
            print("\n👋 Görüşmek üzere!")
            break
        else:
            print("\n❌ Geçersiz seçim!")
    
    print("\n💡 İpucu: Watchlist'inizi analiz etmek için:")
    print("   python scripts\\analyze_watchlist.py\n")


if __name__ == "__main__":
    main()
