import os
import subprocess
import re
import sys
import glob # Dosya arama için
import json # Ayarları kaydetme/yükleme için

# --- Ayarlar ---
# Script'in bulunduğu dizin
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# faster-whisper-xxl.exe'nin yolu (script ile aynı dizinde olduğu varsayılıyor)
EXE_PATH = os.path.join(SCRIPT_DIR, "faster-whisper-xxl.exe")
# Yapılandırma dosyasının adı
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")
# Desteklenen dosya uzantıları (küçük harfle)
SUPPORTED_EXTENSIONS = ['.mp3', '.wav', '.flac', '.ogg', '.m4a', 
                        '.mp4', '.mkv', '.mov', '.avi', '.wmv', '.flv']

# --- Yardımcı Fonksiyonlar ---
def get_user_choice(prompt, options, default_key=None):
    """Kullanıcıdan seçenek listesinden bir girdi alır."""
    print(f"\n{prompt}")
    for key, value in options.items():
        print(f"{key}) {value}")
    default_text = f" (varsayılan: {default_key})" if default_key and default_key in options else ""
    while True:
        choice = input(f"Seçiminizi yapın{default_text}: ").strip().lower() # Küçük harfe çevir
        if not choice and default_key:
            return default_key
        if choice in options:
            return choice
        if not choice and not default_key:
            print("Lütfen bir seçim yapın.")
            continue
        print("Geçersiz seçim, lütfen listeden bir numara girin.")

def get_user_input(prompt, default_value=""):
    """Kullanıcıdan serbest metin girdisi alır."""
    default_text = f" (varsayılan: {default_value})" if default_value else ""
    choice = input(f"\n{prompt}{default_text}: ").strip()
    return choice if choice else default_value

def get_yes_no(prompt, default_yes=None):
    """Kullanıcıdan Evet/Hayır cevabı alır."""
    options = "[e/h]"
    if default_yes is True:
        options = "[E/h]"
    elif default_yes is False:
        options = "[e/H]"
        
    while True:
        choice = input(f"{prompt} {options}: ").strip().lower()
        if not choice:
            if default_yes is True: return True
            if default_yes is False: return False
        if choice == 'e': return True
        if choice == 'h': return False
        print("Lütfen 'e' (evet) veya 'h' (hayır) girin.")

def load_settings(filepath):
    """Yapılandırma dosyasından ayarları yükler."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        print(f"'{os.path.basename(filepath)}' dosyasından ayarlar yüklendi.")
        return settings
    except FileNotFoundError:
        # Bu bir hata değil, sadece dosya yok.
        return None
    except json.JSONDecodeError:
        print(f"UYARI: '{os.path.basename(filepath)}' dosyası bozuk veya geçersiz. Ayarlar yüklenemedi.")
        return None
    except Exception as e:
        print(f"Ayarlar yüklenirken bilinmeyen bir hata oluştu: {e}")
        return None

def save_settings(settings, filepath):
    """Ayarları yapılandırma dosyasına kaydeder."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4) 
        print(f"Ayarlar '{os.path.basename(filepath)}' dosyasına kaydedildi.")
        return True
    except Exception as e:
        print(f"Ayarlar kaydedilirken hata oluştu: {e}")
        return False

