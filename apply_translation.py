import codecs
import re

file_path = "app.py"

with codecs.open(file_path, "r", "utf-8") as f:
    app_code = f.read()

# Insert _tr function right after t = lang_dict[...]
helper_code = """
def _tr(tr_text, en_text):
    return en_text if st.session_state.get('app_lang') == '🇬🇧 EN' else tr_text
"""
app_code = app_code.replace("t = lang_dict[st.session_state['app_lang']]", "t = lang_dict[st.session_state['app_lang']]\n" + helper_code)


replacements = [
    # History Modal
    ('st.markdown("### 🇹🇷 Göklere Adanmış Bir Asır")', 'st.markdown(_tr("### 🇹🇷 Göklere Adanmış Bir Asır", "### 🇹🇷 A Century Dedicated to the Skies"))'),
    ('st.markdown("> *\\"İstikbal Göklerdedir.\\"* - **Mustafa Kemal Atatürk**")', 'st.markdown(_tr("> *\\"İstikbal Göklerdedir.\\"* - **Mustafa Kemal Atatürk**", "> *\\"The future is in the skies.\\"* - **Mustafa Kemal Atatürk**"))'),
    ("1925 - TOMTAŞ ve Vecihi Hürkuş", "1925 - TOMTAŞ and Vecihi Hürkuş"),
    ("Türkiye'nin ilk uçak fabrikası TOMTAŞ kuruldu. Vecihi Hürkuş kendi uçağı K-VI'yı üretip uçmasına rağmen, sertifikasyon engelleri ve bürokrasi yüzünden projeler yarım kaldı.", "Turkey's first aircraft factory TOMTAŞ was established. Although Vecihi Hürkuş produced and flew his own aircraft K-VI, projects were left unfinished due to certification obstacles and bureaucracy."),
    ("1936 - Nuri Demirağ <i>(Yarım Kalan Hayal)</i>", "1936 - Nuri Demirağ <i>(Unfinished Dream)</i>"),
    ("Türkiye'nin ilk seri üretim yolcu uçakları Nu.D.38 üretildi fakat siparişlerin iptal edilmesi sebebiyle fabrika kapatılmak zorunda kaldı, eşsiz bir vizyon yok oldu.", "Turkey's first mass-produced passenger aircraft Nu.D.38 was produced, but the factory had to be closed due to the cancellation of orders, and a unique vision was lost."),
    ("TÜRKSAT 1A'nın okyanusa düşmesinden sadece aylar sonra uzaya fırlatılan TÜRKSAT 1B ile Türkiye, uzaydaki ilk imzasını gururla attı.", "With TÜRKSAT 1B launched into space just months after TÜRKSAT 1A fell into the ocean, Turkey proudly put its first signature in space."),
    ("Teknoloji transferi (Know-How) amacıyla yurt dışı ile ortak fırlatılan ilk gözlem uydumuz.", "Our first observation satellite launched jointly with abroad for the purpose of technology transfer (Know-How)."),
    ("Yabancı destek olmadan, Türk mühendisleri tarafından tasarlanıp üretilen ilk yer gözlem uydusu yörüngeye oturdu!", "The first earth observation satellite designed and produced by Turkish engineers without foreign support was placed in orbit!"),
    ("Milli Uzay Programı'nın yürütülmesi ve sivil uzay faaliyetlerinin tek elde toplanması vizyonuyla hizmete girdi.", "It went into service with the vision of carrying out the National Space Program and gathering civil space activities in a single hand."),
    ("2024 - Kızıl Elma'nın Uzay Yürüyüşü", "2024 - Red Apple's Space Walk"),
    ("Alper Gezeravcı, ISS'te bilimsel deneyler yaparak Türkiye'nin ilk astronotu oldu. Hemen ardından <b>TÜRKSAT 6A</b>, tamamen yerli mühendislikle fırlatıldı!", "Alper Gezeravcı became Turkey's first astronaut by conducting scientific experiments on the ISS. Right after, <b>TÜRKSAT 6A</b> was launched with fully domestic engineering!"),
    
    ('st.markdown("### 🌌 Gözümüz Yükseklerde")', 'st.markdown(_tr("### 🌌 Gözümüz Yükseklerde", "### 🌌 Our Eyes are High"))'),
    ('st.markdown("Türkiye\\'nin uzay ve astronomideki kalbi olan gözlemevlerimiz ve gökyüzü nöbetçileri uydularımız:")', 'st.markdown(_tr("Türkiye\\'nin uzay ve astronomideki kalbi olan gözlemevlerimiz ve gökyüzü nöbetçileri uydularımız:", "Our observatories and satellites, the heart of Turkey in space and astronomy:"))'),
    ("🔭 TUG (TÜBİTAK Ulusal Gözlemevi)", "🔭 TUG (TÜBİTAK National Observatory)"),
    ("1997 yılında Antalya Bakırlıtepe'de kurulan TUG, astronomi biliminin ülkemizdeki kalesidir.", "TUG, established in 1997 in Antalya Bakırlıtepe, is the fortress of astronomy in our country."),
    ("Yüksek çözünürlüklü askeri ve sivil yer gözlem uydularımız. İMECE tamamen yerli olarak tasarlanmıştır!", "Our high-resolution military and civil earth observation satellites. İMECE is completely domestically designed!"),
    ("📡 DAG (Doğu Anadolu Gözlemevi)", "📡 DAG (Eastern Anatolia Observatory)"),
    ("Türkiye'nin en büyük 4 metrelik kızılötesi teleskobuna ev sahipliği yapar. Erzurum'da bulunmaktadır.", "Hosts Turkey's largest 4-meter infrared telescope. Located in Erzurum."),
    ("🌍 TÜRKSAT Filosu", "🌍 TÜRKSAT Fleet"),
    ("Afrika'dan Avrupa'ya devasa bir coğrafyaya yayın yapan güçlü haberleşme altyapımız.", "Our strong communication infrastructure that broadcasts to a huge geography from Africa to Europe."),
    
    ('st.error("Lütfen uygulamanın modal desteklemesi için Streamlit sürümünü güncelleyin.")', 'st.error(_tr("Lütfen uygulamanın modal desteklemesi için Streamlit sürümünü güncelleyin.", "Please update Streamlit to support modals."))'),
    
    ('st.sidebar.button("🌌 Yeni Telemetri Sinyali Oluştur", use_container_width=True, type="primary")', 'st.sidebar.button(t["new_btn"], use_container_width=True, type="primary")'),
    ('yeni_isim = f"📡 Sinyal #{sayac}"', 'yeni_isim = _tr(f"📡 Sinyal #{sayac}", f"📡 Signal #{sayac}")'),
    
    ('st.info("**Şirket:** Kızıl Elmalar Uzay Teknolojileri A.Ş.")', 'st.info(_tr("**Şirket:** Kızıl Elmalar Uzay Teknolojileri A.Ş.", "**Company:** Red Apples Space Technologies Inc."))'),
    ('st.markdown("**📞 Müşteri Hizmetleri:** +90 555 123 4567")', 'st.markdown(_tr("**📞 Müşteri Hizmetleri:** +90 555 123 4567", "**📞 Customer Service:** +90 555 123 4567"))'),
    ('st.markdown("**📧 Kurumsal E-posta:** iletisim@kizilelmalar-space.com")', 'st.markdown(_tr("**📧 Kurumsal E-posta:** iletisim@kizilelmalar-space.com", "**📧 Corporate Email:** contact@kizilelmalar-space.com"))'),
    
    ('st.markdown("**Carrington Olayı (1859):** Kayıtlara geçen en şiddetli Güneş fırtınasıdır. Öyle büyük bir radyoaktif plazma fırlatılmıştı ki, Dünya\\'daki telgraf hatları aşırı yüklenmeden alev almış, operatörler elektrik çarpmasına maruz kalmıştı. Aynı fırtına bugün yaşansa, saniyeler içinde trilyonlarca dolarlık uydu ve internet altyapımız eriyerek yok olabilir!")',
     'st.markdown(_tr("**Carrington Olayı (1859):** Kayıtlara geçen en şiddetli Güneş fırtınasıdır. Öyle büyük bir radyoaktif plazma fırlatılmıştı ki, Dünya\\'daki telgraf hatları aşırı yüklenmeden alev almış, operatörler elektrik çarpmasına maruz kalmıştı. Aynı fırtına bugün yaşansa, saniyeler içinde trilyonlarca dolarlık uydu ve internet altyapımız eriyerek yok olabilir!", "**Carrington Event (1859):** It is the most severe solar storm on record. Such a large radioactive plasma was launched that the telegraph lines on Earth caught fire from overload, and operators were subjected to electric shocks. If the same storm happened today, our multi-trillion dollar satellite and internet infrastructure could melt and disappear in seconds!"))'),
    ('st.markdown("**ISS Hızı ve Sürekli Düşüş:** Uluslararası Uzay İstasyonu (ISS) saniyede yaklaşık 7.66 km hızla seyahat eder. Aslında o irtifada yerçekimi vardır (Dünya\\'daki değerin %90\\'ı), ancak uydular ve istasyon inanılmaz bir doğrusal hızla **\\'Dünya\\'nın eğriminin etrafında sürekli düştükleri\\'** için astronotlar ağırlıksızlık hissi yaşar.")',
     'st.markdown(_tr("**ISS Hızı ve Sürekli Düşüş:** Uluslararası Uzay İstasyonu (ISS) saniyede yaklaşık 7.66 km hızla seyahat eder. Aslında o irtifada yerçekimi vardır (Dünya\\'daki değerin %90\\'ı), ancak uydular ve istasyon inanılmaz bir doğrusal hızla **\\'Dünya\\'nın eğriminin etrafında sürekli düştükleri\\'** için astronotlar ağırlıksızlık hissi yaşar.", "**ISS Speed and Continuous Fall:** The International Space Station (ISS) travels at a speed of approximately 7.66 km per second. In fact, there is gravity at that altitude (90% of the value on Earth), but since satellites and the station are **\\'continuously falling around the Earth\\'s curvature\\'** at an incredible linear speed, astronauts experience a feeling of weightlessness."))'),
    
    ('st.markdown("<div style=\\'text-align:center; color:#64748b; font-size:0.8em; margin-top:10px;\\'>© 2026 <b>Kızıl Elmalar</b> Takımı - Uzay ve Havacılık Teknolojileri</div>", unsafe_allow_html=True)',
     'st.markdown(_tr("<div style=\\'text-align:center; color:#64748b; font-size:0.8em; margin-top:10px;\\'>© 2026 <b>Kızıl Elmalar</b> Takımı - Uzay ve Havacılık Teknolojileri</div>", "<div style=\\'text-align:center; color:#64748b; font-size:0.8em; margin-top:10px;\\'>© 2026 <b>Red Apples</b> Team - Space and Aviation Technologies</div>"), unsafe_allow_html=True)'),
    
    ('with st.expander("💡 Kozmik Hap Bilgi: Biliyor muydunuz?"):', 'with st.expander(_tr("💡 Kozmik Hap Bilgi: Biliyor muydunuz?", "💡 Cosmic Pill Info: Did you know?")):')
]
for src, dst in replacements:
    app_code = app_code.replace(src, dst)

# Step 1 logic
step_blocks = [
    ('"🌟 1/4: CosmoFilter\\'a Hoş Geldiniz!"', '_tr("🌟 1/4: CosmoFilter\\'a Hoş Geldiniz!", "🌟 1/4: Welcome to CosmoFilter!")'),
    ('"Bu sistem, uzay araçlarından gelen gürültülü telemetri verilerini gerçek zamanlı temizlemek için kurgulanmıştır."', '_tr("Bu sistem, uzay araçlarından gelen gürültülü telemetri verilerini gerçek zamanlı temizlemek için kurgulanmıştır.", "This system is designed to clean up noisy telemetry data from spacecraft in real time.")'),
    ('"🎛️ 2/4: Sol Menü (Kontrol Merkezi)"', '_tr("🎛️ 2/4: Sol Menü (Kontrol Merkezi)", "🎛️ 2/4: Left Menu (Control Center)")'),
    ('"Sol taraftaki \\'Yeni Telemetri Oluştur\\' butonu ile farklı kozmik radyasyon parçacıklarıyla dolu (Bozuk) senaryolar yaratabilirsiniz. \\'Canlı Simülasyon\\' butonu ise hatasız referans veriyi (Uydunun ilk halini) ekrana getirir."', '_tr("Sol taraftaki \\'Yeni Telemetri Oluştur\\' butonu ile farklı kozmik radyasyon parçacıklarıyla dolu (Bozuk) senaryolar yaratabilirsiniz. \\'Canlı Simülasyon\\' butonu ise hatasız referans veriyi (Uydunun ilk halini) ekrana getirir.", "With the \\'Generate New Telemetry\\' button on the left, you can create (Corrupted) scenarios full of different cosmic radiation particles. The \\'Live Simulation\\' button brings error-free reference data (the satellite\\'s initial state) to the screen.")'),
    ('"🔄 3/4: Geçmiş ve Kıyaslama"', '_tr("🔄 3/4: Geçmiş ve Kıyaslama", "🔄 3/4: History and Comparison")'),
    ('"Ürettiğiniz her sinyal sol alttaki listeye eklenir. Tabloda isimlerine tıklayarak veriler arasında anında geçiş yapabilir, grafik değişimlerini A/B testi yapar gibi kıyaslayabilirsiniz. Satırlar yandaki Kalem ile isimlendirilebilir."', '_tr("Ürettiğiniz her sinyal sol alttaki listeye eklenir. Tabloda isimlerine tıklayarak veriler arasında anında geçiş yapabilir, grafik değişimlerini A/B testi yapar gibi kıyaslayabilirsiniz. Satırlar yandaki Kalem ile isimlendirilebilir.", "Every signal you produce is added to the list on the bottom left. By clicking on their names in the table, you can instantly switch between data and compare graphic changes just like an A/B test. The rows can be named with the Pen next to them.")'),
    ('"🎚️ 4/4: Kozmik Veri Hattı (Filtreleme)"', '_tr("🎚️ 4/4: Kozmik Veri Hattı (Filtreleme)", "🎚️ 4/4: Cosmic Data Pipeline (Filtering)")'),
    ('"Hemen aşağıdaki \\'Filtre Kalibrasyonu\\' sürgüsünü sağa-sola çekerek CosmoFilter\\'ın hatalı verileri (kırmızı pikleri) nasıl anında tıraşladığını kendiniz de test edin!"', '_tr("Hemen aşağıdaki \\'Filtre Kalibrasyonu\\' sürgüsünü sağa-sola çekerek CosmoFilter\\'ın hatalı verileri (kırmızı pikleri) nasıl anında tıraşladığını kendiniz de test edin!", "Test for yourself how CosmoFilter shaves off faulty data (red peaks) instantly by dragging the \\'Filter Calibration\\' slider below to the right and left!")')
]
for src, dst in step_blocks:
    app_code = app_code.replace(src, dst)

button_blocks = [
    ('st.button("İleri (Next) ⏩"', 'st.button(_tr("İleri (Next) ⏩", "Next ⏩")'),
    ('st.button("Harika, Eğitimi Bitir ✔️"', 'st.button(_tr("Harika, Eğitimi Bitir ✔️", "Great, Finish Tutorial ✔️")'),
    ('st.button("Eğitimi Atla (Skip) ✖"', 'st.button(_tr("Eğitimi Atla (Skip) ✖", "Skip Tutorial ✖")')
]
for src, dst in button_blocks:
    app_code = app_code.replace(src, dst)

# Translate Tab Headers via regex/replacement
# Since we translated tabs directly in lang_dict, we should change st.tabs()
# Wait, st.tabs is called directly.
app_code = app_code.replace('st.tabs([\n    "📡 Kozmik Veri Hattı", \n    "🌍 3D Yörünge Şovu", \n    "📈 Spektrum Analizi", \n    "🛡️ Sistem Sağlığı & Loglar",\n    "🧮 Delta Analizi"\n])', 'st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"], t["tab5"]])')

app_code = app_code.replace('st.markdown("<h1>🛰️ <span class=\\'highlight-cyan\\'>CosmoFilter</span> | Kozmik Veri Ayıklama Hattı</h1>", unsafe_allow_html=True)', 'st.markdown("<h1>" + t["title_main"] + "</h1>", unsafe_allow_html=True)')
app_code = app_code.replace('st.markdown("<p style=\\'color:#94a3b8; font-size:1.1em;\\'>Uzay araçlarından iletilen telemetri verilerindeki <b>SEU (Single Event Upset)</b> ve kozmik gürültüleri gerçek zamanlı tespit ve telafi eden yüksek performanslı sinyal işleme hattı.</p>", unsafe_allow_html=True)', 'st.markdown("<p style=\\'color:#94a3b8; font-size:1.1em;\\'>" + t["subtitle"] + "</p>", unsafe_allow_html=True)')

app_code = app_code.replace("""st.warning(f"⚠️ Düşük/Orta Seviye Uyarı: Telemetride {seu_sayisi} adet ufak çaplı bozucu etki onarıldı.")""", """st.warning(_tr(f"⚠️ Düşük/Orta Seviye Uyarı: Telemetride {seu_sayisi} adet ufak çaplı bozucu etki onarıldı.", f"⚠️ Low/Medium Warning: {seu_sayisi} minor disruptive effects were repaired in telemetry."))""")

app_code = app_code.replace('st.markdown(f\'<div class="uyari-kutusu">🚨 KRİTİK RADYASYON UYARISI: Veri hattında yüksek anomali tespiti! (Sistem <span style="color:#fff">{seu_sayisi} adet</span> dezenformasyonu bloke etti)</div>\', unsafe_allow_html=True)', "st.markdown(_tr(f'<div class=\"uyari-kutusu\">🚨 KRİTİK RADYASYON UYARISI: Veri hattında yüksek anomali tespiti! (Sistem <span style=\"color:#fff\">{seu_sayisi} adet</span> dezenformasyonu bloke etti)</div>', f'<div class=\"uyari-kutusu\">🚨 CRITICAL RADIATION WARNING: High anomaly detection in the data pipeline! (System blocked <span style=\"color:#fff\">{seu_sayisi} units</span> of disinformation)</div>'), unsafe_allow_html=True)")

app_code = app_code.replace('st.markdown("### <span class=\\'highlight-red\\'>🔴</span> Ham Yörünge Telemetrisi", unsafe_allow_html=True)', 'st.markdown(_tr("### <span class=\\'highlight-red\\'>🔴</span> Ham Yörünge Telemetrisi", "### <span class=\\'highlight-red\\'>🔴</span> Raw Orbital Telemetry"), unsafe_allow_html=True)')
app_code = app_code.replace("name='İdeal Sinyal'", "name=_tr('İdeal Sinyal', 'Ideal Signal')")
app_code = app_code.replace("name='Ham Telemetri'", "name=_tr('Ham Telemetri', 'Raw Telemetry')")
app_code = app_code.replace("title=\"Zaman\"", "title=_tr(\"Zaman\", \"Time\")")
app_code = app_code.replace("title=\"Sinyal Genliği\"", "title=_tr(\"Sinyal Genliği\", \"Signal Amplitude\")")
app_code = app_code.replace("ℹ️ Gördüğünüz keskin sıçramalar (pikler), kozmik ışınların mikroçiplerdeki transistörlere çarpması sonucu oluşan donanımsal körlüklerdir. Algoritmamıza akan çıplak veri budur.", "ℹ️ The sharp spikes you see are hardware blindness caused by cosmic rays hitting transistors in microchips. This is the bare data flowing to our algorithm.")

app_code = app_code.replace('st.markdown("### <span class=\\'highlight-cyan\\'>🟢</span> CosmoFilter Çıktısı", unsafe_allow_html=True)', 'st.markdown(_tr("### <span class=\\'highlight-cyan\\'>🟢</span> CosmoFilter Çıktısı", "### <span class=\\'highlight-cyan\\'>🟢</span> CosmoFilter Output"), unsafe_allow_html=True)')
app_code = app_code.replace("name='Filtrelenmiş Veri'", "name=_tr('Filtrelenmiş Veri', 'Filtered Data')")
app_code = app_code.replace("ℹ️ CosmoFilter, bu anomali noktalarını nanosaniyeler içinde tespit edip sinyalin orijinal karakteristiğine (sinüs) zarar vermeden akıllıca tıraşlamaktadır.", "ℹ️ CosmoFilter detects these anomaly points within nanoseconds and smartly shaves them without damaging the original characteristic (sine) of the signal.")

app_code = app_code.replace('st.markdown("### ⚙️ Sistem Kontrol Konsolu")', 'st.markdown(_tr("### ⚙️ Sistem Kontrol Konsolu", "### ⚙️ System Control Console"))')
app_code = app_code.replace('"Filtre Kalibrasyonu (Medyan Penceresi)"', '_tr("Filtre Kalibrasyonu (Medyan Penceresi)", "Filter Calibration (Median Window)")')
app_code = app_code.replace('help="Pencere boyutu artarsa düzeltme artar ancak mikro detaylar kaybolabilir."', 'help=_tr("Pencere boyutu artarsa düzeltme artar ancak mikro detaylar kaybolabilir.", "If the window size increases, correction increases but micro details may be lost.")')
app_code = app_code.replace("Bu ayar CosmoFilter'ın hatalı sinyalleri yakalama agresifliğini belirler. Değişimi anında yukarıdaki grafikte görebilirsiniz.", "This setting determines the aggressiveness of CosmoFilter in catching faulty signals. You can see the change instantly on the graph above.")

app_code = app_code.replace('st.file_uploader("📥 Geçmiş Görev Verisi Yükle (Playback)", type=["csv"], key="dosya_yukle")', 'st.file_uploader(_tr("📥 Geçmiş Görev Verisi Yükle (Playback)", "📥 Load Past Mission Data (Playback)"), type=["csv"], key="dosya_yukle")')
app_code = app_code.replace("Dosya yüklendiğinde otomatik olarak simülasyon modundan çıkılır. (Format: 'Zaman', 'Bozuk Veri')", "When a file is loaded, it automatically exits simulation mode. (Format: 'Time', 'Corrupted Data')")

# Tab 2
app_code = app_code.replace('st.markdown("### 🌍 Uydunun Anlık Yörünge Durumu (Gerçekçi Harita)")', 'st.markdown(_tr("### 🌍 Uydunun Anlık Yörünge Durumu (Gerçekçi Harita)", "### 🌍 Satellite\\'s Instant Orbit Status (Realistic Map)"))')
app_code = app_code.replace("name='Planlanan Rota'", "name=_tr('Planlanan Rota', 'Planned Route')")
app_code = app_code.replace("text=['🚀 Kızıl Elma']", "text=[_tr('🚀 Kızıl Elma', '🚀 Red Apple')]")
app_code = app_code.replace("name='Kızıl Elma Uydusu'", "name=_tr('Kızıl Elma Uydusu', 'Red Apple Satellite')")

app_code = app_code.replace('st.metric(label="İrtifa", value="402.5 km", delta="Yükseliyor", delta_color="normal")', 'st.metric(label=_tr("İrtifa", "Altitude"), value="402.5 km", delta=_tr("Yükseliyor", "Ascending"), delta_color="normal")')
app_code = app_code.replace('st.metric(label="Orbital Hız", value="7.66 km/sn", delta="Stabil", delta_color="off")', 'st.metric(label=_tr("Orbital Hız", "Orbital Speed"), value="7.66 km/s", delta=_tr("Stabil", "Stable"), delta_color="off")')
app_code = app_code.replace('st.metric(label="Güneş Paneli Sıcaklığı", value="74 °C", delta="Maksimum Güç", delta_color="off")', 'st.metric(label=_tr("Güneş Paneli Sıcaklığı", "Solar Panel Temp"), value="74 °C", delta=_tr("Maksimum Güç", "Max Power"), delta_color="off")')

app_code = app_code.replace('st.markdown("### 🔭 Yörünge Telemetri Hap Bilgileri")', 'st.markdown(_tr("### 🔭 Yörünge Telemetri Hap Bilgileri", "### 🔭 Orbital Telemetry Pill Info"))')
app_code = app_code.replace("🛰️ İrtifa ve Atmosfer", "🛰️ Altitude and Atmosphere")
app_code = app_code.replace("Uydumuz LEO (Alçak Dünya Yörüngesi) adı verilen bölgede seyahat etmektedir. Bu bölgede sürüklenme direnci (Drag) nedeniyle uydular düzenli olarak itki kullanmalıdır.", "Our satellite travels in LEO (Low Earth Orbit). In this region, satellites must regularly use propulsion due to drag.")
app_code = app_code.replace("🌌 Koordinat Sistemi", "🌌 Coordinate System")
app_code = app_code.replace("Harita, eşlek koordinat sistemi ile dönüştürülmüş projeksiyonu birleştirerek harita üzerindeki X, Y eksenlerini anlık orbital eğim ile eşleştirmektedir.", "The map combines the equatorial coordinate system with the transformed projection to map the X, Y axes onto the real-time orbital inclination.")
app_code = app_code.replace("☀️ Termal Etkiler", "☀️ Thermal Effects")
app_code = app_code.replace("Uydular Dünya'nın karanlık yüzüne geçerken Güneş panelleri aniden aşırı soğur, aydınlık yüze geçildiğinde ise paneller ısınarak ekstrem dereceleri görebilir.", "When satellites pass to the dark side of the Earth, their solar panels suddenly overcool. When switching to the bright side, the panels heat up to extreme degrees.")

# Tab 3
app_code = app_code.replace('st.markdown("### 📈 Sinyalin Frekans Analizi (Fourier Dönüşümü)")', 'st.markdown(_tr("### 📈 Sinyalin Frekans Analizi (Fourier Dönüşümü)", "### 📈 Frequency Analysis of the Signal (Fourier Transform)"))')
app_code = app_code.replace("name='Ham Veri Frekansları'", "name=_tr('Ham Veri Frekansları', 'Raw Data Frequencies')")
app_code = app_code.replace("name='Filtrelenmiş Veri Frekansları'", "name=_tr('Filtrelenmiş Veri Frekansları', 'Filtered Data Frequencies')")
app_code = app_code.replace('xaxis_title="Frekans (Hz)"', 'xaxis_title=_tr("Frekans (Hz)", "Frequency (Hz)")')
app_code = app_code.replace('yaxis_title="Genlik (Magnitude)"', 'yaxis_title=_tr("Genlik (Magnitude)", "Amplitude (Magnitude)")')

app_code = app_code.replace('st.markdown("### 📡 Spektrum Analiz Açıklamaları")', 'st.markdown(_tr("### 📡 Spektrum Analiz Açıklamaları", "### 📡 Spectrum Analysis Explanations"))')
app_code = app_code.replace("📊 Kırmızı Dikmeler", "📊 Red Pillars")
app_code = app_code.replace("Kozmik radyasyonun çarpması sonucu veri bloğunda oluşan ani şok dalgalarıdır. Normal sensör dalgaları düşük frekanstayken (sola yatkın), bu devasa hatalar çok yüksek frekansa çıkar.", "They are sudden shock waves in the data block caused by the impact of cosmic radiation. While normal sensor waves are at a low frequency, these massive errors go to very high frequencies.")
app_code = app_code.replace("🧬 Fourier Dönüşümü (FFT)", "🧬 Fourier Transform (FFT)")
app_code = app_code.replace("Zaman eksenli karmaşık telemetri verisini alıp onun 'müzikal notalarına' (Frekanslara) ayıran hayati matematik yöntemidir. Gürültüyü tespit etmemizi sağlar.", "It is the vital mathematical method that takes time-axis complex telemetry data and separates it into its 'musical notes' (Frequencies). It helps us detect the noise.")
app_code = app_code.replace("🛡️ Filtreleme Başarısı", "🛡️ Filtering Success")
app_code = app_code.replace("Medyan filtremiz bu spektrumdaki yüksek frekansları akıllı bir eşik değeri ile tıraşlayarak veriyi yumuşatır ve mavi renkle gördüğünüz ideal dizilimine kavuşturur.", "Our median filter softens the data by shaving the high frequencies in this spectrum with a smart threshold, reaching the ideal formation you see in blue.")

# Tab 4
app_code = app_code.replace('st.markdown("### 🛡️ Alt Sistem SEU Dağılımı")', 'st.markdown(_tr("### 🛡️ Alt Sistem SEU Dağılımı", "### 🛡️ Subsystem SEU Distribution"))')
app_code = app_code.replace("subsystems = ['CPU', 'Bellek', 'Sensör Ağı', 'Veriyolu']", "subsystems = [_tr('CPU', 'CPU'), _tr('Bellek', 'Memory'), _tr('Sensör Ağı', 'Sensor Net'), _tr('Veriyolu', 'Bus')]")
app_code = app_code.replace('labels=dict(x="Zaman Dilimi (Son 6 Saat)", y="Alt Sistem", color="Anomali Sayısı")', 'labels=dict(x=_tr("Zaman Dilimi (Son 6 Saat)", "Timeframe (Last 6 Hours)"), y=_tr("Alt Sistem", "Subsystem"), color=_tr("Anomali Sayısı", "Anomaly Count"))')
app_code = app_code.replace("x=['T-6', 'T-5', 'T-4', 'T-3', 'T-2', 'Şu An']", "x=['T-6', 'T-5', 'T-4', 'T-3', 'T-2', _tr('Şu An', 'Now')]")
app_code = app_code.replace('st.success("🟢 Tüm alt sistemler sıfır hata ile optimum seviyede çalışmaktadır!")', 'st.success(_tr("🟢 Tüm alt sistemler sıfır hata ile optimum seviyede çalışmaktadır!", "🟢 All subsystems are running optimally with zero errors!"))')

app_code = app_code.replace('st.markdown("### 📄 Kritik Olay Logları")', 'st.markdown(_tr("### 📄 Kritik Olay Logları", "### 📄 Critical Event Logs"))')
app_code = app_code.replace('st.info("ℹ️ Kaydedilmiş herhangi bir kozmik radyasyon veya SEU anomalisi bulunmamaktadır. Loglar tertemiz.")', 'st.info(_tr("ℹ️ Kaydedilmiş herhangi bir kozmik radyasyon veya SEU anomalisi bulunmamaktadır. Loglar tertemiz.", "ℹ️ No recorded cosmic radiation or SEU anomalies found. Logs are totally clean."))')

app_code = app_code.replace("log_df.rename(columns={'Bozuk Veri':'Tespit Edilen', 'Temizlenen Veri':'Düzeltilen', 'Delta (Gürültü)':'Risk Çarpanı'}, inplace=True)", "log_df.rename(columns={'Bozuk Veri':_tr('Tespit Edilen', 'Detected'), 'Temizlenen Veri':_tr('Düzeltilen', 'Corrected'), 'Delta (Gürültü)':_tr('Risk Çarpanı', 'Risk Factor')}, inplace=True)")
app_code = app_code.replace("log_df.index.name = 'Zaman Damgası'", "log_df.index.name = _tr('Zaman Damgası', 'Timestamp')")

app_code = app_code.replace('label="💾 Olay Loglarını CSV Olarak İndir"', 'label=_tr("💾 Olay Loglarını CSV Olarak İndir", "💾 Download Event Logs as CSV")')

app_code = app_code.replace('st.markdown("### 💡 Sistem Sağlığı Bilgi Rehberi (Kozmik Sözlük)")', 'st.markdown(_tr("### 💡 Sistem Sağlığı Bilgi Rehberi (Kozmik Sözlük)", "### 💡 System Health Info Guide (Cosmic Dictionary)"))')
app_code = app_code.replace("🔬 SEU (Single Event Upset) Nedir?", "🔬 What is SEU (Single Event Upset)?")
app_code = app_code.replace("Uzaydaki yüksek enerjili parçacıkların, uydunun içindeki mikroçiplerin içinden geçerken bitleri (0 ve 1) anlık olarak tersine çevirmesi olayıdır. Donanımı bozmaz ama veriyi kirletir.", "It is the event of high-energy particles in space passing through microchips inside the satellite and momentarily reversing the bits (0 and 1). It does not break the hardware but contaminates the data.")
app_code = app_code.replace("☢️ Uzay Radyasyonu Neden Sorun?", "☢️ Why is Space Radiation a Problem?")
app_code = app_code.replace("Dünya'da atmosfer ve manyetik alan kalkan görevi görürken, yörüngedeki uydular Güneş rüzgarlarına tamamen açıktır. Bu ışınlar işlemcilere çarptıklarında izlediğimiz bu tehlikeli 'Anormal Sıçramaları' üretir.", "While the atmosphere and magnetic field act as a shield on Earth, satellites in orbit are completely open to solar winds. These rays produce these dangerous 'Abnormal Spikes' we see when they hit processors.")
app_code = app_code.replace("🛡️ Sistem Nasıl Çalışır?", "🛡️ How does the System Work?")
app_code = app_code.replace("CosmoFilter algoritmamız, <b>Dinamik Eşik</b> kullanarak sinyalleri tarar. Genel sinüs dalgasının hareket tarzına uymayan saçma değerleri anında tespit edip sönümleyerek veriyi Dünya'ya kusursuz iletir.", "Our CosmoFilter algorithm scans signals using a <b>Dynamic Threshold</b>. It transmits data flawlessly to Earth by instantly detecting and damping absurd values that do not fit the movement style of the general sine wave.")

# Tab 5
app_code = app_code.replace('st.markdown("### 🧮 Saf Gürültü İzolasyonu (Delta Grafiği)")', 'st.markdown(_tr("### 🧮 Saf Gürültü İzolasyonu (Delta Grafiği)", "### 🧮 Pure Noise Isolation (Delta Graph)"))')
app_code = app_code.replace("Bu sekme, sisteme giren ham veriden, süzülmüş ideal verinin çıkarılmasıyla (Bozuk - Temizlenen) elde edilen <b>Saf Gürültü (Delta Katmanı)</b> analizini sunar.", "This tab presents the <b>Pure Noise (Delta Layer)</b> analysis obtained by subtracting the filtered ideal data from the raw data entering the system (Corrupted - Cleaned).")
app_code = app_code.replace('st.success("✨ **Canlı Simülasyon Devrede:** Referans uyduda hiçbir kozmik sızıntı tespit edilmemiştir. Delta frekansı tamamen sıfırdır.")', 'st.success(_tr("✨ **Canlı Simülasyon Devrede:** Referans uyduda hiçbir kozmik sızıntı tespit edilmemiştir. Delta frekansı tamamen sıfırdır.", "✨ **Live Simulation Active:** No cosmic leakage was detected on the reference satellite. Delta frequency is completely zero."))')

app_code = app_code.replace('st.markdown("### 📈 Sistem Telafi Metrikleri")', 'st.markdown(_tr("### 📈 Sistem Telafi Metrikleri", "### 📈 System Compensation Metrics"))')

app_code = app_code.replace('st.metric(label="Maksimum SEU Sıçraması (Risk Zirvesi)", value=f"{sonuc_df[\'Delta (Gürültü)\'].max():.1f} br", delta="Tehlike Sınırı Aşıldı", delta_color="inverse")', 'st.metric(label=_tr("Maksimum SEU Sıçraması (Risk Zirvesi)", "Max SEU Jump (Risk Peak)"), value=f"{sonuc_df[\'Delta (Gürültü)\'].max():.1f} br", delta=_tr("Tehlike Sınırı Aşıldı", "Danger Limit Exceeded"), delta_color="inverse")')
app_code = app_code.replace('st.metric(label="Telafi Edilen Toplam Anomali", value=f"{seu_sayisi} Adet", delta="+ %100 Başarı", delta_color="normal")', 'st.metric(label=_tr("Telafi Edilen Toplam Anomali", "Total Compensated Anomalies"), value=f"{seu_sayisi} {_tr(\'Adet\', \'Units\')}", delta=_tr("+ %100 Başarı", "+ 100% Success"), delta_color="normal")')
app_code = app_code.replace('st.metric(label="Kurtarılan Veri / Latency", value=f"{kayip} Paket", delta="12 ms Gecikme (Mükemmel)", delta_color="normal")', 'st.metric(label=_tr("Kurtarılan Veri / Latency", "Recovered Data / Latency"), value=f"{kayip} {_tr(\'Paket\', \'Packets\')}", delta=_tr("12 ms Gecikme (Mükemmel)", "12 ms Delay (Perfect)"), delta_color="normal")')

app_code = app_code.replace("🟣 Delta Grafiği Neyin İspatıdır?", "🟣 What is the Delta Graph Proof Of?")
app_code = app_code.replace("Yukarıdaki devasa mor alan, uzay boşluğunda uydumuzu anlık döven <b>Güneş Rüzgarlarının</b> şiddet haritasıdır. Çıplak veri ile filtrelenmiş temiz veri arasındaki fark, kozmik fırtınanın ta kendisidir.", "The massive purple area above is a map of the intensity of the <b>Solar Winds</b> that instantly batter our satellite in the vacuum of space. The difference between raw data and filtered clean data is the cosmic storm itself.")
app_code = app_code.replace("⛰️ Tepe Noktaları Ne Anlatır?", "⛰️ What do the Peaks Tell?")
app_code = app_code.replace("Grafikteki ani ve keskin yüksek pikler, yüksek enerjili serbest bir partikülün tam o saniyede doğrudan uydunun beynine isabet ederek donanımsal <b>Bit-Flipping</b> hatasına neden olduğunu gösterir.", "Sudden and sharp high peaks in the graph indicate that a free particle with high energy hit the brain of the satellite directly exactly at that second, causing a hardware <b>Bit-Flipping</b> error.")
app_code = app_code.replace("🟢 CosmoFilter Kalkanı", "🟢 CosmoFilter Shield")
app_code = app_code.replace("Yazılımımızın muazzam gücü, normal şartlarda donanımı çökerterek uydunun görev dizinini bozacak bu devasa radyasyon yükünü sadece <b>12 milisaniyede</b> silmesidir. Saf koruma!", "The immense power of our software is that it can wipe out this massive radiation load in just <b>12 milliseconds</b>, which would normally crash hardware and disrupt the satellite's task sequence. Pure protection!")

# Handle "İsim Değiştirme", vb. sidebar button/help texts
app_code = app_code.replace('help="İsmi yeniden adlandır"', 'help=_tr("İsmi yeniden adlandır", "Rename")')
app_code = app_code.replace('help="Sinyali tamamen sil"', 'help=_tr("Sinyali tamamen sil", "Delete signal entirely")')


with codecs.open(file_path, "w", "utf-8") as f:
    f.write(app_code)

print("Translation applied successfully!")
