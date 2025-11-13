import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


df_customers=pd.read_csv("dosya yolu")
df_basket=pd.read_csv("dosya yolu")

print("Customer Details (ilk 5 satır):")
print(df_customers.head())
print("\nBasket Details(ilk 5 satır):")
print(df_basket.head())
print("\nCustomer Details Bilgisi:")
print(df_customers.info())
print("\nBasket Details Bilgisi:")
print(df_basket.info())

print("\nEksik Değer Sayısı (Customer):")
print(df_customers.isnull().sum())
print(df_basket.isnull().sum())

df_basket["basket_date"]=pd.to_datetime(df_basket["basket_date"], errors="coerce")
df_basket= df_basket.dropna(subset=["basket_date"])

print("\nBenzersiz Müşteri Sayısı:",df_customers["customer_id"].nunique())
print("Benzersiz Sepet-Müşteri Saysısı:", df_basket["customer_id"].nunique())
print("Toplam Ürün Sayısı:",df_basket["product_id"].nunique())
print("\nCustomer Detayları (Sayısal kolon istatistikleri):")

print(df_customers.describe())
print("\nBasket Detayları (Sayısal kolon istatistikleri):")
print(df_basket.describe())
df_customers.to_csv("/Users/user/Downloads/ecommerce-sales-dataset/customer_details.csv",index=False)
df_basket.to_csv("/Users/user/Downloads/ecommerce-sales-dataset/basket_details.csv",index=False)

print("\n--- KEŞİFSEL VERİ ANALİZİ (EDA) ---")

