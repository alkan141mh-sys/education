# Eklenti ve skill taraması: Claude ve ChatGPT

27 Kasım 2026 · personal-educator v2 ile karşılaştırma

## Neden bu not

Vizyon notunun iki açık sorusuna malzeme toplamak için yazıldı:

- **Özgün katkı:** Var olan yapay zekâ öğretmenlerinden farkımız ne?
- **Araştırma ayağı (Aşama 3):** Hangi yöntem hangi kurala karşılık geliyor?

Bu not bir **aday listesi**, karar değil. Buradaki hiçbir şey skill'e kendiliğinden girmez. Bir aday kural, ancak bir oturumda onu gerektiren bir yanlış anlama görülürse, kanıtıyla birlikte önerilir (CLAUDE.md: "kural değişiklikleri kanıta dayanır").

## Nasıl tarandı

- **Claude:** claude.ai plugin kataloğunda öğretmenlik, öğrenme, aralıklı tekrar, quiz, devre, Verilog, diyagram ve literatür anahtar kelimeleriyle arama yapıldı. Kurulu plugin yoktu; etkin skill'ler listelendi.
- **ChatGPT:** GPT Store'a ve ChatGPT uygulama dizinine doğrudan erişim yok. Web araması yapıldı ve OpenAI'nin açık plugin deposu (`openai/plugins`) incelendi.
- Öne çıkan kaynakların asıl dosyaları okundu: Education Skills Library'nin README'si ve öğrenciye yönelik 5 skill'i, engram'ın prior-art belgesi, Study Mode'un sistem komutu.
- Hiçbir şey kurulmadı.

## Bulgular

### 1. Claude Education Skills Library (en değerli kaynak)

Gareth Manning'in açık kaynak kütüphanesi. 20 alanda 165 skill var; her skill isimli araştırmalara dayanıyor ve kanıt gücü notlanmış. Claude Code, claude.ai ve Codex'te çalışıyor. Lisansı **CC BY-SA 4.0**.

Bizi ilgilendiren iki alan:

- **20. alan, öğrenciye yönelik 13 skill:** dersin içinde canlı çalışıyorlar, kurallarımızla birebir karşılaştırılabiliyorlar (aşağıdaki tablo).
- **12. alan, yapay zekâ ve öğrenme bilimi, 14 skill:** yanlış çözülmüş örnek (erroneous example), çözümlü örneği adım adım geri çekme (worked example fading), kişiye göre aralık algoritması, öğrenme analitiği yorumu, bilişsel tutor mimarisi.

Diğer alanlardan işe yarayabilecekler:

- **cognitive-load-analyser:** harita kuralımızı (ünite başına en fazla 1 kavram, 3 isim) sınamak için.
- **dual-coding-designer:** çizim kurallarımız için.
- **hinge-question-designer:** ünitenin anahtar tahmin sorusu için.
- **learning-progression-builder** ve **curriculum-knowledge-architecture-designer:** harita kurarken.

**Skill'lerden daha değerli iki şey:**

- **`evidence_captured` şeması.** Her skill, bir etkileşimden kayda ne yazılacağını alan alan tanımlıyor:
  - hangi bilişsel kapı çalıştı,
  - öncesi ve sonrası güven,
  - ulaşılan ipucu basamağı,
  - hata türü,
  - yardımlı mı yardımsız mı,
  - aktarma kontrolü,
  - yardımsız takip yapıldı mı.

  Bu, ölçek tartışmasında (25 Kasım) önerdiğimiz ortak kayıt biçiminin hazır bir taslağı (aşağıda "Kayıt şeması" bölümü).
- **EXCLUSIONS.md.** Kanıtı zayıf olduğu için bilerek dışarıda bırakılan yöntemlerin listesi ve gerekçeleri (örneğin öğrenme stilleri). Aşama 3'teki literatür taramasında eleme listesi olarak kullanılabilir.

**Sınırları:**

- Komutların kendisi yapay zekâ müdahalesi olarak deneysel olarak doğrulanmamış; bunu yazarlar da söylüyor. Kanıt yöntem için var, bu komutlar için değil.
- Çoğu skill okul öğretmenine yönelik (K-12).
- Lisans "aynı lisansla paylaş" şartı taşıyor (aşağıda "Lisans" bölümü).

### 2. engram (en yakın rakip)

Bir Claude Code plugin'i; katalogda değil, web aramasında bulundu. İçinde şunlar var:

- Sokratik, önce öğrenciye ürettiren bir öğretmenlik.
- Serbest hatırlama ile doğrulama.
- FSRS ile aralıklı tekrar.
- Bağımsız bir değerlendirici (bizim kör izleyicinin karşılığı).
- `~/.claude/learning/` altında dosyalarda tutulan öğrenci durumu.

