import math
from operator import index
import thanhtungcalendartspt.Leaps as Nhuan
import thanhtungcalendartspt.NewMoonGMT0 as Soc
import thanhtungcalendartspt.SolsticeGMT7 as TietKhi
import thanhtungcalendartspt.ListSearch as LS


def TkNam(nam):
    index0 = TietKhi.Years.index(nam-1)
    tk = []
    for i in range(71):
        tk.append(TietKhi.Years[index0+i])
    return tk


def TkThang(nam):
    index0 = TietKhi.Years.index(nam-1)
    tk = []
    for i in range(71):
        tk.append(TietKhi.Months[index0+i])
    return tk


def TkNgay(nam):
    index0 = TietKhi.Years.index(nam-1)
    tk = []
    for i in range(71):
        tk.append(TietKhi.Days[index0+i])
    return tk


def TkGio(nam):
    index0 = TietKhi.Years.index(nam-1)
    tk = []
    for i in range(71):
        tk.append(TietKhi.Hours[index0+i])
    return tk


def TkPhut(nam):
    index0 = TietKhi.Years.index(nam-1)
    tk = []
    for i in range(71):
        tk.append(TietKhi.Minutes[index0+i])
    return tk


def TkTen(nam):
    index0 = TietKhi.Years.index(nam-1)
    tk = []
    for i in range(71):
        tk.append(TietKhi.Names[index0+i])
    return tk


def JDTietKhi(nam, muigio):
    index0 = TietKhi.Years.index(nam-1)
    tk = []
    gio = TkGio(nam)
    phut = TkPhut(nam)
    for i in range(71):
        tk.append(TietKhi.JD[index0+i])
    for i in range(71):
        if ((gio[i]+phut[i]/60+muigio-7) >= 24):
            tk[i] = tk[i]+1
        elif ((gio[i]+phut[i]/60+muigio-7) < 0):
            tk[i] = tk[i]-1

    return tk


def SocNam(nam):
    index0 = Soc.Years.index(nam-1)
    s = []
    for i in range(38):
        s.append(Soc.Years[index0+i])
    return s


def SocThang(nam):
    index0 = Soc.Years.index(nam-1)
    s = []
    for i in range(38):
        s.append(Soc.Months[index0+i])
    return s


def SocNgay(nam):
    index0 = Soc.Years.index(nam-1)
    s = []
    for i in range(38):
        s.append(Soc.Days[index0+i])
    return s


def SocGio(nam):
    index0 = Soc.Years.index(nam-1)
    s = []
    for i in range(38):
        s.append(Soc.Hours[index0+i])
    return s


def SocPhut(nam):
    index0 = Soc.Years.index(nam-1)
    s = []
    for i in range(38):
        s.append(Soc.Minutes[index0+i])
    return s


def JDSoc(nam, muigio):
    index0 = Soc.Years.index(nam-1)
    s = []
    gio = TkGio(nam)
    phut = TkPhut(nam)
    for i in range(38):
        s.append(Soc.JD[index0+i])
    for i in range(38):
        if ((gio[i]+phut[i]/60+muigio-7) >= 24):
            s[i] = s[i]+1
        elif ((gio[i]+phut[i]/60+muigio-7) < 0):
            s[i] = s[i]-1

    return s


def JDTet(namDlNhapThuong, muiGio):
    jdSoc3Nam = JDSoc(namDlNhapThuong, muiGio)
    dongChi = JDDongChi(namDlNhapThuong, muiGio)
    a = 0
    thangNhuan = 0
    jdSocTet = 0
    for i in range(len(jdSoc3Nam)):
        if (jdSoc3Nam[i] >= dongChi):
            break
        a = i
    try:
        pos = Nhuan.Years.index(namDlNhapThuong-1)
    except:
        pos = -1
    if (pos > -1):
        thangNhuan = Nhuan.Months[pos]
    else:
        thangNhuan = 0
    # Nếu năm đó không nhuận tháng 11, 12 thì jdSocTet sẽ là JDSoc tháng Tý + 2
    if (thangNhuan != 11) and (thangNhuan != 12):
        jdSocTet = jdSoc3Nam[a+2]
    else:
        jdSocTet = jdSoc3Nam[a+3]
    return jdSocTet


def JDLapXuan(nam, muiGio):
    tenTietKhi = TkTen(nam)
    jdTietKhiNam = JDTietKhi(nam, muiGio)
    a = tenTietKhi.index(LS.DanhSach24TietKhi[0])+24
    return jdTietKhiNam[a]