def clean_timestamps_and_paragraphize(filepath):
    """Dosyadan zaman damgalarını temizler ve paragrafa dönüştürür."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f: content = f.read()
        content_no_ts = re.sub(r"\[\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}\.\d{3}\]\s*", "", content)
        lines = content_no_ts.splitlines()
        paragraph_lines = [line.strip() for line in lines if line.strip()]
        final_paragraph = " ".join(paragraph_lines)
        with open(filepath, 'w', encoding='utf-8') as f: f.write(final_paragraph)
        return True
    except FileNotFoundError: return False
    except Exception: return False # Hata detayını loglamak daha iyi olurdu

def find_media_files(input_path):
    """Klasördeki veya verilen yoldaki medya dosyalarını bulur."""
    files_to_process = []
    input_path_cleaned = input_path.strip("\"'")
    if os.path.isdir(input_path_cleaned):
        # print(f"'{input_path_cleaned}' klasörü taranıyor...") # Çok fazla çıktı olmasın
        for filename in os.listdir(input_path_cleaned):
            filepath = os.path.join(input_path_cleaned, filename)
            if os.path.isfile(filepath):
                _, ext = os.path.splitext(filename)
                if ext.lower() in SUPPORTED_EXTENSIONS:
                    files_to_process.append(filepath)
    elif os.path.isfile(input_path_cleaned):
        _, ext = os.path.splitext(input_path_cleaned)
        if ext.lower() in SUPPORTED_EXTENSIONS:
            files_to_process.append(input_path_cleaned)
        else:
            print(f"UYARI: '{input_path_cleaned}' desteklenen bir medya dosyası değil.")
    else:
         # Wildcard (*) ile eşleşme dene
         try:
             # Önemli: glob yolu işletim sistemine göre / veya \ kullanmalı, os.path.normpath yardımcı olabilir.
             normalized_path = os.path.normpath(input_path) # Tırnakları glob öncesi temizlemek daha iyi olabilir
             found_glob_files = glob.glob(normalized_path.strip("\"'")) 
             if found_glob_files:
                 print(f"'{input_path}' ile eşleşenler bulundu:")
                 for glob_file in found_glob_files:
                     if os.path.isfile(glob_file):
                        _, ext = os.path.splitext(glob_file)
                        if ext.lower() in SUPPORTED_EXTENSIONS:
                             files_to_process.append(glob_file)
                     # glob klasör de bulabilir, şimdilik sadece dosyalara odaklanalım
             #else: # Eşleşme yoksa sessiz kalabiliriz
             #    print(f"UYARI: '{input_path}' ile eşleşme bulunamadı.")
         except Exception as e:
             print(f"'{input_path}' işlenirken hata (glob): {e}")

    return files_to_process


# --- Ana Fonksiyon ---
def main():
    print("=" * 50)
    print("      Akıllı Toplu Transkripsiyon Arayüzü v2")
    print("=" * 50)

    if not os.path.exists(EXE_PATH):
        print(f"HATA: '{EXE_PATH}' bulunamadı.")
        input("Çıkmak için Enter'a basın...")
        return

    exe_directory = os.path.dirname(EXE_PATH) 
    files_to_process = []
    current_settings = {} # Ayarları tutacak sözlük
    loaded_settings = load_settings(CONFIG_FILE) # Başlangıçta ayarları yüklemeyi dene
    use_loaded_settings = False

    # Kayıtlı ayar varsa sor
    if loaded_settings:
        if get_yes_no("Önceki ayarlar bulundu. Bu ayarları kullanmak ister misiniz?", default_yes=True):
            current_settings = loaded_settings
            use_loaded_settings = True
            print("Önceki ayarlar kullanılıyor.")
        else:
            print("Yeni ayarlar girilecek.")
    
    # --- Dosya/Klasör Girişi ---
    # Komut satırı argümanlarını veya kullanıcı girdisini işle
    input_paths_or_patterns = []
    if len(sys.argv) > 1:
        input_paths_or_patterns = sys.argv[1:]
        print(f"Komut satırı girdileri: {', '.join(input_paths_or_patterns)}")
    else: 
        user_input = input("\nİşlenecek KLASÖRÜN yolunu veya DOSYA/DOSYA_DESENİ (örn: *.mp4) girin:\n").strip()
        if user_input:
            # Basit boşluk ayırma (tırnaklı yollar için ideal değil ama wildcard için ok)
            # Eğer kullanıcı tırnaklı tam yollar girdiyse önceki manuel parser daha iyiydi.
            # Şimdilik basit tutalım, kullanıcı wildcard veya tek klasör/dosya girsin.
            input_paths_or_patterns = [user_input] # Tek girdi olarak alalım
            # Eğer birden fazla dosya/klasör yolu desteği istenirse, önceki parser'a dönülebilir.
            

    if not input_paths_or_patterns:
        print("Girdi alınamadı. Çıkılıyor.")
        input("Çıkmak için Enter'a basın...")
        return

    # Dosyaları bul
    for pattern in input_paths_or_patterns:
         files_found = find_media_files(pattern)
         if files_found:
             files_to_process.extend(files_found)
         elif not os.path.isdir(pattern.strip("\"'")): # Klasör değilse ve find_media_files boş döndüyse uyarı ver
             print(f"UYARI: '{pattern}' için geçerli dosya bulunamadı veya eşleşmedi.")


    if not files_to_process:
        print("\nİşlenecek geçerli medya dosyası bulunamadı. Çıkılıyor.")
        input("Çıkmak için Enter'a basın...")
        return

    files_to_process = sorted(list(set(files_to_process))) # Tekrar edenleri kaldır ve sırala

    print("\n--- İşlenecek Dosyalar ---")
    for f in files_to_process: print(f"- {f}")
    print("--------------------------")
    
    if not get_yes_no(f"{len(files_to_process)} dosya işlenecek. Devam edilsin mi?", default_yes=True):
        print("İşlem iptal edildi.")
        input("Çıkmak için Enter'a basın...")
        return

    # --- Ayarları Al veya Yüklenenleri Kullan ---
    base_args = [] # Komut argümanları
    settings_to_save = {} # Kaydedilecek ayarlar

    if not use_loaded_settings:
        print("\n--- Yeni Ayarlar ---")
        # Model
        models = {"1": "tiny", "2": "base", "3": "small", "4": "medium", 
                  "5": "large-v2", "6": "large-v3", "7": "large-v3-turbo"}
        model_key = get_user_choice("Model Seçin:", models, "6")
        settings_to_save["model"] = models[model_key]
        
        # Dil
        lang = get_user_input("Dil kodu tr/en/ja yada Turkish/English/Japanese(dili algılaması için kodu girin yada otomatik tespit etmesi için boş bırakın)")
        settings_to_save["language"] = lang

        # Zaman Damgası
        ts_options = {"1": "Evet", "2": "Hayır"}
        ts_key = get_user_choice("Çıktıda zaman damgaları görünsün mü?", ts_options, "1")
        settings_to_save["want_visible_timestamps"] = (ts_key == "1")

        # Çıktı Formatı & Satır Stili
        if settings_to_save["want_visible_timestamps"]:
            fmts_opts = {"1": "srt", "2": "vtt", "3": "txt", "4": "json", "5": "lrc", "6": "tsv", "7": "all"}
            print("\nÇıktı Formatı/Formatları (numaraları boşlukla ayırın):")
            for k, v in fmts_opts.items(): print(f"{k}) {v}")
            fmt_keys = input("Seçim(ler) (varsayılan: 1): ").strip()
            if not fmt_keys: fmt_keys = "1"
            sel_fmts = [fmts_opts[k] for k in fmt_keys.split() if k in fmts_opts]
            settings_to_save["output_formats"] = sel_fmts if sel_fmts else ["srt"]
            
            styles = {"1": None, "2": "--sentence", "3": "--standard", "4": "--standard_asia"}
            style_key = get_user_choice("Satır Formatlama Stili:", {"1":"Varsayılan","2":"Cümle","3":"Standart","4":"Standart Asya"}, "3")
            settings_to_save["line_style"] = styles[style_key]
        else:
            settings_to_save["output_formats"] = ["txt"] # Otomatik txt
            settings_to_save["line_style"] = None # Satır stili yok

        # Diarization
        diar_opts = {"1": False, "2": True}
        diar_key = get_user_choice("Konuşmacı Ayrıştırma?", {"1":"Hayır","2":"Evet"}, "1")
        settings_to_save["diarization"] = diar_opts[diar_key]

        # Vokal Ayıklama
        voc_opts = {"1": False, "2": True}
        voc_key = get_user_choice("Vokal Ayıklama?", {"1":"Hayır","2":"Evet"}, "1")
        settings_to_save["vocal_extract"] = voc_opts[voc_key]
        
        current_settings = settings_to_save # Yeni girilen ayarları kullan
        
        # Yeni ayarları kaydetmeyi sor
        if get_yes_no("Bu yeni ayarlar kaydedilsin mi?", default_yes=True):
            save_settings(current_settings, CONFIG_FILE)

    # --- Ayarları `base_args` listesine dönüştür ---
    base_args.extend(["--model", current_settings.get("model", "large-v3")])
    if current_settings.get("language"):
        base_args.extend(["--language", current_settings["language"]])
    
    output_formats = current_settings.get("output_formats", ["srt"])
    base_args.extend(["--output_format", ' '.join(output_formats)])
    
    line_style = current_settings.get("line_style")
    if line_style: # Sadece None değilse ekle
        base_args.append(line_style)
        
    if current_settings.get("diarization"):
        base_args.extend(["--diarize", "pyannote_v3.1"])
    if current_settings.get("vocal_extract"):
        base_args.extend(["--ff_vocal_extract", "mdx_kim2"])

    # Sabit argümanlar
    base_args.extend(["--word_timestamps", "true", "-pp", "-o", "source", "--batch_recursive", "--check_files"])
    
    # Regex gerekip gerekmediğini belirle
    output_format_is_txt_and_no_ts = (not current_settings.get("want_visible_timestamps", True) and 
                                      "txt" in output_formats)

    # --- Dosyaları İşleme Döngüsü ---
    print("\n" + "="*20 + " İŞLEM BAŞLATILIYOR " + "="*20)
    total_files = len(files_to_process)
    processed_count = 0
    success_count = 0
    clean_success_count = 0
    error_count = 0

    for i, media_file_path in enumerate(files_to_process):
        processed_count += 1
        print(f"\n--- Dosya {processed_count}/{total_files}: {os.path.basename(media_file_path)} ---")
        
        final_command_list = [EXE_PATH, media_file_path] + base_args

        print("Çalıştırılan Komut:")
        cmd_parts = [f'"{p}"' if ' ' in p and not p.startswith('"') else p for p in final_command_list]
        print(' '.join(cmd_parts))
        
        return_code = -1
        try:
            process = subprocess.Popen(final_command_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                       universal_newlines=True, encoding='utf-8', errors='replace', bufsize=1,
                                       cwd=exe_directory, shell=False) 
            for line in process.stdout: print(line, end='') 
            process.wait() 
            return_code = process.returncode

            if return_code == 0:
                print("Transkripsiyon başarılı.")
                success_count += 1
                # Temizleme ve paragraf yapma
                if output_format_is_txt_and_no_ts:
                    media_base = os.path.splitext(os.path.basename(media_file_path))[0]
                    media_dir = os.path.dirname(media_file_path)
                    if not media_dir: media_dir = os.getcwd()
                    
                    txt_file = os.path.join(media_dir, f"{media_base}.txt")
                    txt_file_lang = os.path.join(media_dir, f"{media_base}.{current_settings.get('language', '')}.txt")
                    
                    file_to_clean = None
                    if os.path.exists(txt_file):
                        file_to_clean = txt_file
                    elif current_settings.get('language') and os.path.exists(txt_file_lang):
                         file_to_clean = txt_file_lang
                    
                    if file_to_clean:
                         print(f"'{os.path.basename(file_to_clean)}' temizleniyor...")
                         if clean_timestamps_and_paragraphize(file_to_clean):
                             print("Temizleme başarılı.")
                             clean_success_count += 1
                         else:
                             print("Temizleme sırasında hata oluştu.")
                             # Bunu genel hataya eklemeyebiliriz, transkripsiyon başarılıydı.
                    else:
                        print("UYARI: Çıktı .txt dosyası bulunamadı, temizleme atlandı.")
            else:
                print(f"HATA: Transkripsiyon başarısız (Hata Kodu: {return_code}).")
                error_count += 1

        except Exception as e:
            print(f"'{os.path.basename(media_file_path)}' işlenirken kritik hata: {e}")
            error_count += 1
            # Döngüye devam et veya çık? Şimdilik devam edelim.
            continue 

    # --- İşlem Sonu Özet ---
    print("\n" + "="*20 + " İŞLEM SONU " + "="*20)
    print(f"Toplam {total_files} dosya bulundu ve işlenmeye çalışıldı.")
    print(f"{success_count} transkripsiyon başarılı.")
    if output_format_is_txt_and_no_ts:
        print(f"{clean_success_count} dosya başarıyla temizlendi ve paragrafa dönüştürüldü.")
    if error_count > 0:
        print(f"{error_count} dosyada işlem sırasında hata oluştu.")
    print("="* (40 + len(" İŞLEM SONU ")))

    input("\nİşlem bitti. Çıkmak için Enter'a basın...")

if __name__ == "__main__":
    main()