İki nedenle önemli:

- **Claude Code karşılığı:** CLAUDE.md'de "skill'in Claude Code'daki karşılığı henüz tasarlanmadı" diye bir not var. engram, öğrenci durumunu dosyalarda tutan çalışan bir örnek.
- **Prior-art belgesi:** aralıklı tekrar motorları (SuperMemo, Anki/FSRS), ustalık platformları (ALEKS, Khan, Math Academy, Duolingo), keşfedilebilir açıklamalar (Bret Victor, Quantum Country), klasik akıllı öğretim sistemleri (Cognitive Tutor; VanLehn 2011, adım düzeyinde uyarlama) ve LLM öğretmenleri (Khanmigo, LearnLM, Study Mode, Claude Learning Mode) üzerine derli toplu bir özet. Aşama 3 için iyi bir başlangıç noktası.

**Özgün katkı açısından:** engram'da kalıcı öğrenci modeli, zamanlama ve bağımsız değerlendirme var. Okuduğumuz kadarıyla oturumlardaki yanlış anlamalardan kural üreten, insan onayıyla büyüyen bir döngü yok. Bizim aday özgün katkımız ("hatadan kurala döngü" ve "materyal türüne göre dallanma") hâlâ boşta görünüyor. Ama bu, kanıtla gösterilmesi gereken bir iddia.

### 3. Claude kataloğundaki diğer adaylar

| Plugin | Ne yapıyor | Bizim için |
|---|---|---|
| deep-research (etkin) | Çok kaynaklı araştırma raporu | Aşama 3 literatür taraması |
| research-superpowers | Fikir → literatür → analiz → taslak → hakem hattı | Aşama 3; bağımlılıkları ağır, önce okunmalı |
| math-olympiad (Anthropic) | İspatı taze bağlamlı doğrulayıcılarla denetleme | Kör izleyici ve eleştirmen ajanla aynı desen; okumaya değer |
| skill-creator (etkin) | Skill için test ve karşılaştırma | personal-educator'ın davranışını test etmek |
| Study Desk | Materyalden sadık soru üretip "doğru, eksik, yanlış" diye notlama | Vizyondaki "materyal türü modülü" için örnek |
| Diagrams (Kroki) | WaveDrom dahil 20+ diyagram türü | Verilog paketi için zamanlama çizimleri; çizimler kroki.io'ya gönderiliyor |
| learning-tutor, Ágora Learning | Benzer tutor'lar (profil, FSRS, Sokratik) | Kaynakları doğrulanamadı; learning-tutor her turun sonunda çalışan bir hook kuruyor, kurmadan önce okunmalı |

**Gerek yok:** StudyPath, Noteflix, Loopky, Finance Tutor, ADHD Study Coach, CellCog, Figma, Mathbox.

### 4. ChatGPT Study Mode

Study Mode ayrı bir model değil, OpenAI'nin öğretmenler ve pedagoji uzmanlarıyla yazdığını söylediği bir sistem komutu. Komutun metni Simon Willison tarafından modelden çıkarıldı; OpenAI bunu doğrulamadı. Bizim `SKILL.md`'den çok daha kısa ve genel. Öne çıkan ilkeleri şunlar:

- Öğrencinin hedefini ve düzeyini hafifçe sor.
- Bildiklerinin üstüne kur.
- Cevabı verme; soru, ipucu ve küçük adımlarla buldur.
- Zor kısımlardan sonra fikri kendi sözleriyle söyleyebildiğini kontrol et.
- Ritmi değiştir: açıklama, soru ve etkinliği karıştır; öğrenciden sana öğretmesini iste.
- Kısa yaz; bir sonraki adımı hep bil, işini gören etkinliği bitir.

Study Mode'un sınırı, engram'ın tespitiyle aynı: **oturum içinde Sokratik ama hafızasız.** Öğrenci modeli, zamanlama ve ölçüm yok.

### 5. OpenAI plugin deposu, GPT Store ve uygulama dizini