def JDDongChi(nam, muiGio):
    tenTietKhi = TkTen(nam)
    jdTietKhiNam = JDTietKhi(nam, muiGio)
    a = tenTietKhi.index(LS.DanhSach24TietKhi[21])
    return jdTietKhiNam[a]


def JDHaChi(nam, muiGio):
    tenTietKhi = TkTen(nam)
    jdTietKhiNam = JDTietKhi(nam, muiGio)
    a = tenTietKhi.index(LS.DanhSach24TietKhi[9] + 24)
    return jdTietKhiNam[a]


def TietKhiHienTai(nam, thang, ngay, muiGio):
    jdTietKhi = JDTietKhi(nam, muiGio)
    tenTietKhi = TkTen(nam)
    jD = TinhJD(nam, thang, ngay)
    a = 0
    for i in range(len(jdTietKhi)):
        if (jdTietKhi[i] >= jD):
            break
        a = i
    return tenTietKhi[a]


def DoiJDGmtHienTai(nam, thang, ngay, gio, phut, gmt):
    jD = TinhJD(nam, thang, ngay)
    if(gio + phut/60 + gmt) > 24:
        jD = jD+1
    elif (gio + phut/60 + gmt) < 0:
        jD = jD-1
    else:
        jD += 0
    return jD


def TinhJD(nam, thang, ngay):
    a = math.floor((14-thang)/12)
    Y = nam+4800-a
    m = thang + 12*a - 3
    jD = ngay + math.floor((153*m+2)/5)+365*Y+math.floor(Y/4) - \
        math.floor(Y/100)+math.floor(Y/400)-32045
    if (jD < 2299161):
        jD = ngay + math.floor((153*m+2)/5)+365*Y+math.floor(Y/4)-32083
    # jD được coi là của GMT 0
    return jD


def SttSocHienTai(nam, thang, ngay, gio, phut, muigio):
    # Notes: phép tính Sóc ở đây lấy giờ chuyển ngày là 12h đêm, nhưng JD thì sớm hơn 1 tiếng, mục đích lấy giờ Tý
    # Thêm múi giờ vào tính JD hiện tại, là vì TinhJD cho ra điểm múi giờ = 0
    jD = TinhJD(nam, thang, ngay)+muigio/24.0
    if (gio == 23):
        jD += 1
    else:
        jD += 0
    jDSoc = JDSoc(nam, muigio)
    a = 0
    for i in range(len(jDSoc)):
        if(jDSoc[i] >= jD):
            break
        a = i
    return a


def JDSocHienTai(nam, thang, ngay, gio, phut, muigio):
    jD = TinhJD(nam, thang, ngay) + muigio/24.0
    if(gio == 23):
        jD += 1
    jDSoc = JDSoc(nam, muigio)
    a = 0
    for i in range(len(jDSoc)):
        if (jDSoc[i] >= jD):
            break
        a = i
    return jDSoc[a]


def JDSocTiepTheo(nam, thang, ngay, gio, phut, muigio):
    jD = TinhJD(nam, thang, ngay) + muigio/24.0
    if(gio == 23):
        jD += 1
    jDSoc = JDSoc(nam, muigio)
    a = 0
    for i in range(len(jDSoc)):
        if (jDSoc[i] >= jD):
            break
        a = i+1
    return jDSoc[a]


def SttTetTrongDuLieuSoc(nam, thang, ngay, gio, phut, muigio):
    namAmLich = NamAmLich(nam, thang, ngay, gio, muigio)
    jDTet = JDTet(namAmLich, muigio)
    jDSoc = JDSoc(nam, muigio)
    return jDSoc.index(jDTet)

# region Cac method tinh nam


def TichNamThaiAt(nam):
    return nam + 10153917


def NamThaiAt(nam, thang, ngay, gio, phut, muigio):
    jD0 = JDDongChi(nam+1, muigio)
    jD = DoiJDGmtHienTai(nam, thang, ngay, gio, phut, muigio)
    ketQua = 0
    if(jD < jD0):
        ketQua = nam
    else:
        ketQua = nam + 1
    return ketQua


def NamTietKhi(nam, thang, ngay, gio, phut, muigio):
    jD0 = JDLapXuan(nam, muigio)
    jD = DoiJDGmtHienTai(nam, thang, ngay, gio, phut, muigio)
    ketQua = 0
    if jD < jD0:
        ketQua = nam - 1
    elif jD >= jD0:
        ketQua = nam
    return ketQua


def NamAmLich(nam, thang, ngay, gio, muigio):
    jD0 = JDTet(nam, muigio)
    jD = TinhJD(nam, thang, ngay) + muigio/24.0
    ketQua = 0
    if(gio == 23):
        jD += 1
    else:
        jD += 0
    if(jD > jD0):
        ketQua = nam
    else:
        ketQua = nam - 1
    return ketQua


