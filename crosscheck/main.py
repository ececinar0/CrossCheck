import re

def clean_text(text):
    # Temizlenecek kalıplar (RegEx)
    patterns = [
        r"Ara", r"Search", r"Followers", r"People", r"Hashtags",
        r"Takip Ettikleri", r"Kişiler", r"Konu Etiketleri", r"Takipçiler", r"Following",
        r"'in profil resmi", r"'s profile picture"
    ]
    for pattern in patterns:
        text = re.compile(pattern, re.IGNORECASE).sub("", text)
    return text.strip().lower()

def process_file_to_sets(file_path):
    """
    Dosyayı okur, temizler ve benzersiz satırlardan/ifadelerden oluşan
    orijinal hali ile temizlenmiş halini haritalayan bir sözlük ve küme döner.
    """
    unique_lines = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                raw_line = line.strip()
                if not raw_line:
                    continue
                
                cleaned = clean_text(raw_line)
                if cleaned:  # Eğer temizlendikten sonra boş kalmadıysa
                    # Temizlenmiş hali key, orijinal hali value olacak şekilde tutuyoruz
                    unique_lines[cleaned] = raw_line
    except FileNotFoundError:
        print(f"Hata: {file_path} dosyası bulunamadı.")
        
    return unique_lines

def compare_files(old_path, new_path):
    # İki dosyayı da işle ve temizlenmiş verileri küme (set) mantığına hazırla
    old_data = process_file_to_sets(old_path)
    new_data = process_file_to_sets(new_path)

    old_cleaned_set = set(old_data.keys())
    new_cleaned_set = set(new_data.keys())

    # 1. NEW dosyasında olup OLD dosyasında OLMAYANLAR (Yeni eklenenler/Farklı olanlar)
    only_in_new = new_cleaned_set - old_cleaned_set
    
    # 2. OLD dosyasında olup NEW dosyasında OLMAYANLAR (Kaldırılanlar/Farklı olanlar)
    only_in_old = old_cleaned_set - new_cleaned_set

    print("=== KARŞILAŞTIRMA SONUÇLARI ===\n")

    # Sadece NEW dosyasında olanları yazdır
    if only_in_new:
        print(f"[{new_path}] DOSYASINDA OLUP [{old_path}] DOSYASINDA OLMAYANLAR (YENİ/FARKLI):")
        for item in only_in_new:
            print(f" -> {new_data[item]}")
    else:
        print(f"[{new_path}] dosyasına eklenen farklı bir veri bulunamadı.")

    print("\n" + "-"*40 + "\n")

    # Sadece OLD dosyasında olanları yazdır
    if only_in_old:
        print(f"[{old_path}] DOSYASINDA OLUP [{new_path}] DOSYASINDA OLMAYANLAR (SİLİNMİŞ/ESKİ):")
        for item in only_in_old:
            print(f" -> {old_data[item]}")
    else:
        print(f"[{old_path}] dosyasından silinen/farklı olan bir veri bulunamadı.")

# Dosya yollarını tanımlayın
old_file = 'old'
new_file = 'new'

# Karşılaştırmayı başlat
compare_files(old_file, new_file)