- **`openai/plugins` (Codex):** 61 plugin var, hiçbiri eğitim ya da tutor değil. **consensus** (bilimsel makale arama) ve **zotero** (kaynak yönetimi) Aşama 3 için işe yarayabilir. **plugin-eval**, skill-creator'ın karşılığı. Codex skill'leri de SKILL.md biçimini kullanıyor; ileride yazılacak bir skill iki tarafta da çalışabilir.
- **GPT Store:** Khan Academy (Tutor Me, Code Tutor), CK-12 Flexi, Tutoring Pro, Socratic Learning. Komutları kapalı, bilgiler çoğunlukla üçüncü taraf listelerden. Kalıcı öğrenci modeli ya da aralıklı tekrar doğrulanamadı. İnceleyip alabileceğimiz bir şey yok.
- **ChatGPT uygulamaları (Apps SDK):** MCP üzerine kurulu, yaklaşık 1.600 uygulama var. Eğitim uygulamalarının güvenilir bir listesi bulunamadı. Platform sorusu için önemli bir yan bilgi: araçlarımız (`calc`, `names`, `gate`…) bir MCP sunucusu olarak yazılırsa hem Claude'da hem ChatGPT'de çalışabilir.

## Aday kurallar

**27 Kasım kararı:** yalnızca belirgin biçimde artı olan eklendi: maliyeti yok denecek kadar az, var olan bir kuralı netleştiren ve hiçbir şeyi bozmayan. Geri kalanlar not edildi. Not edilen bir adayın tetikleyicisi görülünce tek satırlık bir hatırlatma yapılır: ders sırasında öğretmen notunda (`SKILL.md`, "Noted candidates"), tasarım sırasında proje oturumunda. Uygulamaya Muhammet karar verir; bir aday ancak oturum kanıtıyla birlikte önerilir.