def CanNam(nam):
    return DoiCan((int(nam)+6) % 10)


def ChiNam(nam):
    return DoiChi((int(nam)+8) % 12)

# endregion


# region Cac method tinh thang
def TichThangAmLich(nam, thang, ngay, gio, phut, muigio):
    soThang = 0
    tenThangAmLich = TenThangAmLich(nam, thang, ngay, gio, phut, muigio)
    if(tenThangAmLich > 12):
        soThang = tenThangAmLich/100
    else:
        soThang = tenThangAmLich + 1
    namAmLich = NamAmLich(nam, thang, ngay, gio, muigio)
    return (TichNamThaiAt(namAmLich)-1)*12 + soThang + 12


def TenThangAmLichBangChu(nam, thang, ngay, gio, phut, muigio):
    bangSo = TenThangAmLich(nam, thang, ngay, gio, phut, muigio)
    tenBangChu = ["Giêng", "Hai", "Ba", "Tư", "Năm", "Sáu", "Bảy", "Tám", "Chín", "Mười", "Mười Một", "Mười Hai",
                  "Giêng (Nhuận)", "Hai (Nhuận)", "Ba (Nhuận)", "Tư (Nhuận)", "Năm (Nhuận)", "Sáu (Nhuận)", "Bảy (Nhuận)", "Tám (Nhuận)", "Chín (Nhuận)", "Mười (Nhuận)", "Mười Một (Nhuận)", "Mười Hai (Nhuận)"]
    tenBangSo = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 100,
                 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200]
    a = tenBangSo.index(bangSo)
    return tenBangChu[a]


def TenThangAmLich(nam, thang, ngay, gio, phut, muigio):
    tenThang = 0
    nhuan0 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1]
    nhuan1 = [1, 100, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    nhuan2 = [1, 2, 200, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    nhuan3 = [1, 2, 3, 300, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    nhuan4 = [1, 2, 3, 4, 400, 5, 6, 7, 8, 9, 10, 11, 12]
    nhuan5 = [1, 2, 3, 4, 5, 500, 6, 7, 8, 9, 10, 11, 12]
    nhuan6 = [1, 2, 3, 4, 5, 6, 600, 7, 8, 9, 10, 11, 12]
    nhuan7 = [1, 2, 3, 4, 5, 6, 7, 700, 8, 9, 10, 11, 12]
    nhuan8 = [1, 2, 3, 4, 5, 6, 7, 8, 800, 9, 10, 11, 12]
    nhuan9 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 900, 10, 11, 12]
    nhuan10 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1000, 11, 12]
    nhuan11 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 1100, 12]
    nhuan12 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1200]
    sttThangAm = SttThangAmLich(nam, thang, ngay, gio, phut, muigio)
    thangNhuan = ThangNhuanAmLich(nam, thang, ngay, gio, phut, muigio)
    if thangNhuan == 0:
        tenThang = nhuan0[sttThangAm]
    elif thangNhuan == 1:
        tenThang = nhuan1[sttThangAm]
    elif thangNhuan == 2:
        tenThang = nhuan2[sttThangAm]
    elif thangNhuan == 3:
        tenThang = nhuan3[sttThangAm]
    elif thangNhuan == 4:
        tenThang = nhuan4[sttThangAm]
    elif thangNhuan == 5:
        tenThang = nhuan5[sttThangAm]
    elif thangNhuan == 6:
        tenThang = nhuan6[sttThangAm]
    elif thangNhuan == 7:
        tenThang = nhuan7[sttThangAm]
    elif thangNhuan == 8:
        tenThang = nhuan8[sttThangAm]
    elif thangNhuan == 9:
        tenThang = nhuan9[sttThangAm]
    elif thangNhuan == 10:
        tenThang = nhuan10[sttThangAm]
    elif thangNhuan == 11:
        tenThang = nhuan11[sttThangAm]
    elif thangNhuan == 12:
        tenThang = nhuan12[sttThangAm]
    return tenThang


def ThangNhuanAmLich(namduong, thang, ngay, gio, phut, muigio):
    thangNhuan = 0
    namHienTai = NamAmLich(namduong, thang, ngay, gio, muigio)
    try:
        pos = Nhuan.Years.index(namHienTai)
    except:
        pos = -1
    if(pos > -1):
        thangNhuan = Nhuan.Months[pos]
    else:
        thangNhuan = 0
    return thangNhuan


