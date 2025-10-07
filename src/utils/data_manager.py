"""
Veri Yönetim Modülü
Coin verilerini kaydet, yükle ve yönet
"""

import os
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
from loguru import logger


class DataManager:
    """Veri kaydetme ve yükleme yöneticisi"""
    
    def __init__(self, data_dir: str = "data"):
        """
        Veri yöneticisi başlat
        
        Args:
            data_dir: Veri klasörü yolu
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        logger.info(f"Veri klasörü: {self.data_dir.absolute()}")
    
    def save_coins(self, coins: list, filename: str = None) -> str:
        """
        Coin verilerini kaydet
        
        Args:
            coins: Coin verileri listesi
            filename: Dosya adı (None ise otomatik oluşturulur)
            
        Returns:
            Kaydedilen dosya yolu
        """
        if not coins:
            logger.warning("Kaydedilecek veri yok")
            return None
        
        # Dosya adı oluştur
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"coins_{timestamp}.json"
        
        filepath = self.data_dir / filename
        
        # JSON olarak kaydet
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "count": len(coins),
                "coins": coins
            }, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 {len(coins)} coin verisi kaydedildi: {filepath}")
        return str(filepath)
    
    def save_signals(self, signals: list, filename: str = None) -> str:
        """
        Analiz sinyallerini kaydet
        
        Args:
            signals: Sinyal listesi
            filename: Dosya adı
            
        Returns:
            Kaydedilen dosya yolu
        """
        if not signals:
            logger.warning("Kaydedilecek sinyal yok")
            return None
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"signals_{timestamp}.json"
        
        filepath = self.data_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "count": len(signals),
                "signals": signals
            }, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 {len(signals)} sinyal kaydedildi: {filepath}")
        return str(filepath)
    
    def load_latest_coins(self) -> list:
        """
        En son kaydedilen coin verilerini yükle
        
        Returns:
            Coin verileri listesi
        """
        coin_files = sorted(self.data_dir.glob("coins_*.json"), reverse=True)
        
        if not coin_files:
            logger.warning("Kaydedilmiş veri bulunamadı")
            return []
        
        latest_file = coin_files[0]
        
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger.info(f"📂 {len(data['coins'])} coin verisi yüklendi: {latest_file.name}")
        return data['coins']
    
    def to_dataframe(self, coins: list) -> pd.DataFrame:
        """
        Coin verilerini pandas DataFrame'e çevir
        
        Args:
            coins: Coin verileri
            
        Returns:
            DataFrame
        """
        if not coins:
            return pd.DataFrame()
        
        # Temel alanları seç
        df = pd.DataFrame([{
            'symbol': c.get('symbol'),
            'price': c.get('price'),
            'volume': c.get('volume'),
            'change_24h': c.get('change_24h'),
            'rsi': c.get('rsi'),
            'recommendation': c.get('recommendation')
        } for c in coins])
        
        return df
    
    def export_to_csv(self, coins: list, filename: str = None) -> str:
        """
        Verileri CSV olarak dışa aktar
        
        Args:
            coins: Coin verileri
            filename: Dosya adı
            
        Returns:
            CSV dosya yolu
        """
        df = self.to_dataframe(coins)
        
        if df.empty:
            logger.warning("Dışa aktarılacak veri yok")
            return None
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"coins_{timestamp}.csv"
        
        filepath = self.data_dir / filename
        df.to_csv(filepath, index=False, encoding='utf-8')
        
        logger.info(f"💾 CSV dışa aktarıldı: {filepath}")
        return str(filepath)
