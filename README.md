# `faster-whisper-xxl` için Toplu Transkripsiyon Arayüzü 

Bu Python script'i, [Purfview/whisper-standalone-win](https://github.com/Purfview/whisper-standalone-win) projesindeki güçlü `faster-whisper-xxl.exe` aracı için kullanıcı dostu bir komut satırı arayüzü (CLI) sağlar. Amacı, `faster-whisper-xxl`'nin sunduğu birçok ayarı interaktif olarak yönetmeyi kolaylaştırmak, toplu işlem yetenekleri sunmak ve çıktı dosyaları üzerinde ek işlemler (zaman damgası temizleme ve paragraf birleştirme gibi) yapmaktır.

## ✨ Özellikler

*   **İnteraktif Komut Satırı Arayüzü:** Ayarları kolayca seçmek için adım adım yönlendirme.
*   **Model Seçimi:** Kullanılabilir Whisper/Faster-Whisper modelleri arasından seçim yapma (`tiny`, `base`, `small`, `medium`, `large-v2`, `large-v3`, `large-v3-turbo`).
*   **Dil Seçimi:** Transkripsiyon dilini belirtme veya otomatik algılamaya bırakma.
*   **Toplu İşlem:**
    *   Tek bir medya dosyası işleme.
    *   Birden fazla medya dosyasını (boşlukla ayırarak) işleme.
    *   Bir klasördeki tüm desteklenen medya dosyalarını işleme.
    *   Komut satırı argümanları ile dosya/klasör/uzantı (`*.mp4` gibi) belirtme.
*   **Çıktı Formatı Seçimi:** Zaman damgası istendiğinde `srt`, `vtt`, `txt`, `json`, `lrc`, `tsv` veya `all` formatlarından bir veya birkaçını seçme.
*   **Zaman Damgası Yönetimi:**
    *   Çıktıda zaman damgalarının görünmesini isteme (SRT, VTT vb. için).
    *   Çıktıda zaman damgalarının görünmesini **istememe**: Bu durumda çıktı otomatik olarak `.txt` olur ve transkripsiyon sonrası `.txt` dosyasındaki `[MM:SS.mmm --> MM:SS.mmm]` formatındaki **zaman damgaları temizlenir** ve **tüm satırlar tek bir paragrafa birleştirilir.**
*   **Satır Formatlama:** Zaman damgalı çıktılar için satır bölme stillerini (`--sentence`, `--standard`, `--standard_asia`) seçme.
*   **Ekstra Özellikler:**
    *   Konuşmacı Ayrıştırma (Diarization - pyannote) seçeneği.
    *   Vokal Ayıklama (MDX Kim v2 modeli) seçeneği.
*   **Ayarları Kaydetme/Yükleme:** Sık kullandığınız ayarları otomatik olarak `config.json` dosyasına kaydeder ve bir sonraki çalıştırmada bu ayarları kullanmayı teklif eder.

## ⚙️ Gereksinimler