def SttThangAmLich(nam, thang, ngay, gio, phut, muigio):
    s = SttSocHienTai(nam, thang, ngay, gio, phut, muigio)
    tet = SttTetTrongDuLieuSoc(nam, thang, ngay, gio, phut, muigio)
    stt = s - tet
    return stt


def TenThangThaiAt(tietKhi):
    tenThang = [1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6,
                7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 0, 0, 1]
    ketQua = LS.DanhSach24TietKhi.index(tietKhi)
    return LS.Chi[tenThang[ketQua]]


def TichThangThaiAt(nam, tietKhi):
    tenThang = TenThangThaiAt(tietKhi)
    a = LS.Chi.index(tenThang)+1
    return (TichNamThaiAt(nam)-1)*12+a


def TenThangTietKhi(tietKhi):
    tenThang = ["2", "2", "3", "3", "4", "4", "5", "5", "6", "6", "7",
                "7", "8", "8", "9", "9", "10", "10", "11", "11", "0", "0", "1", "1"]
    ketQua = LS.DanhSach24TietKhi.index(tietKhi)
    return LS.Chi[int(tenThang[ketQua])]


def TichThangTietKhi(namTietKhi, tietKhi):
    chill = ["DẦN", "MÃO", "THÌN", "TỊ", "NGỌ", "MÙI",
             "THÂN", "DẬU", "TUẤT", "HỢI", "TÝ", "SỬU"]
    tenThang = TenThangTietKhi(tietKhi)
    a = chill.index(tenThang)+1
    return (TichNamThaiAt(namTietKhi)-1)*12+a+3


def CanThang(tichThang):
    return DoiCan((tichThang + 48) % 10)


def ChiThang(tichThang):
    return DoiChi((tichThang+46) % 12)

# endregion

# region Cac method tinh ngay


def NgayAmLich(nam, thang, ngay, gio, phut, muiGio):
    # Vì âm lịch lấy 23h đêm làm giờ Tý khởi đầu ngày mới, do đó tại công thức hiệu chỉnh múi giờ tăng thêm 1h
    sttSocHienTai = SttSocHienTai(nam, thang, ngay, gio, phut, muiGio)
    jdSocHienTai = JDSocHienTai(nam, thang, ngay, gio, phut, muiGio)
    jdSocTiepTheo = JDSocTiepTheo(nam, thang, ngay, gio, phut, muiGio)
    kQ = 0
    jD = TinhJD(nam, thang, ngay) + muiGio/24.0
    if(gio == 23):
        jD += 1
    if (jD - jdSocTiepTheo) == 0 or (jD-jdSocHienTai) == 0:
        kQ = 1
    else:
        kQ = math.ceil(jD - jdSocHienTai)
    return kQ


def TichNgayTuJD(jd):
    return 3706920590 + jd


def jdTuTichNgay(tichNgay):
    return tichNgay - 3706920590


def TichNgayTu0Gio(nam, thang, ngay):
    return 3706920590 + TinhJD(nam, thang, ngay)


def TichNgayGioTy(nam, thang, ngay, gio):
    tichNgay = 0
    if(gio >= 23):
        tichNgay = 3706920590 + TinhJD(nam, thang, ngay) + 1
    else:
        tichNgay = 3706920590 + TinhJD(nam, thang, ngay)
    return tichNgay


def CanNgay(tichNgay):
    return DoiCan((tichNgay-1) % 10)


def ChiNgay(tichNgay):
    return DoiChi((tichNgay-1) % 12)


def SoNgayCanChi(tichNgay):
    canNgay = CanNgay(tichNgay)
    chiNgay = ChiNgay(tichNgay)
    canChiNgay = canNgay + " " + chiNgay
    stt = LS.DanhSach60CanChi.index(canChiNgay)
    return stt


def SoNgayQuaTheoTuTru(nam, thang, ngay, gio, phut, muiGio, thuanNghich10):
    # Tìm tiết khí hiện tại
    jdTietKhi = JDTietKhi(nam, muiGio)
    tenTietKhi = TkTen(nam)
    jd = TinhJD(nam, thang, ngay)
    a = 0
    for i in range(len(jdTietKhi)):
        if(jdTietKhi[i] >= jd):
            break
        a = i

    jdDau = 0
    jdSau = 0
    tkHienTai = '0'
    # Tìm tiết khí đầu tháng hiện tại và jd của nó
    b = LS.DanhSach24TietKhi.index(tenTietKhi[a])
    if b % 2 == 0:
        tkHienTai = tenTietKhi[a]
        jdDau = jdTietKhi[a]
    else:
        tkHienTai = tenTietKhi[a-1]
        jdDau = jdTietKhi[a-1]

    # Tìm tiết khí đầu tháng sau và jd của nó
    if (tkHienTai == tenTietKhi[a]):
        jdSau = jdTietKhi[a+2]
    else:
        jdSau = jdTietKhi[a+1]
    ketQua = 0
    if(thuanNghich10 == 1) and (gio < 23):
        ketQua = jdSau - jd
    elif(thuanNghich10 == 1) and (gio >= 23):
        ketQua = jdSau - jd - 1
    elif(thuanNghich10 == 0) and (gio < 23):
        ketQua = jd - jdDau
    elif(thuanNghich10 == 0) and (gio >= 23):
        ketQua = jd-jdSau+1
    return ketQua

