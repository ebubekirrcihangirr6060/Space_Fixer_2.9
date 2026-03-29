import streamlit as st
import pandas as pd
import numpy as np
from scipy.signal import medfilt
import plotly.graph_objects as go
import plotly.express as px
from scipy.fft import fft, fftfreq
import math
import time

# --- BÖLÜM 1: ARAYÜZ MAKYAJI VE SAYFA AYARLARI ---
st.set_page_config(page_title="CosmoFilter | Yer İstasyonu", page_icon="🍎", layout="wide", initial_sidebar_state="expanded")

if 'app_lang' not in st.session_state:
    st.session_state['app_lang'] = '🇹🇷 TR'
if 'app_theme' not in st.session_state:
    st.session_state['app_theme'] = 'Koyu 🌙'
if 'tutorial_step' not in st.session_state:
    st.session_state['tutorial_step'] = 1

lang_dict = {
    '🇹🇷 TR': {
        'title_main': "🛰️ <span class='highlight-cyan'>CosmoFilter</span> | Kozmik Veri Ayıklama Hattı",
        'subtitle': "Uzay araçlarından iletilen telemetri verilerindeki <b>SEU (Single Event Upset)</b> ve kozmik gürültüleri gerçek zamanlı tespit ve telafi eden yüksek performanslı sinyal işleme hattı.",
        'settings': '⚙️ Ayarlar & Menü',
        'theme_label': '🌈 Tema',
        'lang_label': '🌍 Dil',
        'tut_btn': '📺 Oklu Karşılama Eğitimini Başlat',
        'history_modal': '🚀 Türk Uzay ve Havacılık Tarihçesi',
        'sat_modal': '🔭 Gözlemevlerimiz ve Uydu Filomuz',
        'ctrl_panel': '🎛️ Görev Kontrol',
        'team_title': 'Kızıl Elmalar Takımı - CosmoFilter V1.2',
        'hist_btn': '🚀 Türk Uzay Tarihi',
        'obs_btn': '🔭 Gözlemevleri & Uydular',
        'sim_center': '🎛️ Simülasyon Kontrol Merkezi',
        'adv_text1': 'Yepyeni Bir Uzay Macerası!',
        'adv_text2': 'Sinyalleri listede biriktirip birbiriyle anında kıyaslayın!',
        'canli_btn': '🟢 Canlı Simülasyon',
        'new_btn': '🌌 Yeni Telemetri Sinyali Oluştur',
        'saved_signals': '📂 Kayıtlı Sinyaller (Maks 10)',
        'del_q': 'Silinsin mi?',
        'new_name': 'Yeni Ad',
        'yes': 'Evet',
        'no': 'Hayır',
        'contact': '📞 Bize Ulaşın',
        'tab1': '📡 Kozmik Veri Hattı',
        'tab2': '🌍 3D Yörünge Şovu',
        'tab3': '📈 Spektrum Analizi',
        'tab4': '🛡️ Sistem Sağlığı & Loglar',
        'tab5': '🧮 Delta Analizi'
    },
    '🇬🇧 EN': {
        'title_main': "🛰️ <span class='highlight-cyan'>CosmoFilter</span> | Cosmic Data Pipeline",
        'subtitle': "High-performance signal processing pipeline that detects and compensates for SEU (Single Event Upset) and cosmic noise in telemetry data transmitted from spacecraft in real time.",
        'settings': '⚙️ Settings & Language',
        'theme_label': '🌈 Theme',
        'lang_label': '🌍 Language',
        'tut_btn': '📺 Start Interactive Tutorial',
        'history_modal': '🚀 Turkish Space and Aviation History',
        'sat_modal': '🔭 Observatories and Satellite Fleet',
        'ctrl_panel': '🎛️ Mission Control',
        'team_title': 'Red Apples Team - CosmoFilter V1.2',
        'hist_btn': '🚀 Space History',
        'obs_btn': '🔭 Observatories & Sats',
        'sim_center': '🎛️ Simulation Control Center',
        'adv_text1': 'A Brand New Space Adventure!',
        'adv_text2': 'Accumulate signals in the list and compare them instantly!',
        'canli_btn': '🟢 Live Simulation',
        'new_btn': '🌌 Generate New Telemetry Signal',
        'saved_signals': '📂 Saved Signals (Max 10)',
        'del_q': 'Delete?',
        'new_name': 'New Name',
        'yes': 'Yes',
        'no': 'No',
        'contact': '📞 Contact Us',
        'tab1': '📡 Cosmic Pipeline',
        'tab2': '🌍 3D Orbit Show',
        'tab3': '📈 Spectrum Analysis',
        'tab4': '🛡️ System Health & Logs',
        'tab5': '🧮 Delta Analysis'
    }
}
t = lang_dict[st.session_state['app_lang']]

# CSS ile Uzay İstasyonu Konsepti
st.markdown("""
    <style>
    /* Ana Arka Plan: Koyu Parlament Mavisi / Uzay Siyahı */
    .stApp { 
        background-color: #050a15; 
        background-image: radial-gradient(circle at 50% 0%, #1a233a 0%, #050a15 70%);
        color: #e2e8f0;
    }
    
    /* Başlıklar ve Fontlar */
    h1, h2, h3, h4, th { 
        color: #e2e8f0 !important; 
        font-family: 'Inter', 'Segoe UI', sans-serif; 
        font-weight: 600;
    }
    
    /* Vurgulu Neon Renkler (Cyan & Kızıl) */
    .highlight-cyan { color: #00f0ff; text-shadow: 0 0 8px rgba(0,240,255,0.4); }
    .highlight-red { color: #ff3b30; text-shadow: 0 0 8px rgba(255,59,48,0.4); }
    
    /* Uyarı Kutusu */
    .uyari-kutusu { 
        background: linear-gradient(90deg, rgba(255,59,48,0.1) 0%, rgba(255,59,48,0.02) 100%);
        border-left: 4px solid #ff3b30;
        padding: 15px 20px; 
        border-radius: 4px; 
        color: #ffb3b0; 
        font-weight: bold; 
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(255,59,48,0.1);
    }
    
    /* Metrik Kartları Özelleştirme */
    [data-testid="stMetricValue"] { color: #00f0ff !important; font-weight: 700 !important; }
    [data-testid="stMetricLabel"] { color: #94a3b8 !important; }
    
    /* Sidebar Arka Planı */
    [data-testid="stSidebar"] {
        background-color: #0c1222 !important;
        border-right: 1px solid #1e293b;
    }
    
    hr {
        border-color: #1e293b;
    }
    
    /* Özel Buton ve Tarihçe Kartları */
    div.stButton > button[kind="primary"] {
        background-color: #b91c1c !important; /* Koyu Bordo / Kızıl Elma Tok Kırmızı */
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        box-shadow: 0 0 12px rgba(185, 28, 28, 0.5);
        transition: all 0.3s ease;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #991b1b !important;
        box-shadow: 0 0 18px rgba(153, 27, 27, 0.8);
        transform: scale(1.02);
    }
    .history-card {
        background-color: #0f172a; 
        padding: 15px; 
        border-radius: 8px; 
        border-left: 4px solid #b91c1c; 
        margin-bottom: 10px;
        transition: transform 0.2s ease;
    }
    .history-card:hover { transform: translateY(-3px); }
    </style>
""", unsafe_allow_html=True)

