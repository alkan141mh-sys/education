# Öğrenme zemini (Education)

Yapay zekâ destekli, açık kaynak bir öğrenme zemini. Bugünkü çekirdek: `personal-educator` skill'i (v2, 24 Kasım 2026 pilotu) ve kuralları zorlayan araçlar (`edu_tools.py`). Uzun vadeli hedef ve aşamalar: `docs/vizyon-notu.md`.

Bu proje **öğrenme yöntemini** geliştirmek içindir; konu öğretimi (devre, moleküler haberleşme…) başka projelerde yapılır.

## Çalışma kuralları
- **Önce tasarım.** Kod yazmadan önce düz metin, derinlemesine bir tasarım yazılır ve Muhammet onaylar. Yolda tasarlamak ölçek ve verim sorunu çıkarıyor.
- **Kural değişiklikleri kanıta dayanır.** Her yeni ya da değişen kural için şunlar yazılır: hangi oturumda, hangi yanlış anlamadan çıktığı.
- **Skill değişikliklerine Muhammet karar verir.** `skill/SKILL.md` için önce değişikliği gerekçesiyle öner, onay gelmeden uygulama.
- Kodu Claude yazar; Muhammet fikir, tasarım, veri ve testten sorumludur. Açıklamaları sade Türkçe yaz; kod ve kod yorumları İngilizce kalır.
- `tests.json` elle etiketlendi. Bir testi geçirmek için beklenen sonucu değiştirme; beklenti yanlışsa bunu söyle ve sor.

## Dosyalar
| Dosya | Ne |
|---|---|
| `edu_tools.py` | Deterministik yardımcılar: `calc`, `names`, `gate`, `transition`, `svglint`, `maplint`, `metrics`, `due`/`review`, `planmap`, `selftest` |
| `names.json` | İsim kaydı (devre konusunun etiketleri ve anlamları) |
| `map-region1.json` | Müfredat haritası, Bölge 1 (besleme yolu) |
| `planmap-region1.json` | Bölge 1'in plan haritası tanımı (`planmap` için) |
| `tests.json` | Elle etiketlenmiş test seti (`selftest`) |
| `fonts/` | Inter (panonun yazı tipi; `svglint` yazı genişliğini bununla ölçer, OFL lisansı) |
| `skill/SKILL.md` | personal-educator v2'nin claude.ai'deki hâlinin kopyası (24 Kasım) |
| `docs/vizyon-notu.md` | Vizyon notu (Word dosyasının metne çevrilmiş hâli; asıl dosya klasörün kökünde) |
| `docs/eklenti-taramasi.md` | Claude ve ChatGPT eklenti/skill taraması (27 Kasım): aday kurallar, kayıt şeması önerisi, lisans notları |

## Komutlar
```
python edu_tools.py selftest      # edu_tools.py veya names.json her değiştiğinde çalıştır; 43/43 ve "font": "Inter" beklenir
python edu_tools.py calc "div(2.495, 10e3, 15e3)"
python edu_tools.py maplint map-region1.json --model <öğrenci-modeli>.json
```
Windows'ta Türkçe karakterler ve Ω için `PYTHONUTF8=1` gerekir; `.claude/settings.json` bunu ayarlıyor. Bağımlılık: `pip install -r requirements.txt` (yalnızca Pillow).

## Bilinmesi gerekenler
- `skill/SKILL.md` claude.ai'ye bağlı: proje belgelerini `project_read`/`project_write` ile, öğrenci modelini ve panoyu artifact veritabanından (`db_get`, `db_write`) okuyor. Claude Code'da bunların karşılığı henüz tasarlanmadı. Bu yüzden skill şimdilik `.claude/skills/` altında değil, yalnızca kaynak olarak duruyor.
- Belgelerde geçen `claude/...` yolları claude.ai'deki "education" projesinin belgeleridir (öğrenme tasarımı, yanlış anlama kaydı, aşama belgeleri). Bu klasörde değiller.
- Öğrenci modeli, oturum kayıtları ve yanlış anlama kayıtları gerçek öğrenci verisidir. Gizlilik kararı verilene kadar git'e girmezler (`.gitignore`).
- Git deposu 24 Kasım 2026'da başlatıldı (`main` dalı). Uzak depo: `origin` → github.com/alkan141mh-sys/education (herkese açık, MIT lisansı). Commit'ler GitHub'ın noreply e-postasıyla atılır. `.claude/settings.json` depoda; kişisel ayarlar `.claude/settings.local.json` dosyasına gider ve git'e girmez.