# endregion

# region Cac method tinh gio


def TichGio(nam, thang, ngay, gio):
    tichNgayGioTy = TichNgayGioTy(nam, thang, ngay, gio)
    sttGio = int(DoiGio_temp(gio)[1])
    return (tichNgayGioTy-1)*12+sttGio


def CanGio(tichGio):
    return DoiCan((tichGio-1) % 10)


def ChiGio(gio):
    return DoiGio_temp(gio)[0]


def DoiGio_temp(gio):
    ketQua = ['0', '0']
    if gio == 0:
        ketQua[0] = 'TÝ'
        ketQua[1] = '1'
    elif gio == 1:
        ketQua[0] = 'SỬU'
        ketQua[1] = '2'
    elif gio == 2:
        ketQua[0] = 'SỬU'
        ketQua[1] = '2'
    elif gio == 3:
        ketQua[0] = 'DẦN'
        ketQua[1] = '3'
    elif gio == 4:
        ketQua[0] = 'DẦN'
        ketQua[1] = '3'
    elif gio == 5:
        ketQua[0] = 'MÃO'
        ketQua[1] = '4'
    elif gio == 6:
        ketQua[0] = 'MÃO'
        ketQua[1] = '4'
    elif gio == 7:
        ketQua[0] = 'THÌN'
        ketQua[1] = '5'
    elif gio == 8:
        ketQua[0] = 'THÌN'
        ketQua[1] = '5'
    elif gio == 9:
        ketQua[0] = 'TỊ'
        ketQua[1] = '6'
    elif gio == 10:
        ketQua[0] = 'TỊ'
        ketQua[1] = '6'
    elif gio == 11:
        ketQua[0] = 'NGỌ'
        ketQua[1] = '7'
    elif gio == 12:
        ketQua[0] = 'NGỌ'
        ketQua[1] = '7'
    elif gio == 13:
        ketQua[0] = 'MÙI'
        ketQua[1] = '8'
    elif gio == 14:
        ketQua[0] = 'MÙI'
        ketQua[1] = '8'
    elif gio == 15:
        ketQua[0] = 'THÂN'
        ketQua[1] = '9'
    elif gio == 16:
        ketQua[0] = 'THÂN'
        ketQua[1] = '9'
    elif gio == 17:
        ketQua[0] = 'DẬU'
        ketQua[1] = '10'
    elif gio == 18:
        ketQua[0] = 'DẬU'
        ketQua[1] = '10'
    elif gio == 19:
        ketQua[0] = 'TUẤT'
        ketQua[1] = '11'
    elif gio == 20:
        ketQua[0] = 'TUẤT'
        ketQua[1] = '11'
    elif gio == 21:
        ketQua[0] = 'HỢI'
        ketQua[1] = '12'
    elif gio == 22:
        ketQua[0] = 'HỢI'
        ketQua[1] = '12'
    elif gio == 23:
        ketQua[0] = 'TÝ'
        ketQua[1] = '1'

    return ketQua

# endregion

# region General Methods


def DoiCan(number):
    return LS.Can[number]


def DoiChi(number):
    return LS.Chi[number]


def ThuTrongTuan(nam, thang, ngay):
    thuTrongTuan = ["Chủ nhật", "Thứ hai", "Thứ ba",
                    "Thứ tư", "Thứ năm", "Thứ sáu", "Thứ bảy"]
    jd = TinhJD(nam, thang, ngay)
    stt = (jd + 1) % 7+1
    return thuTrongTuan[stt-1]


def JDSangNgayThangNam(jd):
    thoiGian = [0, 0, 0]
    a = 0
    b = 0
    c = 0
    d = 0
    e = 0
    if(jd > 2299160):
        a = jd+32044
        b = math.floor((4*a+3)/146097)
        c = a - math.floor((b*146097)/4)
    elif(jd <= 2299160):
        b = 0
        c = jd+32082
    d = math.floor((4*c+3)/1461)
    e = c-math.floor((1461*d)/4)
    m = math.floor((5*e+2)/153)
    thoiGian[0] = e - math.floor((153*m+2)/5)+1
    thoiGian[1] = m+3-12*math.floor(m/10)
    thoiGian[2] = b*100+d-4800+math.floor(m/10)
    return thoiGian
