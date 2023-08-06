import warnings
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
import atexit, copy

__all__ = ["Denek", "Deneme", "DenemeSonucObject", "DenemeDereceObject"]

opts = Options()
opts.headless = True
driver = webdriver.Firefox(options=opts)


def _cleanup():
    driver.quit()


atexit.register(_cleanup)


class DenemeSonucObject:
    """derslere göre sonuçları saklamak için oluşturulan, pek de bir amacı olmayan sınıf"""

    def __init__(
        self, soru: int = 0, dogru: int = 0, yanlis: int = 0, bos: int = 0, net: float = 0
    ) -> None:
        """### derslere göre sonuçlar

        `soru`: soru sayısı
        `dogru`: doğru sayısı
        `yanlis`: yanlış sayısı
        `bos`: boş sayısı
        `net`: net"""
        if not soru:
            self = None
            return
        self.soru = soru
        self.dogru = dogru
        self.yanlis = yanlis
        self.bos = bos
        self.net = net

    def __bool__(self):
        return self == None


class DenemeDereceObject:
    """dereceleri tutmak için oluşturulan, pek de bir amacı olmayan sınıf"""

    def __init__(self, sinif: int, kurum: int, il: int, genel: int) -> None:
        """### dereceler

        `sinif`: sınıf derecesi
        `kurum`: kurum derecesi
        `il`: il derecesi
        `genel`: genel derece"""
        self.sinif = sinif
        self.kurum = kurum
        self.il = il
        self.genel = genel


class Deneme:
    """deneme hakkında bilgileri tutan sınıf"""

    def __init__(self, deneme_adi: str = "", url: str = "https://bes.karnemiz.com/?pg=ogrgiris"):
        """### denemenin genel bilgileri

        `deneme_adi`: deneme adı

        `url`: deneme sonuç sayfasının url'si. varsayılan olarak https://bes.karnemiz.com/?pg=ogrgiris"""
        self.deneme_adi = deneme_adi
        self.url = url
        if not self.deneme_adi:
            warnings.warn(
                "deneme adı boş, ilk gelen neyse onu kullanıcaz, bu toplu kullanımlarda sıkıntı yaratabilir bilgin olsun"
            )


