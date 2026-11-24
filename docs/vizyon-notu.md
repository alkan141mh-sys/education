# Öğrenme zemini — vizyon notu

Nov 24, 2026 · @Muhammet Alkan

## Fikir

Yapay zekâ destekli, açık kaynak bir öğrenme zemini kurmak. Bu zemin iki
şeyi birleştiriyor: farklı öğrenme yöntemlerinin araştırma düzeyinde
analizi ve bu yöntemleri gerektiğinde kullanan, hatalarından öğrenerek
büyüyen bir skill/plugin yapısı. Uzun vadeli hedef bir "eğitimde köklü
değişim" (education overhaul). Kısa vadede ise kendi öğrenme sürecimde
sınanan bir yöntemle başlanıyor.

## Neden

Eğitim beni en çok çeken konulardan biri. Birebir özel ders, kişiye göre
ayarlanan tempo, aralıklı tekrar ve hatırlama pratiği gibi işe yaradığı
bilinen yöntemler bugüne kadar pahalıydı ve ancak az kişinin
ulaşabildiği yöntemlerdi. Yapay zekâ çağında bu yöntemler herkese, her
konuda ve kişiye göre uyarlanmış olarak sunulabilir.

Ama tek başına bir yapay zekâ öğretmeni iyi öğretmeye yetmiyor.
Terimleri tanımlamadan kullanmak ya da öğrencinin kafasındaki resmi
sormadan açıklama yığmak gibi hatalar tekrar ediyor. Bu hataları
yakalayıp kurala dönüştüren bir döngü gerekiyor.

## Üç bileşen

1.  **Araştırma:** Öğrenme yöntemlerinin literatür düzeyinde analizi
    (özel ders, akıllı öğretim sistemleri, aralıklı tekrar, ipucu
    merdivenleri, yanlış anlamayı karşı örnekle çözme). Amaç: hangi
    yöntemin hangi öğrenci, konu ve materyal türünde işe yaradığını
    bilmek.

2.  **Açık kaynak plugin:** Ortak bir yöntem çekirdeği, materyal türüne
    göre modüller (devre ünitesi, makale, ders kitabı bölümü, tasarım
    belgesi, problem seti), konuya göre ince paketler ve kuralları
    zorlayan araçlar (isim kontrolü, sayı kontrolü, çizim kontrolü).

3.  **Kendini geliştiren döngü:** Oturumlardaki yanlış anlamalar ve
    ölçümler kaydedilir, tekrar eden hatalar kurala dönüşür. Bu kurallar
    insan ve yapay zekâ incelemesinden geçtikten sonra yapıya eklenir.
    Yapı bu şekilde dallanarak büyür.

## Bugün nerede

Projenin el yapımı ilk hâli zaten çalışıyor:

- **Yazılı bir yöntem:** personal-educator skill'i (v2, 24 Kasım
  pilotu). İçinde öğrenci modeli, karışıklığı çözme adımları, ipucu
  merdiveni, aralıklı tekrar ve çizim kuralları var.

- **İki konu:** Devre tasarımı (araçları, öğrenci modeli ve ders panosu
  bu konu için kuruldu) ve moleküler haberleşme (makale okuma, bilgi
  teorisine giriş).

- **Ölçüm:** Başlangıç değerleri kaydedildi (23 Kasım: yaklaşık 2,5
  saatte yaklaşık 6 yanlış anlama ve 2 yön kaybı).

- **Hatadan kurala döngü:** Her yanlış anlama kimden kaynaklandığı ve
  nedeniyle birlikte kaydediliyor. Bu kayıtlardan çıkan kurallar skill'e
  ekleniyor. 24 Kasım'da bir makale okuma oturumundaki karışıklıktan
  altı genel kural çıktı (örneğin önce makalenin amacını anlatmak, her
  sayının neyin sayısı olduğunu söylemek).

Şimdilik eksik olan şey ölçek: tek öğrenci, tek öğretmen ve birkaç
oturum var.

## Aşamalar

1.  **Veri toplayan kullanım (şimdi):** Tek ana skill. Materyal türleri
    aynı skill'in içinde bölümler olarak duruyor. Yeni bir konuya
    başlarken konu paketi otomatik olarak taslaklanıyor. Kayıtlar
    ileride analiz edilebilecek biçimde tutuluyor: yanlış anlama türü,
    nedeni, hangi kuralın eksik olduğu.

    - Geçiş koşulu: 2-3 farklı konu ve materyal türü bu yapıyla çalışmış
      olmalı.

2.  **Tasarım belgesi:** Kod yazmadan, düz metin bir tasarım. Hangi
    parçaların ortak olduğu ve hangilerinin konuya göre değiştiği
    toplanan kayıtlardan çıkarılır. Plugin mimarisi, kural ekleme süreci
    ve ölçüm planı belirlenir.

3.  **Araştırma ayağı:** Öğrenme yöntemleri literatürünün sistematik bir
    taraması yapılır. Her yöntem plugin'deki bir modüle ya da kurala
    eşlenir.

4.  **Açık kaynak sürüm:** İlk plugin sürümü ve katkı kuralları
    yayımlanır. Hatadan kurala döngü başka öğrencilere ve katkıcılara
    açılır.

## Açık sorular

- Projenin özgün katkısı ne olacak? Var olan akıllı öğretim sistemleri
  ve yapay zekâ öğretmenlerinden farkı nerede? (Şimdiki aday: yöntemin
  konuya ve materyal türüne göre dallanması ve hatadan kural üreten
  döngü.)

- Etki nasıl ölçülecek? Hangi metrikler kullanılacak, kontrol grubu
  olacak mı?

- Kendini geliştiren döngü nasıl denetlenecek? Yeni bir kuralı kim
  onaylayacak? Kötü bir kuralın yayılması nasıl önlenecek?

- Öğrenci verileri ve gizlilik: kayıtlar açık kaynak bir yapıda nasıl
  paylaşılacak?

- Hangi platform üzerinde çalışacak? Claude skill/plugin olarak mı,
  bağımsız bir uygulama olarak mı, yoksa ikisi birden mi?

- Kişisel öğrenme hedefleri, moleküler haberleşme gibi süren projeler ve
  bu uzun soluklu proje arasında zaman nasıl bölünecek?
