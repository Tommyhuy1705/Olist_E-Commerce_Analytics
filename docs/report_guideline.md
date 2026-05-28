# Guideline viết báo cáo đồ án theo chuẩn nghiên cứu khoa học

Tài liệu này dùng để chia nội dung báo cáo cho nhóm. Báo cáo nên viết theo văn phong học thuật, có dẫn nguồn, có hình/bảng minh họa, có kết quả thực nghiệm và có phần đánh giá rõ ràng.

## Quy ước chung

- Viết tiếng Việt có dấu, tránh văn nói.
- Mỗi chương cần có phần mở đầu ngắn và kết luận chương.
- Hình, bảng phải có số thứ tự và chú thích: `Hình 2.1`, `Bảng 3.1`.
- Các thuật ngữ như `data warehouse`, `star schema`, `Iceberg Cube`, `classification`, `feature engineering` có thể giữ tiếng Anh nhưng cần giải thích khi xuất hiện lần đầu.
- Không đưa code dài vào nội dung chính; code quan trọng có thể đưa vào phụ lục.
- Mọi biểu đồ/kết quả trong báo cáo phải lấy từ notebook, script hoặc app của repo.

## Bìa và phần đầu báo cáo

Nội dung cần có:

- Tên trường, khoa, môn học.
- Tên đề tài: **Xây dựng data warehouse và khai phá dữ liệu thương mại điện tử trên bộ dữ liệu Olist Brazilian E-Commerce**.
- Danh sách thành viên, MSSV, lớp.
- Giảng viên hướng dẫn.
- Ngày nộp.
- Lời cảm ơn nếu giảng viên yêu cầu.
- Mục lục.
- Danh mục hình.
- Danh mục bảng.
- Danh mục từ viết tắt.

## Tóm tắt

Viết khoảng 200-300 từ:

- Bối cảnh bài toán thương mại điện tử.
- Dataset sử dụng.
- Các phương pháp chính: EDA, preprocessing, data warehouse, Iceberg Cube, classification, web app.
- Kết quả nổi bật: warehouse đã xây dựng, cube patterns, model metrics, dashboard/API.
- Ý nghĩa ứng dụng.

## Chương 1. Giới thiệu đề tài

### 1.1. Lý do chọn đề tài

Nêu lý do chọn dữ liệu e-commerce:

- Thương mại điện tử tạo ra nhiều dữ liệu giao dịch, thanh toán, vận chuyển và phản hồi khách hàng.
- Doanh nghiệp cần phân tích doanh thu, độ trễ giao hàng, mức độ hài lòng và nguy cơ review xấu.
- Olist là dataset thực tế, có nhiều bảng và phù hợp để xây dựng data warehouse.

### 1.2. Mục tiêu nghiên cứu

Trình bày các mục tiêu:

- Mô tả và phân tích bộ dữ liệu Olist.
- Tiền xử lý và tạo đặc trưng phục vụ khai phá dữ liệu.
- Thiết kế data warehouse theo star schema.
- Tính toán Iceberg Cube để tìm các nhóm dữ liệu có ý nghĩa.
- Xây dựng mô hình dự đoán review xấu.
- Triển khai API và web dashboard.

### 1.3. Đối tượng và phạm vi nghiên cứu

- Đối tượng: dữ liệu đơn hàng, khách hàng, seller, sản phẩm, thanh toán, review và giao hàng.
- Phạm vi: dữ liệu Olist giai đoạn 2016-2018.
- Không đi sâu vào xử lý NLP comment review trong phiên bản hiện tại.

### 1.4. Đóng góp của đề tài

Nêu các đóng góp:

- Pipeline xử lý dữ liệu hoàn chỉnh.
- Data warehouse bằng PostgreSQL/SQL Server.
- Iceberg Cube theo các chủ đề kinh doanh.
- Model classification dự đoán bad review.
- Dashboard và API phục vụ demo.