class Denek:
    """# denemeye giren kişi. denek.

    `fetchDeneme`: verilen denemenin sonuçlarını çeker
    `getDeneme`: çekilen deneme sonucunu döndürür"""

    def __init__(self, ad: str, no: int, sinif_duzeyi: int, sehir: str, kurum: str) -> None:
        """### denek bilgileri

        `ad`: ad
        `no`: numara
        `sinif_duzeyi`: sınıf düzeyi
        `sehir`: şehir, tamamı büyük harf olmalı
        `kurum`: okulun adı, siteye yazıldığında listede ilk sonuç olarak görünmeli"""
        self.ad = ad
        self.no = no
        self.sinif_duzeyi = sinif_duzeyi
        self.sehir = (
            sehir.replace("ı", "I").replace("i", "İ").upper()
        )  # pythonın localeler ile sorunu var
        self.kurum = kurum
        self.__deneme = {}

    def __repr__(self) -> str:
        """can sıkıntısı. denekleri stringe çevirmek için. abracadabra"""
        return f"Denek: {self.no} ({self.ad})"

    def fetchDeneme(self, deneme: Deneme) -> int:
        """### denek ve deneme bilgileriyle deneme sonuçlarını çeker

        return:
        - 0: çekme başarılı
        - 1: reserved for future use
        - 2: denek denemeye girmemiş"""

        d = copy.deepcopy(deneme)

        driver.get(d.url)

        seviye = Select(driver.find_element("id", "seviye"))
        seviye.select_by_visible_text(f"{str(self.sinif_duzeyi)}.Sınıf")

        ilkodu = Select(driver.find_element("id", "ilkodu"))
        ilkodu.select_by_visible_text(self.sehir)

        okuladi = driver.find_element("id", "kurumarama")
        okuladi.send_keys(self.kurum)
        WebDriverWait(driver, 2).until(EC.presence_of_element_located(("id", "ui-id-2")))
        okulasilad = driver.find_element("id", "ui-id-2")
        okulasilad.click()

        ogrnoinp = driver.find_element("id", "ogrencino")
        ogrnoinp.send_keys(str(self.no))

        ogradinp = driver.find_element("id", "isim")
        ogradinp.send_keys(self.ad)

        driver.find_element("name", "bulbtn1").submit()

        document = "/html/body/div[1]/section/div/div"
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(("xpath", f"{document}/div[1]"))
        )

        deneme_select = Select(driver.find_element("id", "digersinavlarcombo"))
        deneme_type = deneme_select.first_selected_option.text
        if (deneme_type != d.deneme_adi) and d.deneme_adi:
            if d.deneme_adi in [i.text for i in deneme_select.options]:
                deneme_select.select_by_visible_text(d.deneme_adi)
                WebDriverWait(driver, 5).until(
                    EC.text_to_be_present_in_element(
                        ("xpath", f"{document}/div[4]/div/div"), d.deneme_adi
                    )
                )
            else:
                return 2

        derece_head = f"{document}/div[5]/div/div[3]/div"
        d_sinif = int(driver.find_element("xpath", f"{derece_head}/div[2]").text)
        d_kurum = int(driver.find_element("xpath", f"{derece_head}/div[3]").text)
        d_il = int(driver.find_element("xpath", f"{derece_head}/div[5]").text)
        d_genel = int(driver.find_element("xpath", f"{derece_head}/div[6]").text)
        d.derece = DenemeDereceObject(d_sinif, d_kurum, d_il, d_genel)

        d.sinif = driver.find_element("xpath", f"{document}/div[1]/div[2]/div[3]").text.replace(
            "-", ""
        )  # 9larda "-9A" gibi, diğer sınıflarda "11A" gibi gözüküyor o yüzden

        d.puan = float(
            driver.find_element("xpath", f"{document}/div[5]/div/div[1]/div/div")
            .text.replace(",", ".")
            .split(" ")[-1]
        )  # "puanınız: 123,456" gibi göründüğü için

        available_heads = []
        i = 0
        while True:
            try:
                i += 1
                head = f"{document}/div[7]/div/div[{i}]/div[1]/div[2]/div[2]"
                if driver.find_element("xpath", f"{head}/div[1]").text:
                    available_heads.append(head)
            except:
                break

        def getDers(name: str = "") -> DenemeSonucObject:
            """#### dersleri tek tek toplamak yerine yazılmış fonksiyon"""
            if name:
                matches = [
                    head
                    for head in available_heads
                    if name == driver.find_element("xpath", head[:-14] + "/div[1]/div/div").text
                ]
                if not matches:
                    return DenemeSonucObject()
                head = matches[0]
            else:
                head = f"{document}/div[6]/div/div/div[1]/div[2]/div[2]"  # genel sonuçlar her zaman vardır herhalde

            d_ss = int(driver.find_element("xpath", f"{head}/div[1]").text)
            d_ds = int(driver.find_element("xpath", f"{head}/div[2]").text)
            d_ys = int(driver.find_element("xpath", f"{head}/div[3]").text)
            d_bs = d_ss - d_ds - d_ys
            d_ns = float(driver.find_element("xpath", f"{head}/div[4]").text.replace(",", "."))
            return DenemeSonucObject(d_ss, d_ds, d_ys, d_bs, d_ns)

        d.genel = getDers()
        d.edb = getDers("TYT Türkçe Testi Toplamı")
        d.trh = getDers("Tarih-1")
        d.cog = getDers("Coğrafya-1")
        d.din = getDers("Din Kül. ve Ahl. Bil.")
        d.mat = getDers("TYT Matematik Testi Toplamı")
        d.fiz = getDers("Fizik")
        d.kim = getDers("Kimya")
        d.biy = getDers("Biyoloji")
        d.fls = getDers("Felsefe")
        d.sfl = getDers("Felsefe (Seçmeli)")

        self.__deneme[d.deneme_adi] = d
        return 0

    def getDenemeList(self) -> list[str]:
        """### girilen denemelerin adlarının listesini döndürür"""
        return list(self.__deneme.keys())

    def getDeneme(self, deneme_adi: str) -> Deneme:
        """### çekilmiş deneme sonucunu döndürür

        `deneme_adi`: deneme adı"""
        return self.__deneme[deneme_adi]
