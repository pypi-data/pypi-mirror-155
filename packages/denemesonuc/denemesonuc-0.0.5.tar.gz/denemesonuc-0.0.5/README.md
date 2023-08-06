# denemesonuc
orbim ölçme değerlendirme şeyi için bir modül.

## yükleme
`pip install denemesonuc`

## basit kullanım
```python
from denemesonuc import Denek, Deneme

biri = Denek(ad="biri", no=7, sinif_duzeyi=9, sehir="ŞEHİR", okul_adi="Okul Adı")
deneme = Deneme(deneme_adi="deneme adı", url="https://bes.karnemiz.com/?pg=ogrgiris")
biri.fetchDeneme(deneme)
sonuc = biri.getDeneme("deneme adı")

sinif=sonuc.sinif
puan=sonuc.puan

genel_dogru=sonuc.genel.dogru
fizik_dogru=sonuc.fzk.dogru
edebiyat_yanlis=sonuc.edb.yanlis
kimya_bos=sonuc.kim.bos
matematik_net=sonuc.mat.net

sinif_derece=sonuc.derece.sinif
kurum_derece=sonuc.derece.kurum
il_derece=sonuc.derece.il
genel_derece=sonuc.derece.genel
```