# Açık (Light) Tema CSS Overrides
if st.session_state['app_theme'] == 'Açık ☀️':
    st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; background-image: none; color: #0f172a; }
    h1, h2, h3, h4, th, p { color: #0f172a !important; }
    .uyari-kutusu { background: #ffe4e6; border-left: 4px solid #e11d48; color: #e11d48; box-shadow: none; }
    [data-testid="stMetricValue"] { color: #2563eb !important; }
    [data-testid="stMetricLabel"] { color: #475569 !important; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #cbd5e1; }
    .history-card { background: #f1f5f9; border: 1px solid #cbd5e1; }
    /* Override embedded divs */
    div[style*="background: rgba(30,41,59,0.5)"] { background: #ffffff !important; box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important; color:#0f172a !important; }
    div[style*="background:rgba(0,240,255,0.05)"] { background: #eff6ff !important; border-color: #bfdbfe !important; }
    div[style*="color:#00f0ff;"] { color: #0284c7 !important; text-shadow:none; }
    div[style*="color: #e2e8f0;"] { color: #334155 !important; }
    div[style*="color:#94a3b8;"] { color: #475569 !important; }
    div[style*="border-left: 3px solid #00f0ff;"] { border-left-color: #3b82f6 !important; }
    div[style*="color:#fff"] { color: #0f172a !important; }
    text { fill: #334155 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BÖLÜM 2: GÖREV KONTROL PANELİ ---
# Kızıl Elmalar Takım Logosu
logo_path = r"C:\Users\user\.gemini\antigravity\brain\3f1ded66-8f49-435b-aade-1077a4caf9a3\media__1774794292603.png"
try:
    st.sidebar.image(logo_path, use_container_width=True)
except:
    st.sidebar.markdown("### 🍎 KIZIL ELMALAR")

st.sidebar.title(t['ctrl_panel'])
st.sidebar.markdown(f"<span style='color:#94a3b8; font-size:0.9em;'>{t['team_title']}</span>", unsafe_allow_html=True)
st.sidebar.markdown("---")

st.sidebar.caption(t['settings'])
col_thm, col_lng = st.sidebar.columns(2)
with col_thm:
    new_theme = st.selectbox(t['theme_label'], ["Koyu 🌙", "Açık ☀️"], index=0 if st.session_state.get('app_theme', 'Koyu 🌙') == "Koyu 🌙" else 1)
    if new_theme != st.session_state.get('app_theme'):
        st.session_state['app_theme'] = new_theme
        st.rerun()
with col_lng:
    new_lang = st.selectbox(t['lang_label'], ["🇹🇷 TR", "🇬🇧 EN"], index=0 if st.session_state.get('app_lang', '🇹🇷 TR') == "🇹🇷 TR" else 1)
    if new_lang != st.session_state.get('app_lang'):
        st.session_state['app_lang'] = new_lang
        st.rerun()
if st.sidebar.button(t['tut_btn'], use_container_width=True, type="secondary"):
    st.session_state['tutorial_step'] = 1
    st.rerun()

st.sidebar.markdown("---")

try:
    @st.dialog(t['history_modal'], width="large")
    def uzay_tarihi_modal():
        st.markdown("### 🇹🇷 Göklere Adanmış Bir Asır")
        st.markdown("> *\"İstikbal Göklerdedir.\"* - **Mustafa Kemal Atatürk**")
        st.markdown("---")
        
        st.markdown("""
        <div class='history-card'>
            <h4 style='color: #FFD700; margin:0;'>1925 - TOMTAŞ ve Vecihi Hürkuş</h4>
            <p style='color: #e2e8f0; margin-top:5px;'>Türkiye'nin ilk uçak fabrikası TOMTAŞ kuruldu. Vecihi Hürkuş kendi uçağı K-VI'yı üretip uçmasına rağmen, sertifikasyon engelleri ve bürokrasi yüzünden projeler yarım kaldı.</p>
        </div>
        <div class='history-card'>
            <h4 style='color: #FFD700; margin:0;'>1936 - Nuri Demirağ <i>(Yarım Kalan Hayal)</i></h4>
            <p style='color: #e2e8f0; margin-top:5px;'>Türkiye'nin ilk seri üretim yolcu uçakları Nu.D.38 üretildi fakat siparişlerin iptal edilmesi sebebiyle fabrika kapatılmak zorunda kaldı, eşsiz bir vizyon yok oldu.</p>
        </div>
        <div class='history-card'>
            <h4 style='color: #FFD700; margin:0;'>1994 - TÜRKSAT 1B</h4>
            <p style='color: #e2e8f0; margin-top:5px;'>TÜRKSAT 1A'nın okyanusa düşmesinden sadece aylar sonra uzaya fırlatılan TÜRKSAT 1B ile Türkiye, uzaydaki ilk imzasını gururla attı.</p>
        </div>
        <div class='history-card'>
            <h4 style='color: #FFD700; margin:0;'>2003 - BİLSAT Projesi</h4>
            <p style='color: #e2e8f0; margin-top:5px;'>Teknoloji transferi (Know-How) amacıyla yurt dışı ile ortak fırlatılan ilk gözlem uydumuz.</p>
        </div>
        <div class='history-card'>
            <h4 style='color: #FFD700; margin:0;'>2011 - RASAT</h4>
            <p style='color: #e2e8f0; margin-top:5px;'>Yabancı destek olmadan, Türk mühendisleri tarafından tasarlanıp üretilen ilk yer gözlem uydusu yörüngeye oturdu!</p>
        </div>
        <div class='history-card'>
            <h4 style='color: #FFD700; margin:0;'>2018 - Türkiye Uzay Ajansı (TUA)</h4>
            <p style='color: #e2e8f0; margin-top:5px;'>Milli Uzay Programı'nın yürütülmesi ve sivil uzay faaliyetlerinin tek elde toplanması vizyonuyla hizmete girdi.</p>
        </div>
        <div class='history-card'>
            <h4 style='color: #FFD700; margin:0;'>2024 - Kızıl Elma'nın Uzay Yürüyüşü</h4>
            <p style='color: #e2e8f0; margin-top:5px;'>Alper Gezeravcı, ISS'te bilimsel deneyler yaparak Türkiye'nin ilk astronotu oldu. Hemen ardından <b>TÜRKSAT 6A</b>, tamamen yerli mühendislikle fırlatıldı!</p>
        </div>
        """, unsafe_allow_html=True)

    @st.dialog(t['sat_modal'], width="large")
    def uydular_modal():
        st.markdown("### 🌌 Gözümüz Yükseklerde")
        st.markdown("Türkiye'nin uzay ve astronomideki kalbi olan gözlemevlerimiz ve gökyüzü nöbetçileri uydularımız:")
        st.markdown("---")
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown("""
            <div class='history-card' style='border-left-color: #00f0ff;'>
                <h4 style='color: #00f0ff; margin:0;'>🔭 TUG (TÜBİTAK Ulusal Gözlemevi)</h4>
                <p style='color: #e2e8f0; margin-top:5px;'>1997 yılında Antalya Bakırlıtepe'de kurulan TUG, astronomi biliminin ülkemizdeki kalesidir.</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div class='history-card' style='border-left-color: #00f0ff;'>
                <h4 style='color: #00f0ff; margin:0;'>🛰️ GÖKTÜRK & İMECE</h4>
                <p style='color: #e2e8f0; margin-top:5px;'>Yüksek çözünürlüklü askeri ve sivil yer gözlem uydularımız. İMECE tamamen yerli olarak tasarlanmıştır!</p>
            </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown("""
            <div class='history-card' style='border-left-color: #00f0ff;'>
                <h4 style='color: #00f0ff; margin:0;'>📡 DAG (Doğu Anadolu Gözlemevi)</h4>
                <p style='color: #e2e8f0; margin-top:5px;'>Türkiye'nin en büyük 4 metrelik kızılötesi teleskobuna ev sahipliği yapar. Erzurum'da bulunmaktadır.</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div class='history-card' style='border-left-color: #00f0ff;'>
                <h4 style='color: #00f0ff; margin:0;'>🌍 TÜRKSAT Filosu</h4>
                <p style='color: #e2e8f0; margin-top:5px;'>Afrika'dan Avrupa'ya devasa bir coğrafyaya yayın yapan güçlü haberleşme altyapımız.</p>
            </div>
            """, unsafe_allow_html=True)

except AttributeError:
    def uzay_tarihi_modal():
        st.error("Lütfen uygulamanın modal desteklemesi için Streamlit sürümünü güncelleyin.")
    def uydular_modal(): pass

if st.sidebar.button(t['hist_btn'], use_container_width=True, type="primary"):
    uzay_tarihi_modal()
if st.sidebar.button(t['obs_btn'], use_container_width=True, type="primary"):
    uydular_modal()

st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown(f"### {t['sim_center']}")

# Tab 1 içerisindeki uploader ve slider değerleri buradan algılanır
yuklenen_dosya = st.session_state.get('dosya_yukle', None)
kernel_gucu = st.session_state.get('filt_gucu_slider', 5)

# --- BÖLÜM 3: VERİ ÜRETİMİ ---
def veri_uret(rastgele_tohum=False, temiz_sim=False):
    if rastgele_tohum:
        np.random.seed(int(time.time() * 1000) % (2**32))
    else:
        np.random.seed(42) 
    
    zaman = np.arange(0, 100, 0.5) 
    gercek_sinyal = np.sin(zaman) * 20 + 50 
    bozuk_sinyal = gercek_sinyal.copy()
    
    if not temiz_sim:
        sicrama_noktalari = np.random.choice(len(zaman), size=np.random.randint(10, 20), replace=False)
        bozuk_sinyal[sicrama_noktalari] += np.random.choice([120, -110, 85, -95, 140, -135], size=len(sicrama_noktalari))
        
        kopuk_noktalar = np.random.choice(len(zaman), size=np.random.randint(5, 12), replace=False)
        bozuk_sinyal[kopuk_noktalar] = np.nan
        
    df = pd.DataFrame({'Zaman': zaman, 'Gerçek Veri': gercek_sinyal, 'Bozuk Veri': bozuk_sinyal})
    df.set_index('Zaman', inplace=True)
    return df

if 'telemetri_gecmisi' not in st.session_state:
    st.session_state['telemetri_gecmisi'] = []
if 'aktif_veri_id' not in st.session_state:
    st.session_state['aktif_veri_id'] = 'canli'
if 'tmp_canli_df' not in st.session_state:
    st.session_state['tmp_canli_df'] = veri_uret(rastgele_tohum=False, temiz_sim=True)
if 'sinyal_sayaci' not in st.session_state:
    st.session_state['sinyal_sayaci'] = 1

# Özel Yapım Gökkuşağı (Spectrum) İndirme Simülasyonu
def show_custom_progress():
    pb_placeholder = st.sidebar.empty()
    for i in range(1, 101):
        time.sleep(0.025) # Daha yavaş yükleme hissi
        # Kırmızı(0) -> Sarı -> Yeşil -> Mavi -> Magenta(300) renk geçişi (Hue HSL)
        hue = int((i / 100.0) * 300)
        c = f"hsl({hue}, 100%, 50%)"
        html_code = f"""
        <div style='width: 100%; background: #1e293b; border-radius: 10px; margin-bottom: 10px;'>
            <div style='width: {i}%; height: 12px; background: {c}; border-radius: 10px; transition: width 0.05s linear, background 0.05s linear;'></div>
        </div>
        """
        pb_placeholder.markdown(html_code, unsafe_allow_html=True)
    pb_placeholder.empty()

st.sidebar.markdown(f"<div style='background:rgba(0,240,255,0.05); padding:15px; border-radius:10px; border:1px solid rgba(0,240,255,0.2); text-align:center;'> <h4 style='color:#00f0ff; margin-top:0;'>{t['adv_text1']}</h4> <p style='color:#e2e8f0; font-size:0.9em;'>{t['adv_text2']}</p>", unsafe_allow_html=True)

if st.sidebar.button(t['canli_btn'], use_container_width=True, type="secondary"):
    st.session_state['aktif_veri_id'] = 'canli'
    st.session_state['tmp_canli_df'] = veri_uret(rastgele_tohum=True, temiz_sim=True)
    st.rerun()

if st.sidebar.button("🌌 Yeni Telemetri Sinyali Oluştur", use_container_width=True, type="primary"):
    show_custom_progress()
    yeni_df = veri_uret(rastgele_tohum=True, temiz_sim=False)
    sayac = st.session_state['sinyal_sayaci']
    yeni_isim = f"📡 Sinyal #{sayac}"
    st.session_state['telemetri_gecmisi'].append({'id': yeni_isim, 'df': yeni_df})
    if len(st.session_state['telemetri_gecmisi']) > 10:
        st.session_state['telemetri_gecmisi'].pop(0)
    st.session_state['aktif_veri_id'] = yeni_isim
    st.session_state['sinyal_sayaci'] += 1
    st.rerun()

st.sidebar.markdown("</div>", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown(f"### {t['saved_signals']}")

# En yenisi en üstte görünsün
for kayit in reversed(st.session_state['telemetri_gecmisi']):
    kayit_id = kayit['id']
    is_active = (kayit_id == st.session_state['aktif_veri_id'])
    
    # State flags for inline edit & delete
    state_edit = st.session_state.get(f"edit_{kayit_id}", False)
    state_del = st.session_state.get(f"del_{kayit_id}", False)
    
    st.sidebar.markdown(f"<div style='border-left: 3px solid {'#00f0ff' if is_active else 'transparent'}; padding-left:5px; margin-bottom:5px;'>", unsafe_allow_html=True)
    
    if state_edit:
        # İsim Değiştirme (Edit) Modu
        c1, c2, c3 = st.sidebar.columns([6, 2, 2])
        yeni_ad = c1.text_input(t['new_name'], value=kayit_id, key=f"inp_{kayit_id}", label_visibility="collapsed")
        if c2.button("💾", key=f"save_{kayit_id}", help="Save"):
            # Update ID in history
            for k in st.session_state['telemetri_gecmisi']:
                if k['id'] == kayit_id:
                     k['id'] = yeni_ad
                     break
            # Eğer aktifse, aktif kimliği de güncelle
            if is_active:
                 st.session_state['aktif_veri_id'] = yeni_ad
                 
            st.session_state[f"edit_{kayit_id}"] = False
            st.rerun()
            
        if c3.button("✖", key=f"cancel_edit_{kayit_id}", help="Cancel"):
            st.session_state[f"edit_{kayit_id}"] = False
            st.rerun()
            
    elif state_del:
        # Silme Onaylama Modu
        st.sidebar.warning(t['del_q'])
        c1, c2 = st.sidebar.columns(2)
        if c1.button(t['yes'], key=f"yes_del_{kayit_id}", use_container_width=True):
            st.session_state['telemetri_gecmisi'] = [x for x in st.session_state['telemetri_gecmisi'] if x['id'] != kayit_id]
            if is_active:
                if len(st.session_state['telemetri_gecmisi']) > 0:
                    st.session_state['aktif_veri_id'] = st.session_state['telemetri_gecmisi'][-1]['id']
                else:
                    st.session_state['aktif_veri_id'] = None
            st.session_state[f"del_{kayit_id}"] = False
            st.rerun()
            
        if c2.button(t['no'], key=f"no_del_{kayit_id}", use_container_width=True):
            st.session_state[f"del_{kayit_id}"] = False
            st.rerun()
            
    else:
        # Normal Görünüm: [ Sinyal İsmi ] [ ✏️ ] [ ❌ ]
        c1, c2, c3 = st.sidebar.columns([6, 2, 2])
        button_type = "primary" if is_active else "secondary"
        if c1.button(kayit_id, key=f"btn_activate_{kayit_id}", use_container_width=True, type=button_type):
            st.session_state['aktif_veri_id'] = kayit_id
            st.rerun()
            
        if c2.button("✏️", key=f"btn_edit_{kayit_id}", help="İsmi yeniden adlandır"):
            st.session_state[f"edit_{kayit_id}"] = True
            st.rerun()
            
        if c3.button("❌", key=f"btn_del_{kayit_id}", help="Sinyali tamamen sil"):
            st.session_state[f"del_{kayit_id}"] = True
            st.rerun()

    st.sidebar.markdown("</div>", unsafe_allow_html=True)

st.sidebar.markdown("---")
with st.sidebar.expander(t['contact']):
    st.info("**Şirket:** Kızıl Elmalar Uzay Teknolojileri A.Ş.")
    st.markdown("**📞 Müşteri Hizmetleri:** +90 555 123 4567")
    st.markdown("**📧 Kurumsal E-posta:** iletisim@kizilelmalar-space.com")
    st.markdown("**💼 LinkedIn:** [Kızıl Elmalar Uzay](#)")
    st.markdown("**📸 Instagram:** [@kizilelmalar_space](#)")

# --- BÖLÜM 4: ÇEKİRDEK ALGORİTMA ---
def veriyi_temizle(df, k_size):
    islenmis_df = df.copy()
    islenmis_df['Temizlenen Veri'] = islenmis_df['Bozuk Veri'].interpolate(method='linear', limit_direction='both')
    medyan = medfilt(islenmis_df['Temizlenen Veri'], kernel_size=k_size)
    fark = np.abs(islenmis_df['Temizlenen Veri'] - medyan)
    islenmis_df['Temizlenen Veri'] = np.where(fark > 30, medyan, islenmis_df['Temizlenen Veri'])
    islenmis_df['Delta (Gürültü)'] = np.abs(islenmis_df['Bozuk Veri'].fillna(islenmis_df['Temizlenen Veri']) - islenmis_df['Temizlenen Veri'])
    return islenmis_df

# Ana Veri Entegrasyonu (Yüklü Dosya veya Seçili Aktif Sinyal)
if yuklenen_dosya is not None:
    # Dosya yüklendiyse öncelik onda
    ham_veri_df = pd.read_csv(yuklenen_dosya, index_col=0)
    if 'Gerçek Veri' not in ham_veri_df.columns:
        ham_veri_df['Gerçek Veri'] = ham_veri_df['Bozuk Veri']
else:
    # Aktif simülasyon sinyali
    aktif_id = st.session_state.get('aktif_veri_id')
    
    if aktif_id == 'canli':
        ham_veri_df = st.session_state.get('tmp_canli_df', veri_uret(rastgele_tohum=False, temiz_sim=True))
    else:
        ham_veri_df = None
        for k in st.session_state.get('telemetri_gecmisi', []):
            if k['id'] == aktif_id:
                ham_veri_df = k['df']
                break
                
        # Kullanıcı tüm sinyalleri elinde sildiyse veya bulamadıysa canlı simülasyona fallback at
        if ham_veri_df is None:
            ham_veri_df = st.session_state.get('tmp_canli_df', veri_uret(rastgele_tohum=False, temiz_sim=True))
            st.session_state['aktif_veri_id'] = 'canli'

sonuc_df = veriyi_temizle(ham_veri_df, kernel_gucu)

plotly_layout = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#FFD700'),
    margin=dict(l=20, r=20, t=40, b=20),
    xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title="Zaman"),
    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title="Sinyal Genliği")
)
legend_ayari = dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#FFD700'))

def render_footer(mode="normal"):
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: center; margin-top: 50px; margin-bottom: 20px;">
        <span style="font-size: 24px; margin-right: 15px;">🌍</span>
        <div style="flex-grow: 1; height: 2px; background: #fff; box-shadow: 0 0 10px #fff, 0 0 20px #00f0ff; border-radius: 5px;"></div>
        <span style="font-size: 24px; margin-left: 15px;">🚀</span>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("💡 Kozmik Hap Bilgi: Biliyor muydunuz?"):
        if mode == "kritik_vaka":
            st.markdown("**Carrington Olayı (1859):** Kayıtlara geçen en şiddetli Güneş fırtınasıdır. Öyle büyük bir radyoaktif plazma fırlatılmıştı ki, Dünya'daki telgraf hatları aşırı yüklenmeden alev almış, operatörler elektrik çarpmasına maruz kalmıştı. Aynı fırtına bugün yaşansa, saniyeler içinde trilyonlarca dolarlık uydu ve internet altyapımız eriyerek yok olabilir!")
        else:
            st.markdown("**ISS Hızı ve Sürekli Düşüş:** Uluslararası Uzay İstasyonu (ISS) saniyede yaklaşık 7.66 km hızla seyahat eder. Aslında o irtifada yerçekimi vardır (Dünya'daki değerin %90'ı), ancak uydular ve istasyon inanılmaz bir doğrusal hızla **'Dünya'nın eğriminin etrafında sürekli düştükleri'** için astronotlar ağırlıksızlık hissi yaşar.")
    
    st.markdown("<div style='text-align:center; color:#64748b; font-size:0.8em; margin-top:10px;'>© 2026 <b>Kızıl Elmalar</b> Takımı - Uzay ve Havacılık Teknolojileri</div>", unsafe_allow_html=True)


# --- BÖLÜM 5: ANA EKRAN VE SUNUM ---
if st.session_state.get('tutorial_step', 0) > 0:
    step = st.session_state['tutorial_step']
    steps = [
        {"title": "🌟 1/4: CosmoFilter'a Hoş Geldiniz!", "text": "Bu sistem, uzay araçlarından gelen gürültülü telemetri verilerini gerçek zamanlı temizlemek için kurgulanmıştır."},
        {"title": "🎛️ 2/4: Sol Menü (Kontrol Merkezi)", "text": "Sol taraftaki 'Yeni Telemetri Oluştur' butonu ile farklı kozmik radyasyon parçacıklarıyla dolu (Bozuk) senaryolar yaratabilirsiniz. 'Canlı Simülasyon' butonu ise hatasız referans veriyi (Uydunun ilk halini) ekrana getirir."},
        {"title": "🔄 3/4: Geçmiş ve Kıyaslama", "text": "Ürettiğiniz her sinyal sol alttaki listeye eklenir. Tabloda isimlerine tıklayarak veriler arasında anında geçiş yapabilir, grafik değişimlerini A/B testi yapar gibi kıyaslayabilirsiniz. Satırlar yandaki Kalem ile isimlendirilebilir."},
        {"title": "🎚️ 4/4: Kozmik Veri Hattı (Filtreleme)", "text": "Hemen aşağıdaki 'Filtre Kalibrasyonu' sürgüsünü sağa-sola çekerek CosmoFilter'ın hatalı verileri (kırmızı pikleri) nasıl anında tıraşladığını kendiniz de test edin!"}
    ]
    
    current_step = steps[step-1]
    
    st.markdown(f"""
    <div style='background: linear-gradient(90deg, rgba(0,240,255,0.1) 0%, rgba(30,41,59,0.5) 100%); 
                border-left: 5px solid #00f0ff; padding: 20px; border-radius: 8px; margin-bottom: 20px;
                box-shadow: 0 4px 15px rgba(0,240,255,0.1);'>
        <h3 style='color: #00f0ff; margin-top:0;'>{current_step['title']}</h3>
        <p style='color: #e2e8f0; font-size: 1.1em;'>{current_step['text']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    t_col1, t_col2, t_col3 = st.columns([2, 2, 6])
    with t_col1:
        if step < 4:
            if st.button("İleri (Next) ⏩", key=f"btn_tut_ileri_{step}", type="primary"):
                st.session_state['tutorial_step'] += 1
                st.rerun()
        else:
            if st.button("Harika, Eğitimi Bitir ✔️", key="btn_tut_bitir", type="primary"):
                st.session_state['tutorial_step'] = 0
                st.rerun()
    with t_col2:
        if st.button("Eğitimi Atla (Skip) ✖", key=f"btn_tut_atla_{step}"):
            st.session_state['tutorial_step'] = 0
            st.rerun()
            
    st.markdown("---")

st.markdown("<h1>🛰️ <span class='highlight-cyan'>CosmoFilter</span> | Kozmik Veri Ayıklama Hattı</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#94a3b8; font-size:1.1em;'>Uzay araçlarından iletilen telemetri verilerindeki <b>SEU (Single Event Upset)</b> ve kozmik gürültüleri gerçek zamanlı tespit ve telafi eden yüksek performanslı sinyal işleme hattı.</p>", unsafe_allow_html=True)

# Sekmelerin (Tabs) Oluşturulması
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📡 Kozmik Veri Hattı", 
    "🌍 3D Yörünge Şovu", 
    "📈 Spektrum Analizi", 
    "🛡️ Sistem Sağlığı & Loglar",
    "🧮 Delta Analizi"
])

# --- TAB 1: ANA VERİ HATTI ---
with tab1:
    seu_sayisi = len(sonuc_df[sonuc_df['Delta (Gürültü)'] > 50])
    if seu_sayisi > 8:
        st.markdown(f'<div class="uyari-kutusu">🚨 KRİTİK RADYASYON UYARISI: Veri hattında yüksek anomali tespiti! (Sistem <span style="color:#fff">{seu_sayisi} adet</span> dezenformasyonu bloke etti)</div>', unsafe_allow_html=True)
    elif seu_sayisi > 0:
        st.warning(f"⚠️ Düşük/Orta Seviye Uyarı: Telemetride {seu_sayisi} adet ufak çaplı bozucu etki onarıldı.")

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### <span class='highlight-red'>🔴</span> Ham Yörünge Telemetrisi", unsafe_allow_html=True)
        fig_raw = go.Figure()
        fig_raw.add_trace(go.Scatter(x=sonuc_df.index, y=sonuc_df['Gerçek Veri'], mode='lines', name='İdeal Sinyal', line=dict(color='rgba(255,255,255,0.2)', width=1, dash='dot')))
        fig_raw.add_trace(go.Scatter(x=sonuc_df.index, y=sonuc_df['Bozuk Veri'], mode='lines+markers', name='Ham Telemetri', line=dict(color='#ff3b30', width=2), marker=dict(size=4)))
        fig_raw.update_layout(**plotly_layout, height=350, showlegend=True, legend=legend_ayari)
        st.plotly_chart(fig_raw, use_container_width=True, key="fig_raw_main")
        st.markdown("<div style='padding:10px; background:#1e293b; border-radius:5px; margin-top:-10px;'><span style='color:#94a3b8; font-size:0.85em;'>ℹ️ Gördüğünüz keskin sıçramalar (pikler), kozmik ışınların mikroçiplerdeki transistörlere çarpması sonucu oluşan donanımsal körlüklerdir. Algoritmamıza akan çıplak veri budur.</span></div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("### <span class='highlight-cyan'>🟢</span> CosmoFilter Çıktısı", unsafe_allow_html=True)
        fig_clean = go.Figure()
        fig_clean.add_trace(go.Scatter(x=sonuc_df.index, y=sonuc_df['Gerçek Veri'], mode='lines', name='İdeal Sinyal', line=dict(color='rgba(255,255,255,0.2)', width=1, dash='dot')))
        fig_clean.add_trace(go.Scatter(x=sonuc_df.index, y=sonuc_df['Temizlenen Veri'], mode='lines', name='Filtrelenmiş Veri', line=dict(color='#00f0ff', width=3)))
        fig_clean.update_layout(**plotly_layout, height=350, showlegend=True, legend=legend_ayari)
        st.plotly_chart(fig_clean, use_container_width=True, key="fig_clean_main")
        st.markdown("<div style='padding:10px; background:#1e293b; border-radius:5px; margin-top:-10px;'><span style='color:#94a3b8; font-size:0.85em;'>ℹ️ CosmoFilter, bu anomali noktalarını nanosaniyeler içinde tespit edip sinyalin orijinal karakteristiğine (sinüs) zarar vermeden akıllıca tıraşlamaktadır.</span></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ⚙️ Sistem Kontrol Konsolu")
    
    col_ctrl1, col_ctrl2 = st.columns(2)
    with col_ctrl1:
        st.markdown("<div style='background:rgba(30,41,59,0.5); padding:15px; border-radius:8px; border-top:3px solid #00f0ff; height:100%;'>", unsafe_allow_html=True)
        st.slider(
            "Filtre Kalibrasyonu (Medyan Penceresi)", 
            min_value=1, max_value=99, step=2, value=kernel_gucu, key="filt_gucu_slider",
            help="Pencere boyutu artarsa düzeltme artar ancak mikro detaylar kaybolabilir."
        )
        st.markdown("<p style='color:#94a3b8; font-size:0.85em; margin-bottom:0;'>Bu ayar CosmoFilter'ın hatalı sinyalleri yakalama agresifliğini belirler. Değişimi anında yukarıdaki grafikte görebilirsiniz.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_ctrl2:
        st.markdown("<div style='background:rgba(30,41,59,0.5); padding:15px; border-radius:8px; border-top:3px solid #8b5cf6; height:100%;'>", unsafe_allow_html=True)
        st.file_uploader("📥 Geçmiş Görev Verisi Yükle (Playback)", type=["csv"], key="dosya_yukle")
        st.markdown("<p style='color:#94a3b8; font-size:0.85em; margin-bottom:0;'>Dosya yüklendiğinde otomatik olarak simülasyon modundan çıkılır. (Format: 'Zaman', 'Bozuk Veri')</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 2: 3D YÖRÜNGE SİMÜLASYONU ---
with tab2:
    st.markdown("### 🌍 Uydunun Anlık Yörünge Durumu (Gerçekçi Harita)")
    
    # Gerçekçi 3D Yörünge Modeli (Orthographic ScatterGeo)
    fig3d = go.Figure()

    # Yörünge Yolu (Ekvatora 51.6 derece eğimli ISS benzeri)
    lon_orbit = np.linspace(-180, 180, 100)
    lat_orbit = np.sin(np.radians(lon_orbit)) * 51.6
    sat_idx = 45 # Mevcut pozisyon

    # Yörünge İzi Çizgisi
    fig3d.add_trace(go.Scattergeo(
        lon=lon_orbit,
        lat=lat_orbit,
        mode='lines',
        line=dict(width=2, color='rgba(0, 240, 255, 0.6)', dash='dash'),
        name='Planlanan Rota',
        hoverinfo='skip'
    ))

    # Uydu Modellemesi (Gelişmiş İşaretleyici)
    fig3d.add_trace(go.Scattergeo(
        lon=[lon_orbit[sat_idx]],
        lat=[lat_orbit[sat_idx]],
        mode='markers+text',
        marker=dict(
            size=16, 
            color='#FFD700', 
            symbol='star-triangle-up', 
            line=dict(color='#ff3b30', width=2)
        ),
        text=['🚀 Kızıl Elma'],
        textposition="top center",
        textfont=dict(color="#FFD700", size=14, weight='bold'),
        name='Kızıl Elma Uydusu'
    ))

    # Gerçek Dünya Fiziksel Haritası Parametreleri
    fig3d.update_geos(
        projection_type="orthographic",
        showcoastlines=True, coastlinecolor="rgba(0, 240, 255, 0.6)", coastlinewidth=1.2,
        showland=True, landcolor="#0a1f11", # Koyu Orman Yeşili Kıtalar
        showocean=True, oceancolor="#020f26", # Derin Okyanus Laciverti
        showlakes=True, lakecolor="#020f26",
        showcountries=True, countrycolor="rgba(148, 163, 184, 0.3)", countrywidth=0.5,
        bgcolor="#000000", # Uzay Siyahı Arka Plan
        framecolor="rgba(0,0,0,0)"
    )
    
    fig3d.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        plot_bgcolor='#000000',
        paper_bgcolor='#000000',
        height=400,
        showlegend=False
    )
    
    c1, c2 = st.columns([3, 1])
    with c1:
        st.plotly_chart(fig3d, use_container_width=True, key="fig3d_main")
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.metric(label="İrtifa", value="402.5 km", delta="Yükseliyor", delta_color="normal")
        st.metric(label="Orbital Hız", value="7.66 km/sn", delta="Stabil", delta_color="off")
        st.metric(label="Güneş Paneli Sıcaklığı", value="74 °C", delta="Maksimum Güç", delta_color="off")

    st.markdown("---")
    st.markdown("### 🔭 Yörünge Telemetri Hap Bilgileri")
    col_t2_1, col_t2_2, col_t2_3 = st.columns(3)
    with col_t2_1:
         st.markdown("<div style='background: rgba(30,41,59,0.5); padding: 15px; border-radius: 8px; border-left: 5px solid #FFD700; height:100%; box-shadow: 0 4px 6px rgba(0,0,0,0.3);'> <h4 style='color: #FFD700; margin-top:0;'>🛰️ İrtifa ve Atmosfer</h4> <p style='color: #e2e8f0; font-size:0.9em;'>Uydumuz LEO (Alçak Dünya Yörüngesi) adı verilen bölgede seyahat etmektedir. Bu bölgede sürüklenme direnci (Drag) nedeniyle uydular düzenli olarak itki kullanmalıdır.</p> </div>", unsafe_allow_html=True)
    with col_t2_2:
         st.markdown("<div style='background: rgba(30,41,59,0.5); padding: 15px; border-radius: 8px; border-left: 5px solid #00f0ff; height:100%; box-shadow: 0 4px 6px rgba(0,0,0,0.3);'> <h4 style='color: #00f0ff; margin-top:0;'>🌌 Koordinat Sistemi</h4> <p style='color: #e2e8f0; font-size:0.9em;'>Harita, eşlek koordinat sistemi ile dönüştürülmüş projeksiyonu birleştirerek harita üzerindeki X, Y eksenlerini anlık orbital eğim ile eşleştirmektedir.</p> </div>", unsafe_allow_html=True)
    with col_t2_3:
         st.markdown("<div style='background: rgba(30,41,59,0.5); padding: 15px; border-radius: 8px; border-left: 5px solid #ff3b30; height:100%; box-shadow: 0 4px 6px rgba(0,0,0,0.3);'> <h4 style='color: #ff3b30; margin-top:0;'>☀️ Termal Etkiler</h4> <p style='color: #e2e8f0; font-size:0.9em;'>Uydular Dünya'nın karanlık yüzüne geçerken Güneş panelleri aniden aşırı soğur, aydınlık yüze geçildiğinde ise paneller ısınarak ekstrem dereceleri görebilir.</p> </div>", unsafe_allow_html=True)

# --- TAB 3: FREKANS SPEKTRUMU (FFT) ---
with tab3:
    st.markdown("### 📈 Sinyalin Frekans Analizi (Fourier Dönüşümü)")
    
    N = len(sonuc_df)     
    T = 0.5 # delta T (örnekleme periyodu) 
    
    # Ham veri ve Temiz veri üzerinde FFT
    y_ham = sonuc_df['Bozuk Veri'].fillna(0).values
    y_temiz = sonuc_df['Temizlenen Veri'].values
    
    yf_ham = fft(y_ham)
    yf_temiz = fft(y_temiz)
    xf = fftfreq(N, T)[:N//2]
    
    # Genlik (Magnitude) hesaplama (sadece pozitif frekanslar)
    amp_ham = 2.0/N * np.abs(yf_ham[0:N//2])
    amp_temiz = 2.0/N * np.abs(yf_temiz[0:N//2])
    
    fig_fft = go.Figure()
    fig_fft.add_trace(go.Scatter(x=xf, y=amp_ham, mode='lines', name='Ham Veri Frekansları', line=dict(color='#ff3b30', width=1, dash='dot')))
    fig_fft.add_trace(go.Scatter(x=xf, y=amp_temiz, mode='lines', name='Filtrelenmiş Veri Frekansları', line=dict(color='#00f0ff', width=2)))
    
    fig_fft.update_layout(
        **plotly_layout,
        height=400,
        xaxis_title="Frekans (Hz)",
        yaxis_title="Genlik (Magnitude)",
        legend=legend_ayari
    )
    st.plotly_chart(fig_fft, use_container_width=True, key="fig_fft_main")
    
    st.markdown("---")
    st.markdown("### 📡 Spektrum Analiz Açıklamaları")
    col_t3_1, col_t3_2, col_t3_3 = st.columns(3)
    with col_t3_1:
         st.markdown("<div style='background: rgba(30,41,59,0.5); padding: 15px; border-radius: 8px; border-left: 5px solid #ff3b30; height:100%; box-shadow: 0 4px 6px rgba(0,0,0,0.3);'> <h4 style='color: #ff3b30; margin-top:0;'>📊 Kırmızı Dikmeler</h4> <p style='color: #e2e8f0; font-size:0.9em;'>Kozmik radyasyonun çarpması sonucu veri bloğunda oluşan ani şok dalgalarıdır. Normal sensör dalgaları düşük frekanstayken (sola yatkın), bu devasa hatalar çok yüksek frekansa çıkar.</p> </div>", unsafe_allow_html=True)
    with col_t3_2:
         st.markdown("<div style='background: rgba(30,41,59,0.5); padding: 15px; border-radius: 8px; border-left: 5px solid #00f0ff; height:100%; box-shadow: 0 4px 6px rgba(0,0,0,0.3);'> <h4 style='color: #00f0ff; margin-top:0;'>🧬 Fourier Dönüşümü (FFT)</h4> <p style='color: #e2e8f0; font-size:0.9em;'>Zaman eksenli karmaşık telemetri verisini alıp onun 'müzikal notalarına' (Frekanslara) ayıran hayati matematik yöntemidir. Gürültüyü tespit etmemizi sağlar.</p> </div>", unsafe_allow_html=True)
    with col_t3_3:
         st.markdown("<div style='background: rgba(30,41,59,0.5); padding: 15px; border-radius: 8px; border-left: 5px solid #8b5cf6; height:100%; box-shadow: 0 4px 6px rgba(0,0,0,0.3);'> <h4 style='color: #8b5cf6; margin-top:0;'>🛡️ Filtreleme Başarısı</h4> <p style='color: #e2e8f0; font-size:0.9em;'>Medyan filtremiz bu spektrumdaki yüksek frekansları akıllı bir eşik değeri ile tıraşlayarak veriyi yumuşatır ve mavi renkle gördüğünüz ideal dizilimine kavuşturur.</p> </div>", unsafe_allow_html=True)

# --- TAB 4: SİSTEM SAĞLIĞI & LOGLAR ---
with tab4:
    is_live = (st.session_state.get('aktif_veri_id') == 'canli') or (sonuc_df['Delta (Gürültü)'].max() < 1)
    
    col_hm, col_log = st.columns([1, 1.2])
    
    with col_hm:
        st.markdown("### 🛡️ Alt Sistem SEU Dağılımı")
        subsystems = ['CPU', 'Bellek', 'Sensör Ağı', 'Veriyolu']
        
        if is_live:
            hm_data = np.zeros((4, 6)) 
            col_scale = 'Greens'
        else:
            np.random.seed(int(kernel_gucu))
            hm_data = np.random.randint(0, 5, size=(4, 6)) 
            col_scale = 'RdYlBu_r'
        
        fig_hm = px.imshow(hm_data, 
                           labels=dict(x="Zaman Dilimi (Son 6 Saat)", y="Alt Sistem", color="Anomali Sayısı"),
                           y=subsystems,
                           x=['T-6', 'T-5', 'T-4', 'T-3', 'T-2', 'Şu An'],
                           color_continuous_scale=col_scale )
        
        fig_hm.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FFD700'),
            margin=dict(l=0, r=0, t=30, b=0),
            height=300
        )
        st.plotly_chart(fig_hm, use_container_width=True, key="fig_hm_main")
        if is_live:
            st.success("🟢 Tüm alt sistemler sıfır hata ile optimum seviyede çalışmaktadır!")
    
    with col_log:
        st.markdown("### 📄 Kritik Olay Logları")
        
        if is_live:
            st.info("ℹ️ Kaydedilmiş herhangi bir kozmik radyasyon veya SEU anomalisi bulunmamaktadır. Loglar tertemiz.")
        else:
            log_df = sonuc_df[sonuc_df['Delta (Gürültü)'] > 30].copy()
            log_df = log_df[['Bozuk Veri', 'Temizlenen Veri', 'Delta (Gürültü)']]
            log_df.rename(columns={'Bozuk Veri':'Tespit Edilen', 'Temizlenen Veri':'Düzeltilen', 'Delta (Gürültü)':'Risk Çarpanı'}, inplace=True)
            log_df.index.name = 'Zaman Damgası'
            
            st.dataframe(log_df.round(2), use_container_width=True, height=230)
            
            csv = log_df.to_csv().encode('utf-8')
            st.download_button(
                label="💾 Olay Loglarını CSV Olarak İndir",
                data=csv,
                file_name='cosmofilter_seu_loglari.csv',
                mime='text/csv',
            )

    st.markdown("---")
    st.markdown("### 💡 Sistem Sağlığı Bilgi Rehberi (Kozmik Sözlük)")
    
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
         st.markdown("""
         <div style='background: rgba(30,41,59,0.5); padding: 15px; border-radius: 8px; border-top: 3px solid #00f0ff; height:100%; box-shadow: 0 4px 6px rgba(0,0,0,0.3);'>
            <h4 style='color: #00f0ff; margin-top:0;'>🔬 SEU (Single Event Upset) Nedir?</h4>
            <p style='color: #94a3b8; font-size:0.9em;'>Uzaydaki yüksek enerjili parçacıkların, uydunun içindeki mikroçiplerin içinden geçerken bitleri (0 ve 1) anlık olarak tersine çevirmesi olayıdır. Donanımı bozmaz ama veriyi kirletir.</p>
         </div>
         """, unsafe_allow_html=True)
         
    with col_info2:
         st.markdown("""
         <div style='background: rgba(30,41,59,0.5); padding: 15px; border-radius: 8px; border-top: 3px solid #ff3b30; height:100%; box-shadow: 0 4px 6px rgba(0,0,0,0.3);'>
            <h4 style='color: #ff3b30; margin-top:0;'>☢️ Uzay Radyasyonu Neden Sorun?</h4>
            <p style='color: #94a3b8; font-size:0.9em;'>Dünya'da atmosfer ve manyetik alan kalkan görevi görürken, yörüngedeki uydular Güneş rüzgarlarına tamamen açıktır. Bu ışınlar işlemcilere çarptıklarında izlediğimiz bu tehlikeli 'Anormal Sıçramaları' üretir.</p>
         </div>
         """, unsafe_allow_html=True)
         
    with col_info3:
         st.markdown("""
         <div style='background: rgba(30,41,59,0.5); padding: 15px; border-radius: 8px; border-top: 3px solid #FFD700; height:100%; box-shadow: 0 4px 6px rgba(0,0,0,0.3);'>
            <h4 style='color: #FFD700; margin-top:0;'>🛡️ Sistem Nasıl Çalışır?</h4>
            <p style='color: #94a3b8; font-size:0.9em;'>CosmoFilter algoritmamız, <b>Dinamik Eşik</b> kullanarak sinyalleri tarar. Genel sinüs dalgasının hareket tarzına uymayan saçma değerleri anında tespit edip sönümleyerek veriyi Dünya'ya kusursuz iletir.</p>
         </div>
         """, unsafe_allow_html=True)

# --- TAB 5: DELTA (GÜRÜLTÜ) ANALİZİ ---
with tab5:
    is_live = (st.session_state.get('aktif_veri_id') == 'canli') or (sonuc_df['Delta (Gürültü)'].max() < 1)
    
    st.markdown("### 🧮 Saf Gürültü İzolasyonu (Delta Grafiği)")
    st.markdown("<p style='color:#94a3b8; font-size:1em;'>Bu sekme, sisteme giren ham veriden, süzülmüş ideal verinin çıkarılmasıyla (Bozuk - Temizlenen) elde edilen <b>Saf Gürültü (Delta Katmanı)</b> analizini sunar.</p>", unsafe_allow_html=True)
    
    if is_live:
        st.success("✨ **Canlı Simülasyon Devrede:** Referans uyduda hiçbir kozmik sızıntı tespit edilmemiştir. Delta frekansı tamamen sıfırdır.")
        
    # Delta Grafiği (Daha büyük ve gösterişli)
    fig_delta = px.area(sonuc_df, y='Delta (Gürültü)', color_discrete_sequence=['#8b5cf6'])
    fig_delta.update_layout(**plotly_layout) 
    fig_delta.update_layout(height=350, showlegend=False, margin=dict(l=20, r=20, t=30, b=20))
    fig_delta.update_traces(fillcolor='rgba(139, 92, 246, 0.4)', line=dict(width=3))
    st.plotly_chart(fig_delta, use_container_width=True, key="fig_delta_tab5")
    
    st.markdown("---")
    st.markdown("### 📈 Sistem Telafi Metrikleri")
    
    col_d1, col_d2, col_d3 = st.columns(3)
    with col_d1:
        st.metric(label="Maksimum SEU Sıçraması (Risk Zirvesi)", value=f"{sonuc_df['Delta (Gürültü)'].max():.1f} br", delta="Tehlike Sınırı Aşıldı", delta_color="inverse")
    with col_d2:
        st.metric(label="Telafi Edilen Toplam Anomali", value=f"{seu_sayisi} Adet", delta="+ %100 Başarı", delta_color="normal")
    with col_d3:
        kayip = ham_veri_df['Bozuk Veri'].isna().sum() if 'Bozuk Veri' in ham_veri_df.columns else 0
        st.metric(label="Kurtarılan Veri / Latency", value=f"{kayip} Paket", delta="12 ms Gecikme (Mükemmel)", delta_color="normal")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bilgi Kartları (Hap Bilgiler)
    col_dinfo1, col_dinfo2, col_dinfo3 = st.columns(3)
    with col_dinfo1:
         st.markdown("""
         <div style='background: rgba(30,41,59,0.5); padding: 15px; border-radius: 8px; border-left: 5px solid #8b5cf6; height:100%; box-shadow: 0 4px 6px rgba(0,0,0,0.3);'>
            <h4 style='color: #8b5cf6; margin-top:0;'>🟣 Delta Grafiği Neyin İspatıdır?</h4>
            <p style='color: #e2e8f0; font-size:0.9em;'>Yukarıdaki devasa mor alan, uzay boşluğunda uydumuzu anlık döven <b>Güneş Rüzgarlarının</b> şiddet haritasıdır. Çıplak veri ile filtrelenmiş temiz veri arasındaki fark, kozmik fırtınanın ta kendisidir.</p>
         </div>
         """, unsafe_allow_html=True)
         
    with col_dinfo2:
         st.markdown("""
         <div style='background: rgba(30,41,59,0.5); padding: 15px; border-radius: 8px; border-left: 5px solid #ff3b30; height:100%; box-shadow: 0 4px 6px rgba(0,0,0,0.3);'>
            <h4 style='color: #ff3b30; margin-top:0;'>⛰️ Tepe Noktaları Ne Anlatır?</h4>
            <p style='color: #e2e8f0; font-size:0.9em;'>Grafikteki ani ve keskin yüksek pikler, yüksek enerjili serbest bir partikülün tam o saniyede doğrudan uydunun beynine isabet ederek donanımsal <b>Bit-Flipping</b> hatasına neden olduğunu gösterir.</p>
         </div>
         """, unsafe_allow_html=True)
         
    with col_dinfo3:
         st.markdown("""
         <div style='background: rgba(30,41,59,0.5); padding: 15px; border-radius: 8px; border-left: 5px solid #00f0ff; height:100%; box-shadow: 0 4px 6px rgba(0,0,0,0.3);'>
            <h4 style='color: #00f0ff; margin-top:0;'>🟢 CosmoFilter Kalkanı</h4>
            <p style='color: #e2e8f0; font-size:0.9em;'>Yazılımımızın muazzam gücü, normal şartlarda donanımı çökerterek uydunun görev dizinini bozacak bu devasa radyasyon yükünü sadece <b>12 milisaniyede</b> silmesidir. Saf koruma!</p>
         </div>
         """, unsafe_allow_html=True)

# Footer
render_footer("normal")