# endregion

# region Exception Input Methods


def TichNamThaiAtTren2200Duoi1100(nam):
    return TichNamThaiAt(nam)


def TichThangThaiAtTren2200Duoi1100(nam, thang):
    return (TichNamThaiAt(nam) - 1) * 12 + thang
# endregion

# region Cac method tinh tich ngay va phu dau


def TichNgayThaiAtGiapNgoSauDongChi(nam, thang, ngay, gio, phut, muiGio):
    namTinh = NamThaiAt(nam, thang, ngay, gio, phut, muiGio)
    jdDongChi = math.floor(JDDongChi(namTinh, muiGio))
    tichNgayDongChi = TichNgayTuJD(jdDongChi)
    soNgayDongChiTrong60 = SoNgayCanChi(tichNgayDongChi)+1
    a = 31 - soNgayDongChiTrong60
    tichNgayGiapNgoSauDongChi = tichNgayDongChi + a
    if(tichNgayGiapNgoSauDongChi < tichNgayDongChi):
        tichNgayGiapNgoSauDongChi += 60
    return tichNgayGiapNgoSauDongChi


def TichNgayThaiAtGiapTySauDongChi(nam, thang, ngay, gio, phut, muiGio):
    namTinh = NamThaiAt(nam, thang, ngay, gio, phut, muiGio)
    jdDongChi = math.floor(JDDongChi(namTinh, muiGio))
    tichNgayDongChi = TichNgayTuJD(jdDongChi)
    soNgayDongChiTrong60 = SoNgayCanChi(tichNgayDongChi)+1
    a = 1 - soNgayDongChiTrong60
    tichNgayGiapTySauDongChi = tichNgayDongChi+a
    if(tichNgayGiapTySauDongChi < tichNgayDongChi):
        tichNgayGiapTySauDongChi += 60
    return tichNgayGiapTySauDongChi


def TichSoKeNgayThaiAtTuDongChi(nam, thang, ngay, gio, phut, muiGio):
    tichNgayGiapTyKhoi = TichNgayThaiAtGiapTySauDongChi(
        nam, thang, ngay, gio, phut, muiGio)
    tichNgayGiapTyKhoiNamTruoc = TichNgayThaiAtGiapTySauDongChi(
        nam-1, thang, ngay, gio, phut, muiGio)
    jdHienTai = TinhJD(nam, thang, ngay)
    tichNgayHienTai = TichNgayTuJD(jdHienTai)
    ketQua = tichNgayHienTai - tichNgayGiapTyKhoi + 1
    if (ketQua < 1):
        ketQua = tichNgayHienTai - tichNgayGiapTyKhoiNamTruoc + 1
    return ketQua