| Aday | Kaynak | Bizde şu an | Ne eklerdi | Durum | Ne zaman hatırlatılır |
|---|---|---|---|---|---|
| Yardımsız kontrol noktası | Library: unassisted-evidence-checkpoint | Çözüm kuralının ikinci şartı: "eski fikri tetikleyecek yeni bir vakayı doğru çözer" | Bu kontrolün ipucu verilmeden, yüzeyi farklı bir soruyla yapılması ve kayıtta "yardımsız" diye ayrı işaretlenmesi | **eklendi** (27 Kasım; Muhammet'in kararı, oturum kanıtı yok) | — |
| Öğrenciye anlattırma (teach-back) | Library: teach-back-evaluator; Study Mode | Seviye 4 "kendiliğinden türetir"; yanlış anlama çözümü için "kendi sözleriyle söyler" | Öğrenci, yalnızca önceki üniteleri bilen birine konuyu anlatır; anlatım tutarlılık, eksiksizlik ve yanlış anlama riski üzerinden notlanır. Seviye 4 için somut bir kanıt yolu | not edildi (iki bağımsız kaynakta var) | Bölüm kapanışında; ya da bir kavramın seviye 4'e çıkması gerektiği hâlde bunu gösteren kendiliğinden bir türetme olmadığında |
| Cevaptan sonra da güven | Library: confidence-calibration-check | Yalnızca cevaptan önce güven sorusu | Öncesi ile sonrası arasındaki fark ayrı bir veri; pilot raporundaki "güven ile sonuç uyumu" analizini güçlendirir | not edildi (her cevaba bir dokunuş daha ekler) | Güven seçimleri ile sonuçlar sık ayrıştığında (örneğin bir ünitede iki kez "Emindim" ama yanlış) |
| İpucundan önce "ne denedin?" | Library: progressive-hint-ladder | H1 "soruyu somutlaştır" | Önce öğrencinin denemesini ve nasıl bir yardım istediğini sormak; yardım türü hata teşhisiyle birleşebilir | not edildi | Denemeden "ipucu" istediğinde; ya da nerede takıldığı bilinmediği için bir basamak boşa gittiğinde |
| Desteği geri çekme (fading) | Library: fading-manager, worked-example-fading-designer | Yok | Kavram seviyesi yükseldikçe çizim, iskelet ve ipucu desteğini azaltmak | not edildi (tasarım gerektirir) | Seviye 3'teki bir kavram hâlâ tam çizim ya da iskeletle sorulduğunda; ya da iskeletli adımlarda "hızlanalım", "bu kolay" dediğinde |
| Yanlış çözülmüş örnek | Library: erroneous-example-designer | Önce karşı örnek (öğrencinin modeli imkânsız bir sonuç verir) | Hatalı bir çözümü gösterip hatayı buldurmak; karşı örneğe ikinci bir yol | not edildi | Bir `learner_belief` karşı örnekten sonra da sürdüğünde ya da yeniden açıldığında |
| Ritim | Study Mode | Yok; her ünite aynı kalıpla ilerliyor | Açıklama, tahmin, alıştırma ve anlattırma arasında bilinçli geçiş | not edildi (zayıf: tek kaynak, ölçmesi zor) | Yorgunluk ya da tekdüzelik işareti verdiğinde; ya da birkaç ünite üst üste aynı kalıpla geçtiğinde |

**Proje oturumlarında hatırlatılacaklar** (ders dışı, tasarım işi):

| Not | Ne zaman hatırlatılır |
|---|---|
| Kayıt şeması önerisi (aşağıda) | Stash ya da log biçimine, `metrics` aracına veya Aşama 2 tasarım belgesine dokunulduğunda |
| engram (öğrenci durumu dosyalarda) | Skill'in Claude Code karşılığı tasarlanırken |
| Araçlar bir MCP sunucusu olarak | Platform sorusu (Claude, ChatGPT ya da bağımsız uygulama) açıldığında |
| Library'nin 12. ve 20. alanı, EXCLUSIONS.md, engram prior-art, consensus/zotero | Aşama 3 literatür taraması başladığında |
| Lisans uyumsuzluğu (CC BY-SA ve MIT) | Dışarıdan bir skill'in ya da komutun metni alınmak istendiğinde |

## Kayıt şeması önerisi (tasarım gerektirir)

Bugünkü stash kaydı şu alanları tutuyor: ünite, soru, cevabı, gerekçesi, güven, iddia, değerlendirme ölçütü, tarih. Library'nin `evidence_captured` alanlarından eksik olanlar:

- `confidence_after`: cevaptan sonraki güven.
- `hint_level_reached`: hangi ipucu basamağına çıkıldı (bugün serbest metin).
- `error_type`: hata türü (hata teşhisindeki beş seçenekle aynı).
- `assistance`: yardımsız ya da yardımlı.
- `transfer_check`: yeni bir durumda mı soruldu.
- `followup_due`: yardımsız takibin tarihi.

25 Kasım ölçek tartışmasında önerdiğimiz iki alan da buna eklenmeli:

- **Düzeltme nereye gider:** araç, çekirdek kural, konu paketi ya da öğrenci modeli.
- **Etiketin kaynağı:** öğrenci, tasarımcı ya da kör izleyici.

Bu bir **kod değişikliği değil, tasarım önerisi**. Önce düz metin bir tasarım yazılır ve onaylanır. Ardından `edu_tools.py` (`metrics`) ve skill buna göre değişir.

## Lisans

- Education Skills Library **CC BY-SA 4.0**, bizim depo **MIT**. Bir skill'in metni olduğu gibi kopyalanırsa o kısım CC BY-SA olmak zorunda. Yol: fikirleri ve kaynak araştırmaları kendi sözlerimizle yazmak ve skill adını kaynak olarak göstermek, ya da bir skill'i olduğu gibi kullanmak gerekirse onu ayrı bir klasörde kendi lisansıyla tutmak.
- Study Mode komutu OpenAI'nin; kısa alıntı dışında kopyalanmaz.
- engram'ın lisansı kontrol edilmedi; kod alınmadan önce bakılmalı.

## Sonraki adımlar (öneri)

1. Pilot sürerken hiçbir plugin kurulmaz ve canlı skill'e bir şey eklenmez.
2. Library'nin 20. ve 12. alanındaki skill'ler ve engram'ın prior-art belgesi, Aşama 3'teki literatür taramasının ilk kaynakları olarak işaretlenir.
3. Kayıt şeması için düz metin bir tasarım yazılır (yukarıdaki bölüm).
4. Aday kurallar, oturumlarda onları gerektiren bir yanlış anlama görüldükçe tek tek önerilir.
5. Platform sorusu için "araçlar bir MCP sunucusu olarak" seçeneği tasarım belgesine (Aşama 2) not edilir.

## Kaynaklar

- [GarethManning/education-agent-skills](https://github.com/GarethManning/education-agent-skills) (README, EXCLUSIONS.md, `skills/student-learning/`)
- [nagisanzenin/engram](https://github.com/nagisanzenin/engram) ve [prior-art belgesi](https://raw.githubusercontent.com/nagisanzenin/engram/master/docs/02-prior-art.md)
- [anthropics/k12-teacher-skills](https://github.com/anthropics/k12-teacher-skills)
- [OpenAI: Introducing study mode](https://openai.com/index/chatgpt-study-mode/)
- [Simon Willison: Study Mode sistem komutu](https://simonwillison.net/2025/Jul/29/openai-introducing-study-mode/)
- [Edutopia: Putting ChatGPT's Study Mode Through Its Paces](https://www.edutopia.org/article/putting-chatgpts-study-mode-through-its-paces/)
- [OpenAI Codex skills](https://developers.openai.com/codex/skills)
- [openai/plugins](https://github.com/openai/plugins)
- [OpenAI: Introducing apps in ChatGPT](https://openai.com/index/introducing-apps-in-chatgpt/)
- [SlideSpeak: The best GPTs for students](https://slidespeak.co/blog/the-best-gpts-for-students)