### 1.5. Cấu trúc báo cáo

Tóm tắt nội dung từng chương.

## Chương 2. Cơ sở lý thuyết và công nghệ sử dụng

### 2.1. Khai phá dữ liệu

Trình bày:

- Khái niệm data mining.
- Vai trò của EDA và preprocessing.
- Bài toán classification.
- Các metric đánh giá: accuracy, precision, recall, F1-score, ROC-AUC, confusion matrix.

### 2.2. Data Warehouse

Trình bày:

- Khái niệm data warehouse.
- Sự khác nhau giữa OLTP và OLAP.
- Star schema.
- Fact table và dimension table.
- Grain của fact table.

### 2.3. Iceberg Cube

Trình bày:

- Khái niệm data cube.
- Vấn đề số lượng cuboid tăng rất nhanh.
- Iceberg Cube giữ lại các nhóm thỏa ngưỡng support/measure.
- Các ngưỡng dùng trong đồ án: `count_orders`, `sum_revenue`, `bad_review_rate`.

### 2.4. Mô hình classification

Trình bày ngắn:

- Logistic Regression.
- Random Forest.
- HistGradientBoosting hoặc mô hình tối ưu nhóm đã dùng.
- Lý do chọn mô hình chính.

### 2.5. Công nghệ sử dụng

Liệt kê:

- Python, pandas, numpy, scikit-learn.
- PostgreSQL hoặc SQL Server.
- SQLAlchemy.
- FastAPI.
- Streamlit.
- GitHub Project.

## Chương 3. Mô tả bộ dữ liệu và phân tích khám phá EDA

### 3.1. Nguồn dữ liệu

Mô tả:

- Tên dataset: Brazilian E-Commerce Public Dataset by Olist.
- Nguồn: Kaggle.
- Dữ liệu đã được ẩn danh.
- Khoảng thời gian: 2016-2018.

### 3.2. Cấu trúc dữ liệu

Tạo bảng mô tả 9 file:

- `olist_orders_dataset.csv`
- `olist_customers_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_order_payments_dataset.csv`
- `olist_order_reviews_dataset.csv`
- `olist_products_dataset.csv`
- `olist_sellers_dataset.csv`
- `olist_geolocation_dataset.csv`
- `product_category_name_translation.csv`

Nên có:

- số dòng;
- số cột;
- khóa chính;
- khóa ngoại;
- ý nghĩa bảng.

### 3.3. Quan hệ giữa các bảng

Vẽ ERD hoặc sơ đồ quan hệ:

- `orders` liên kết `customers`.
- `order_items` liên kết `orders`, `products`, `sellers`.
- `payments` liên kết `orders`.
- `reviews` liên kết `orders`.
- `products` liên kết bảng translation.

### 3.4. Kiểm tra chất lượng dữ liệu

Trình bày:

- Missing values.
- Duplicate rows.
- Kiểu dữ liệu.
- Các cột timestamp.
- Các vấn đề cần xử lý trước khi phân tích.

### 3.5. Phân tích EDA

Các biểu đồ nên có:

- Số đơn hàng theo tháng.
- Doanh thu theo tháng.
- Phân bố trạng thái đơn hàng.
- Phân bố review score.
- Phân bố payment type.
- Top category theo doanh thu.
- Top state theo số đơn/doanh thu.
- Delivery days và delay days.
- Liên hệ giữa giao hàng trễ và review xấu.

### 3.6. Nhận xét từ EDA

Viết insight dạng gạch đầu dòng, ví dụ:

- Doanh thu tập trung ở một số bang lớn.
- Credit card là phương thức thanh toán phổ biến.
- Giao hàng trễ có liên hệ với tỷ lệ review xấu.
- Một số category có doanh thu cao nhưng review/delay cần chú ý.

## Chương 4. Tiền xử lý dữ liệu và xây dựng đặc trưng

### 4.1. Quy trình tiền xử lý