def TichSoKeGioThaiAtTrongNam(nam, thang, ngay, gio, phut, muiGio):
    ketQua = [1, 1]
    # ketQua[0] là âm dương độn kể giờ; ketQua[1] là tích số cần tìm
    giapTyHaChiNamTruoc = TichNgayThaiAtGiapTySauHaChi(
        nam-1, thang, ngay, gio, phut, muiGio)
    giapNgoHaChiNamTruoc = TichNgayThaiAtGiapNgoSauHaChi(
        nam-1, thang, ngay, gio, phut, muiGio)
    giapTyDongChiNamNay = TichNgayThaiAtGiapTySauDongChi(
        nam, thang, ngay, gio, phut, muiGio)
    giapNgoDongChiNamNay = TichNgayThaiAtGiapNgoSauDongChi(
        nam, thang, ngay, gio, phut, muiGio)
    giapTyHaChiNamNay = TichNgayThaiAtGiapTySauHaChi(
        nam, thang, ngay, gio, phut, muiGio)
    giapNgoHaChiNamNay = TichNgayThaiAtGiapNgoSauHaChi(
        nam, thang, ngay, gio, phut, muiGio)
    giapTyDongChiNamSau = TichNgayThaiAtGiapTySauDongChi(
        nam+1, thang, ngay, gio, phut, muiGio)
    giapNgoDongChiNamSau = TichNgayThaiAtGiapNgoSauDongChi(
        nam + 1, thang, ngay, gio, phut, muiGio)
    jdHienTai = TinhJD(nam, thang, ngay)
    tichNgayHienTai = TichNgayTuJD(jdHienTai)
    chiGio = ChiGio(gio)
    chiGoc = ["TÝ", "SỬU", "DẦN", "MÃO", "THÌN", "TỊ",
              "NGỌ", "MÙI", "THÂN", "DẬU", "TUẤT", "HỢI"]
    a = chiGoc.index(chiGio)+1
    soGioThem = a
    haChiTruoc = 0
    dongChiHienTai = 0
    haChiHienTai = 0
    dongChiSau = 0
    if(giapTyHaChiNamTruoc >= giapNgoHaChiNamTruoc):
        haChiTruoc = giapNgoHaChiNamTruoc
    else:
        haChiTruoc = giapTyHaChiNamTruoc
    if(giapTyDongChiNamNay >= giapNgoDongChiNamNay):
        dongChiHienTai = giapNgoDongChiNamNay
    else:
        dongChiHienTai = giapTyDongChiNamNay
    if(giapTyHaChiNamNay >= giapNgoHaChiNamNay):
        haChiHienTai = giapNgoHaChiNamNay
    else:
        haChiHienTai = giapTyHaChiNamNay
    if(giapTyDongChiNamSau >= giapNgoDongChiNamSau):
        dongChiSau = giapNgoDongChiNamSau
    else:
        dongChiSau = giapTyDongChiNamSau

    if (tichNgayHienTai >= haChiTruoc) and (tichNgayHienTai < dongChiHienTai):
        ketQua[0] = 0  # Âm độn
        ketQua[1] = (tichNgayHienTai-haChiTruoc)*12+soGioThem
    elif(tichNgayHienTai >= dongChiHienTai) and (tichNgayHienTai < haChiHienTai):
        ketQua[0] = 1
        ketQua[1] = (tichNgayHienTai-dongChiHienTai)*12+soGioThem
    elif(tichNgayHienTai >= haChiHienTai) and (tichNgayHienTai < dongChiSau):
        ketQua[0] = 0
        ketQua[1] = (tichNgayHienTai-haChiHienTai)*12+soGioThem
    elif(tichNgayHienTai >= dongChiSau):
        ketQua[0] = 1
        ketQua[1] = (tichNgayHienTai-dongChiSau)*12+soGioThem
    return ketQua


def TichNgayThaiAtGiapTySauHaChi(nam, thang, ngay, gio, phut, muiGio):
    namTinh = NamThaiAt(nam, thang, ngay, gio, phut, muiGio)
    jdHaChi = math.floor(JDHaChi(namTinh, muiGio))
    tichNgayHaChi = TichNgayTuJD(jdHaChi)
    soNgayHaChiTrong60 = SoNgayCanChi(tichNgayHaChi)+1
    a = 1-soNgayHaChiTrong60
    tichNgayGiapTySauHaChi = tichNgayHaChi+a
    if(tichNgayGiapTySauHaChi < tichNgayHaChi):
        tichNgayGiapTySauHaChi += 60
    return tichNgayGiapTySauHaChi


def TichNgayThaiAtGiapNgoSauHaChi(nam, thang, ngay, gio, phut, muiGio):
    namTinh = NamThaiAt(nam, thang, ngay, gio, phut, muiGio)
    jdHaChi = JDHaChi(namTinh, muiGio)
    tichNgayHaChi = TichNgayTuJD(jdHaChi)
    soNgayHaChiTrong60 = SoNgayCanChi(tichNgayHaChi)+1
    a = 31 - soNgayHaChiTrong60
    tichNgayGiapNgoSauHaChi = tichNgayHaChi + a
    if(tichNgayGiapNgoSauHaChi < tichNgayHaChi):
        tichNgayGiapNgoSauHaChi += 60
    return tichNgayGiapNgoSauHaChi


def TichNgayPhuDauDuongCucDonGiap(nam, thang, ngay, gio, phut, muiGio):
    namTinh = NamThaiAt(nam, thang, ngay, gio, phut, muiGio)
    jdDongChi = JDDongChi(namTinh, muiGio)
    tichNgayDongChi = TichNgayTuJD(jdDongChi)
    soNgayDongChiTrong60 = SoNgayCanChi(tichNgayDongChi)+1
    aGiapTy = 1-soNgayDongChiTrong60
    aKyMao = 16-soNgayDongChiTrong60
    aGiapNgo = 31 - soNgayDongChiTrong60
    aKyDau = 46 - soNgayDongChiTrong60
    mang = [aGiapTy, aGiapNgo, aKyDau, aKyMao]
    arra = [abs(aGiapTy), abs(aGiapNgo), abs(aKyDau), abs(aKyMao)]
    min = arra[0]
    b = 0
    for i in range(len(arra)):
        if(arra[i] < min):
            min = arra[i]
    for i in range(len(arra)):
        if(arra[i] == min):
            b = i
    addit = mang[b]
    return tichNgayDongChi + addit