# En çok satılan ürünler
product_sales = (
    df_basket.groupby("product_id")["basket_count"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
print("\nEn çok satılan 10 ürün:")
print(product_sales.head(10))

# En çok alışveriş yapan müşteriler
top_customers = (
    df_basket.groupby("customer_id")["basket_count"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
print("\nEn çok alışveriş yapan 10 müşteri:")
print(top_customers.head(10))

# Aylık satış trendi
df_basket["year_month"] = df_basket["basket_date"].dt.to_period("M")
monthly_sales = (
    df_basket.groupby("year_month")["basket_count"]
    .sum()
    .reset_index()
)
print("\nAylık Satış Trend (Adet Bazlı):")
print(monthly_sales.head())

# Müşteri şehirlerine göre satış (müşteri ve sepeti birleştir)
merged_df = pd.merge(df_basket, df_customers, on="customer_id", how="left")

if "customer_city" in merged_df.columns:
    city_sales = (
        merged_df.groupby("customer_city")["basket_count"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    print("\nŞehirlere Göre Toplam Satış:")
    print(city_sales.head(10))
else:
    print("\nUyarı: Müşteri verisinde 'customer_city' sütunu bulunamadı. Şehir analizi atlandı.")
    city_sales = pd.DataFrame(columns=["customer_city", "basket_count"])

plot_dir = "/Users/user/Downloads/ecommerce-sales-dataset/plots"
os.makedirs(plot_dir, exist_ok=True)

print(f"\nGrafikler {plot_dir} klasörüne kaydediliyor...")

# 1) En çok satılan ürünler
plt.figure(figsize=(10, 6))
plt.bar(product_sales["product_id"].head(10).astype(str), product_sales["basket_count"].head(10))
plt.title("En Çok Satılan 10 Ürün")
plt.xlabel("Ürün ID")
plt.ylabel("Toplam Satış Adedi")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(plot_dir, "en_cok_satilan_urunler.png"))
plt.close()

# 2) Aylık satış trendi
plt.figure(figsize=(10, 5))
plt.plot(monthly_sales["year_month"].astype(str), monthly_sales["basket_count"], marker="o")
plt.title("Aylık Satış Trendleri")
plt.xlabel("Yıl-Ay")
plt.ylabel("Toplam Satış Adedi")
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(plot_dir, "aylik_satis_trendi.png"))
plt.close()

# 3) Şehirlere göre satış
if not city_sales.empty:
    plt.figure(figsize=(10, 6))
    plt.bar(city_sales["customer_city"].head(10), city_sales["basket_count"].head(10))
    plt.title("En Çok Satış Yapılan 10 Şehir")
    plt.xlabel("Şehir")
    plt.ylabel("Toplam Satış Adedi")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, "en_cok_satis_yapilan_sehirler.png"))
    plt.close()

print("Grafikler başarıyla kaydedildi ✅")

# AŞAMA 4: RAPORLAMA
# ---------------------------------------------------------------

top3_products = product_sales.head(3)
for _, row in top3_products.iterrows():
    print(f"- Ürün {row['product_id']}: toplam {row['basket_count']} adet satılmış.")

if not city_sales.empty:
    best_city = city_sales.iloc[0]
    print(f"\nEn çok satış yapılan şehir: {best_city['customer_city']} ({best_city['basket_count']} adet)")

print("\n--- YÖNETİM İÇİN ÖNERİLER ---")
print("1. En çok satılan ürünlerin stokları güçlendirilmeli.")
if not city_sales.empty:
    print(f"2. {best_city['customer_city']} şehrinde reklam ve kampanya yoğunlaştırılmalı.")
print("3. Düşük satış yapılan bölgelerde promosyon planları yapılmalı.")
print("4. Aylık trendlere göre sezonluk kampanyalar hazırlanmalı.")

# CSV olarak kaydet
out_dir = "/Users/user/Downloads/ecommerce-sales-dataset/outputs"
os.makedirs(out_dir, exist_ok=True)

product_sales.to_csv(os.path.join(out_dir, "top_products.csv"), index=False)
top_customers.to_csv(os.path.join(out_dir, "top_customers.csv"), index=False)
monthly_sales.to_csv(os.path.join(out_dir, "monthly_sales.csv"), index=False)
if not city_sales.empty:
    city_sales.to_csv(os.path.join(out_dir, "top_cities.csv"), index=False)

print(f"\nTüm analiz tamamlandı. Sonuç dosyaları '{out_dir}' ve grafikler '{plot_dir}' klasöründe kaydedildi.")

# Rapor klasörü
report_dir = "/Users/user/Downloads/ecommerce-sales-dataset/report"
os.makedirs(report_dir, exist_ok=True)
report_file = os.path.join(report_dir, "ecommerce_sales_report.txt")

# Rapor içeriği
report_lines = []

report_lines.append("E-Ticaret Satış Analizi Raporu\n")
report_lines.append("="*50 + "\n")

# Özet Bilgiler
report_lines.append("1. Özet Bilgiler\n")
report_lines.append(f"- Benzersiz Müşteri Sayısı: {df_customers['customer_id'].nunique()}")
report_lines.append(f"- Benzersiz Sepet-Müşteri Sayısı: {df_basket['customer_id'].nunique()}")
report_lines.append(f"- Toplam Ürün Sayısı: {df_basket['product_id'].nunique()}")
report_lines.append(f"- Toplam Satış Adedi: {df_basket['basket_count'].sum()}\n")

# En Çok Satılan Ürünler
report_lines.append("2. En Çok Satılan 10 Ürün\n")
for i, row in product_sales.head(10).iterrows():
    report_lines.append(f"{i+1}. Ürün ID {row['product_id']} - Toplam Satış: {row['basket_count']} adet")
report_lines.append("")

# En Çok Alışveriş Yapan Müşteriler
report_lines.append("3. En Çok Alışveriş Yapan 10 Müşteri\n")
for i, row in top_customers.head(10).iterrows():
    report_lines.append(f"{i+1}. Müşteri ID {row['customer_id']} - Toplam Sepet Adedi: {row['basket_count']}")
report_lines.append("")

# Aylık Satış Trendleri
report_lines.append("4. Aylık Satış Trendleri (Adet Bazlı)\n")
for i, row in monthly_sales.iterrows():
    report_lines.append(f"- {row['year_month']}: {row['basket_count']} adet")
report_lines.append("")

# Şehirlere Göre Satış
report_lines.append("5. Şehirlere Göre Satış (Top 10)\n")
if not city_sales.empty:
    for i, row in city_sales.head(10).iterrows():
        report_lines.append(f"{i+1}. {row['customer_city']} - Toplam Satış: {row['basket_count']} adet")
else:
    report_lines.append("Şehir bilgisi bulunamadığı için şehir bazlı analiz yapılamadı.")
report_lines.append("")

# Yönetim İçin Öneriler
report_lines.append("6. Yönetim İçin Öneriler\n")
report_lines.append("- En çok satılan ürünlerin stokları güçlendirilmeli.")
if not city_sales.empty:
    report_lines.append(f"- {best_city['customer_city']} şehrinde reklam ve kampanya yoğunlaştırılmalı.")
report_lines.append("- Düşük satış yapılan bölgelerde promosyon planları yapılmalı.")
report_lines.append("- Aylık trendlere göre sezonluk kampanyalar hazırlanmalı.\n")

# Dosyaya yaz
with open(report_file, "w", encoding="utf-8") as f:
    f.write("\n".join(report_lines))

print(f"Metin raporu başarıyla oluşturuldu ✅: {report_file}")




