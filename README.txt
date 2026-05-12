VOLT VISION AI - ULTRA PRO VERSION

1. File chính
- app_dien_ultra.py: giao diện dashboard đẹp và chuyên nghiệp hơn.
- model_dien_pro.pkl: mô hình đã train sẵn.
- model_metrics.json: thông tin đánh giá mô hình.
- Book1_clean_no_email.csv: dữ liệu đã làm sạch.
- train_model_dien_pro.py: code train lại mô hình nếu cần.
- requirements.txt: thư viện cần cài.

2. Cách chạy trên máy tính
Mở CMD/Terminal trong thư mục này:

pip install -r requirements.txt
streamlit run app_dien_ultra.py

3. Cách chạy trên Google Colab
Upload file zip này lên Colab rồi chạy:

from google.colab import files
uploaded = files.upload()

import zipfile, os
with zipfile.ZipFile("du_bao_tien_dien_ultra_pro.zip", "r") as z:
    z.extractall("du_bao_tien_dien_ultra_pro")

os.chdir("du_bao_tien_dien_ultra_pro")

!pip install -r requirements.txt
!streamlit run app_dien_ultra.py --server.port 8501 --server.address 0.0.0.0 > app.log 2>&1 &
!npm install -g localtunnel
!npx localtunnel --port 8501

Nếu localtunnel hỏi IP, chạy:
!wget -q -O - ipv4.icanhazip.com

4. Điểm nâng cấp của bản Ultra Pro
- Giao diện dạng dashboard cao cấp.
- Có hero section, logo, thẻ KPI, hóa đơn mô phỏng.
- Có thanh mức độ chi phí và energy score.
- Có biểu đồ kịch bản giờ dùng máy lạnh.
- Có gợi ý tiết kiệm điện theo đầu vào.
- Hạn chế dùng một số widget động dễ lỗi khi chạy qua localtunnel.