1.  **`faster-whisper-xxl.exe`:** Bu script, `faster-whisper-xxl.exe` programının ve onun bağımlılıklarının (`_models` klasörü vb.) sisteminizde **bu script ile aynı dizinde** bulunmasını bekler. Buradan indirebilirsiniz: [Purfview/whisper-standalone-win Releases](https://github.com/Purfview/whisper-standalone-win/releases)
2.  **Python 3.x:** Sisteminizde Python 3'ün yüklü olması ve komut satırından `python` komutuyla erişilebilir olması gerekir (PATH ortam değişkenine eklenmiş olmalıdır). Python'u [python.org](https://www.python.org/downloads/) adresinden indirebilirsiniz.

## 🚀 Kurulum ve Kullanım

1.  **İndirme:** Bu Python script dosyasını (`command-ui.py` veya verdiğiniz isimle) indirin.
2.  **Yerleştirme:** Script dosyasını, `faster-whisper-xxl.exe`'nin bulunduğu klasörün içine kopyalayın.
3.  **Çalıştırma:**
    *   Komut istemcisini (CMD veya PowerShell) açın.
    *   `cd` komutu ile script'in ve `faster-whisper-xxl.exe`'nin bulunduğu dizine gidin.
        ```bash
        cd /d "C:\path\to\your\faster-whisper-folder"
        ```
    *   Script'i Python ile çalıştırın:
        ```bash
        python command-ui.py
        ```
    *   **Dosya/Klasör Belirtme:**
        *   Script'i argümansız çalıştırırsanız, sizden işlenecek klasörün veya dosya(lar)ın yolunu/uzantınızı girmenizi isteyecektir.
        *   Alternatif olarak, dosya/klasör/uzantı yollarını doğrudan komut satırı argümanı olarak verebilirsiniz:
            ```bash
            # Tek dosya
            python command-ui.py "C:\videos\my_video.mp4"

            # Bir klasördeki tüm desteklenen dosyalar
            python command-ui.py "C:\audio_files\"

            # Belirli bir uzantıya uyan dosyalar (örn: tüm mp3ler)
            python command-ui.py *.mp3

            # Birden fazla dosya/klasör (komut istemcisinin yorumlamasına bağlı olabilir)
            python command-ui.py "file1.wav" "C:\my_folder\" *.mkv 
            ```
    *   **Ayarları Takip Etme:** Script sizi ayarlar konusunda yönlendirecektir.

## 💾 Yapılandırma Dosyası (`config.json`)

*   Script, ilk başarılı çalıştırmadan sonra (veya siz isterseniz), seçtiğiniz ayarları (model, dil, format tercihleri vb.) script ile aynı dizinde bulunan `config.json` dosyasına kaydeder.
*   Script bir sonraki çalıştırılışında bu dosyayı bulursa, size bu kayıtlı ayarları kullanıp kullanmak istemediğinizi sorar.
    *   "Evet" derseniz, ayar sorma adımları atlanır ve kayıtlı ayarlarla işlem yapılır.
    *   "Hayır" derseniz, size tüm ayarları yeniden sorar ve isterseniz yeni ayarları kaydedebilirsiniz.
*   Bu dosyayı manuel olarak (dikkatlice) düzenleyebilirsiniz, ancak genellikle script'in sormasını beklemek daha güvenlidir.

## 📝 Notlar ve İpuçları

*   **Zaman Damgası Temizleme ve Paragraf:** "Çıktıda zaman damgaları görünsün mü?" sorusuna "Hayır" demek, çıktının sadece `.txt` olmasını sağlar ve işlem bittikten sonra bu `.txt` dosyasındaki `[MM:SS.mmm --> MM:SS.mmm]` etiketleri silinerek tüm metin tek bir paragrafa birleştirilir.
*   **Dosya Yolları:** Komut satırından veya interaktif olarak dosya/klasör yolu girerken, yolda boşluk varsa yolu çift tırnak (`"`) içine almanız önerilir.
*   **`-o source` Varsayımı:** Script, `faster-whisper-xxl.exe`'nin `-o source` argümanıyla çalıştığını varsayar (çıktılar orijinal dosyanın yanına kaydedilir). Zaman damgası temizleme işlemi de çıktı `.txt` dosyasını burada arar.
*   **Hata Yönetimi:** Script temel hata kontrolleri yapar (dosya bulunamadı vb.), ancak `faster-whisper-xxl.exe`'nin kendisinden kaynaklanan hatalar için programın kendi çıktılarını takip etmeniz gerekebilir.

## 🙏 Bağımlılıklar ve Teşekkür

*   Bu script, **`faster-whisper-xxl.exe`** üzerine kurulmuştur.
*   Orijinal `whisper-standalone-win` projesi ve geliştiricisi **Purfview**'e teşekkürler. [GitHub Deposu](https://github.com/Purfview/whisper-standalone-win)