def PhuDauDuongNamSauDeDatNhuan(nam, thang, ngay, gio, phut, muiGio):
    namTinh = NamThaiAt(nam, thang, ngay, gio, phut, muiGio)
    jdDongChi = JDDongChi(namTinh, muiGio)
    tichNgayDongChi = TichNgayTuJD(jdDongChi)
    soNgayDongChiTrong60 = SoNgayCanChi(tichNgayDongChi)
    aGiapTy = 1-soNgayDongChiTrong60
    aKyMao = 16 - soNgayDongChiTrong60
    aGiapNgo = 31-soNgayDongChiTrong60
    aKyDau = 46 - soNgayDongChiTrong60
    mang = [aGiapTy, aGiapNgo, aKyDau, aKyMao]
    b = 0
    arr = [abs(aGiapTy), abs(aGiapNgo), abs(aKyDau), abs(aKyMao)]
    min = arr[0]
    for i in range(len(arr)):
        if(arr[i] < min):
            min = arr[i]
    for i in range(len(arr)):
        if(arr[i] == min):
            b = i
    add = mang[b]
    return tichNgayDongChi + add


def KiemTraNhuanDonGiap(nam, thang, ngay, gio, phut, muiGio):
    phuDauDuongNamNay = TichNgayPhuDauDuongCucDonGiap(
        nam, thang, ngay, gio, phut, muiGio)
    phuDauAmNamNay = TichNgayPhuDauAmCucDonGiap(
        nam, thang, ngay, gio, phut, muiGio)
    phuDauDuongNamSau = PhuDauDuongNamSauDeDatNhuan(
        nam, thang, ngay, gio, phut, muiGio)
    ketQua = ''
    if (phuDauAmNamNay - phuDauDuongNamNay > 180):
        ketQua = 'Nhuận Mang chủng'
    elif(phuDauDuongNamSau - phuDauAmNamNay > 180):
        ketQua = 'Nhuận Đại tuyết'
    else:
        ketQua = 'Không nhuận'
    return ketQua


def TichNgayPhuDauAmCucDonGiap(nam, thang, ngay, gio, phut, muiGio):
    namTinh = NamThaiAt(nam, thang, ngay, gio, phut, muiGio)
    jdHaChi = JDHaChi(namTinh, muiGio)
    tichNgayHaChi = TichNgayTuJD(jdHaChi)
    soNgayHaChiTrong60 = SoNgayCanChi(tichNgayHaChi)+1
    aGiapTy = 1 - soNgayHaChiTrong60
    aKyMao = 16-soNgayHaChiTrong60
    aGiapNgo = 31-soNgayHaChiTrong60
    aKyDau = 46 - soNgayHaChiTrong60
    mang = [aGiapTy, aGiapNgo, aKyDau, aKyMao]
    b = 0
    add = 0
    arr = [abs(aGiapTy), abs(aGiapNgo), abs(aKyDau), abs(aKyMao)]
    min = arr[0]
    for i in range(len(arr)):
        if(arr[i] < min):
            min = arr[i]
    for i in range(len(arr)):
        if(arr[i] == min):
            b = i
    add = mang[b]
    return tichNgayHaChi+add


def TinhTuanGiapVaCanTang(can, chi):
    ketQua = ['', '']
    canChi = can + " " + chi
    stt = LS.DanhSach60CanChi.index(canChi)
    if(stt < 10):
        ketQua[0] = 'TÝ'
        ketQua[1] = 'MẬU'
    elif ((stt >= 10) and (stt < 20)):
        ketQua[0] = 'TUẤT'
        ketQua[1] = 'KỶ'
    elif ((stt >= 20) and (stt < 30)):
        ketQua[0] = 'THÂN'
        ketQua[1] = 'CANH'
    elif ((stt >= 30) and (stt < 40)):
        ketQua[0] = 'NGỌ'
        ketQua[1] = 'TÂN'
    elif ((stt >= 40) and (stt < 50)):
        ketQua[0] = 'THÌN'
        ketQua[1] = 'NHÂM'
    elif ((stt >= 50) and (stt < 60)):
        ketQua[0] = 'DẦN'
        ketQua[1] = 'QUÝ'
    return ketQua


def NguHanhNapAm(can, chi):
    canChi = can + " " + chi
    return LS.NguHanhNapAmTuongUngCanChi[LS.DanhSach60CanChi.index(canChi)]

# endregion