Mô tả pipeline:

1. Đọc 9 file CSV.
2. Chuẩn hóa kiểu dữ liệu.
3. Xử lý missing values.
4. Join các bảng.
5. Tổng hợp dữ liệu về mức order-level.
6. Tạo feature cho model.
7. Lưu dữ liệu processed.

### 4.2. Xử lý missing values

Trình bày cách xử lý:

- Product category thiếu -> `unknown`.
- Product dimensions thiếu -> median.
- Timestamp giao hàng thiếu -> giữ cho phân tích status, loại khỏi một số feature nếu không đủ điều kiện.
- Review comment thiếu -> không dùng NLP trong phiên bản hiện tại.

### 4.3. Feature engineering

Danh sách feature chính:

- `delivery_days`
- `approval_hours`
- `carrier_days`
- `delay_days`
- `is_delayed`
- `order_year_month`
- `order_month`
- `order_day_of_week`
- `item_count`
- `total_price`
- `total_freight`
- `freight_ratio`
- `payment_type`
- `max_installments`
- `customer_state`
- `seller_state`
- `product_category_name_english`

### 4.4. Tạo target cho classification

Target:

- `bad_review = 1` nếu `review_score <= 2`.
- `bad_review = 0` nếu `review_score >= 4`.
- Bỏ review 3 sao để tránh nhãn trung tính.

### 4.5. Kết quả dữ liệu sau xử lý

Nêu các file output:

- `order_features.csv`
- `model_dataset.csv`
- các bảng dimension/fact dạng CSV nếu có.

## Chương 5. Xây dựng Data Warehouse

### 5.1. Mục tiêu xây dựng DWH

Nêu mục tiêu:

- Hỗ trợ truy vấn OLAP.
- Tổ chức dữ liệu theo fact/dimension.
- Phục vụ dashboard và Iceberg Cube.

### 5.2. Thiết kế star schema

Trình bày sơ đồ star schema:

- Fact: `fact_order_items`.
- Dimensions: `dim_date`, `dim_customer`, `dim_seller`, `dim_product`, `dim_payment`, `dim_order_status`.

### 5.3. Mô tả fact table

Grain:

- 1 dòng = 1 item trong 1 order.

Measures:

- `price`
- `freight_value`
- `review_score`
- `delivery_days`
- `delay_days`
- `is_delayed`
- `bad_review`

### 5.4. Mô tả dimension tables

Mỗi dimension cần mô tả:

- khóa;
- thuộc tính;
- vai trò trong phân tích.

### 5.5. Load dữ liệu vào PostgreSQL/SQL Server

Nêu:

- cấu hình `.env`;
- script `scripts/load_warehouse.py`;
- số dòng từng bảng sau khi load;
- query kiểm tra.

### 5.6. Các truy vấn OLAP mẫu

Đưa một số query:

- doanh thu theo tháng;
- top category theo doanh thu;
- delay rate theo seller state;
- bad review rate theo category/payment type.

## Chương 6. Tính toán Iceberg Cube

### 6.1. Mục tiêu

Giải thích vì sao dùng Iceberg Cube:

- cube đầy đủ sinh quá nhiều tổ hợp;
- chỉ giữ nhóm dữ liệu có ý nghĩa theo ngưỡng;
- giúp phát hiện pattern kinh doanh đáng chú ý.

### 6.2. Thiết kế thuật toán

Mô tả input:

- DataFrame order-level;
- danh sách dimensions;
- measure;
- threshold.

Mô tả output:

- bảng cuboid thỏa điều kiện iceberg.

### 6.3. Các chủ đề cube

Các cube nên trình bày:

- `order_year_month x product_category_name_english x customer_state`
- `seller_state x product_category_name_english x is_delayed`
- `payment_type x installments_group x review_group`
- `customer_state x seller_state x review_group`

### 6.4. Kết quả Iceberg Cube

Trình bày:

- số pattern giữ lại;
- top pattern theo doanh thu;
- top pattern theo bad review rate;
- top pattern theo delay rate.

### 6.5. Nhận xét

Nêu insight:

- nhóm category/state nào đem lại doanh thu cao;
- nhóm nào có tỷ lệ giao hàng trễ cao;
- nhóm nào có nguy cơ review xấu cao.

## Chương 7. Mô hình classification dự đoán review xấu

### 7.1. Phát biểu bài toán

Input:

- thông tin đơn hàng, thanh toán, sản phẩm, khách hàng, seller, giao hàng.

Output:

- dự đoán đơn hàng có review xấu hay không.

### 7.2. Dữ liệu train/test

Nêu:

- số dòng model dataset;
- tỷ lệ bad review;
- train/test split;
- stratify theo target.

### 7.3. Mô hình baseline

Trình bày Logistic Regression:

- lý do dùng làm baseline;
- preprocessing numeric/categorical;
- kết quả metrics.

### 7.4. Tối ưu hóa mô hình

Trình bày model nâng cao:

- Random Forest;
- HistGradientBoosting hoặc model nhóm chọn;
- tham số chính;
- xử lý class imbalance nếu có.

### 7.5. Đánh giá mô hình

Bảng metrics:

- accuracy;
- precision;
- recall;
- F1-score;
- ROC-AUC.

Thêm confusion matrix.

### 7.6. Nhận xét mô hình

Nêu:

- model dự đoán tốt ở mức nào;
- điểm mạnh/yếu;
- tại sao recall lớp bad review còn khó;
- hướng cải thiện.

## Chương 8. Triển khai ứng dụng

### 8.1. Kiến trúc hệ thống

Vẽ sơ đồ:

```text
CSV Dataset -> ETL/Preprocessing -> Data Warehouse -> Iceberg Cube/Model -> API -> Streamlit App
```

### 8.2. FastAPI

Mô tả endpoints:

- `/health`
- `/summary`
- `/metrics`
- `/cube`
- `/predict`

### 8.3. Streamlit dashboard

Mô tả các trang:

- Overview.
- EDA.
- Iceberg Cube.
- Prediction.

### 8.4. Demo

Chèn screenshot:

- dashboard overview;
- biểu đồ EDA;
- bảng Iceberg Cube;
- form prediction;
- kết quả dự đoán.

## Chương 9. Kết luận và hướng phát triển

### 9.1. Kết quả đạt được

Tóm tắt:

- đã mô tả và phân tích dataset;
- đã tiền xử lý và tạo feature;
- đã xây dựng DWH;
- đã tính Iceberg Cube;
- đã train model classification;
- đã triển khai API và web app.

### 9.2. Hạn chế

Nêu hạn chế:

- chưa phân tích sâu review text bằng NLP;
- dataset đã cũ, chỉ đến 2018;
- mô hình còn có thể cải thiện recall lớp bad review;
- chưa triển khai production cloud.

### 9.3. Hướng phát triển

Đề xuất:

- thêm NLP sentiment analysis từ review comment;
- thêm clustering khách hàng/seller;
- thêm dashboard bản đồ;
- triển khai Docker;
- tự động hóa pipeline bằng scheduler;
- so sánh thêm nhiều mô hình ML.

## Tài liệu tham khảo

Nên có ít nhất:

- Trang Kaggle dataset Olist.
- Tài liệu pandas.
- Tài liệu scikit-learn.
- Tài liệu PostgreSQL hoặc SQL Server.
- Tài liệu FastAPI.
- Tài liệu Streamlit.
- Tài liệu về data warehouse, OLAP, data cube hoặc Iceberg Cube.

## Phụ lục

Nội dung có thể đưa vào phụ lục:

- Data dictionary đầy đủ.
- Một số SQL query.
- Một số đoạn code quan trọng.
- Kết quả chạy pipeline.
- Link GitHub repository.
