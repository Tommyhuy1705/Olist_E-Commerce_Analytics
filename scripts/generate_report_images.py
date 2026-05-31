"""Generate report-ready visualization images with Vietnamese font support."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib import font_manager
from sklearn.metrics import ConfusionMatrixDisplay, PrecisionRecallDisplay, RocCurveDisplay
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.etl.extract import load_olist_tables
from src.etl.transform import build_model_dataset, build_order_features
from src.models.train import CATEGORICAL_FEATURES, NUMERIC_FEATURES, train_model
from src.olap.iceberg_cube import compute_default_olist_cubes


IMAGE_DIR = PROJECT_ROOT / "docs" / "images"


def configure_fonts() -> None:
    """Use a Windows font that supports Vietnamese diacritics."""
    for font_path in [Path(r"C:\Windows\Fonts\arial.ttf"), Path(r"C:\Windows\Fonts\arialbd.ttf")]:
        if font_path.exists():
            font_manager.fontManager.addfont(str(font_path))
    matplotlib.rcParams["font.family"] = "Arial"
    matplotlib.rcParams["axes.unicode_minus"] = False
    sns.set_theme(style="whitegrid", font="Arial")


def save(fig: plt.Figure, filename: str) -> None:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    path = IMAGE_DIR / filename
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    print(path)


def generate_eda_images(features: pd.DataFrame, tables: dict[str, pd.DataFrame]) -> None:
    monthly = (
        features.groupby("order_year_month")
        .agg(orders=("order_id", "nunique"), revenue=("total_price", "sum"))
        .reset_index()
    )

    fig = plt.figure(figsize=(11, 4.5))
    sns.lineplot(data=monthly, x="order_year_month", y="orders", marker="o")
    plt.xticks(rotation=60)
    plt.title("Số lượng đơn hàng theo tháng")
    plt.xlabel("Tháng")
    plt.ylabel("Số đơn hàng")
    save(fig, "eda_monthly_orders.png")

    fig = plt.figure(figsize=(11, 4.5))
    sns.lineplot(data=monthly, x="order_year_month", y="revenue", marker="o")
    plt.xticks(rotation=60)
    plt.title("Doanh thu theo tháng")
    plt.xlabel("Tháng")
    plt.ylabel("Doanh thu")
    save(fig, "eda_monthly_revenue.png")

    status_counts = tables["orders"]["order_status"].value_counts().reset_index()
    status_counts.columns = ["order_status", "orders"]
    fig = plt.figure(figsize=(8, 4.5))
    sns.barplot(data=status_counts, x="order_status", y="orders")
    plt.xticks(rotation=45)
    plt.title("Phân bố trạng thái đơn hàng")
    plt.xlabel("Trạng thái")
    plt.ylabel("Số đơn")
    save(fig, "eda_order_status_distribution.png")

    category = (
        features.groupby("product_category_name_english")
        .agg(
            orders=("order_id", "nunique"),
            revenue=("total_price", "sum"),
            avg_review=("review_score", "mean"),
            delay_rate=("is_delayed", "mean"),
        )
        .sort_values("revenue", ascending=False)
    )
    fig = plt.figure(figsize=(10, 6))
    sns.barplot(data=category.head(12).reset_index(), y="product_category_name_english", x="revenue")
    plt.title("Top danh mục theo doanh thu")
    plt.xlabel("Doanh thu")
    plt.ylabel("Danh mục")
    save(fig, "eda_top_categories_by_revenue.png")

    state_revenue = (
        features.groupby("customer_state")
        .agg(orders=("order_id", "nunique"), revenue=("total_price", "sum"))
        .reset_index()
        .sort_values("revenue", ascending=False)
        .head(15)
    )
    fig = plt.figure(figsize=(9, 5))
    sns.barplot(data=state_revenue, x="customer_state", y="revenue")
    plt.title("Doanh thu theo bang của khách hàng")
    plt.xlabel("Bang khách hàng")
    plt.ylabel("Doanh thu")
    save(fig, "eda_revenue_by_customer_state.png")

    review_counts = features["review_score"].value_counts().sort_index().reset_index()
    review_counts.columns = ["review_score", "orders"]
    fig = plt.figure(figsize=(7, 4.5))
    sns.barplot(data=review_counts, x="review_score", y="orders")
    plt.title("Phân bố điểm review")
    plt.xlabel("Điểm review")
    plt.ylabel("Số đơn")
    save(fig, "eda_review_score_distribution.png")

    delivery_group = features.copy()
    delivery_group["delivery_group"] = (
        delivery_group["is_delayed"]
        .map({0: "Giao đúng hạn", 1: "Giao trễ"})
        .fillna("Không xác định")
    )
    bad_delivery = (
        delivery_group.groupby("delivery_group")
        .agg(
            orders=("order_id", "nunique"),
            bad_review_rate=("bad_review", "mean"),
            avg_delay_days=("delay_days", "mean"),
        )
        .reset_index()
    )
    fig = plt.figure(figsize=(7, 4.5))
    sns.barplot(data=bad_delivery, x="delivery_group", y="bad_review_rate")
    plt.title("Tỷ lệ review xấu theo nhóm giao hàng")
    plt.xlabel("Nhóm giao hàng")
    plt.ylabel("Bad review rate")
    save(fig, "eda_bad_review_by_delivery_group.png")


def generate_cube_images(cubes: dict[str, pd.DataFrame]) -> None:
    cube_shapes = pd.DataFrame(
        [{"cube_theme": name, "rows": cube.shape[0], "columns": cube.shape[1]} for name, cube in cubes.items()]
    )
    fig = plt.figure(figsize=(9, 4.5))
    sns.barplot(data=cube_shapes, x="cube_theme", y="rows")
    plt.xticks(rotation=35, ha="right")
    plt.title("Số pattern được giữ lại theo từng Iceberg Cube")
    plt.xlabel("Chủ đề cube")
    plt.ylabel("Số dòng")
    save(fig, "cube_patterns_by_theme.png")

    delivery_top = (
        cubes["delivery_quality"]
        .sort_values(["bad_review_rate", "count_orders"], ascending=False)
        .head(12)
        .copy()
    )
    delivery_top["pattern"] = (
        delivery_top["seller_state"].astype(str)
        + " | "
        + delivery_top["product_category_name_english"].astype(str)
        + " | delayed="
        + delivery_top["is_delayed"].astype(str)
    )
    fig = plt.figure(figsize=(10, 6))
    sns.barplot(data=delivery_top, y="pattern", x="bad_review_rate")
    plt.title("Top pattern có tỷ lệ review xấu cao")
    plt.xlabel("Bad review rate")
    plt.ylabel("Pattern")
    save(fig, "cube_top_bad_review_patterns.png")


def generate_model_images(model_dataset: pd.DataFrame) -> None:
    pipeline, _ = train_model(model_dataset, model_name="random_forest")
    X = model_dataset[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = model_dataset["bad_review"].astype(int)
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    ConfusionMatrixDisplay.from_predictions(y_test, y_pred, ax=ax, cmap="Blues", colorbar=False)
    ax.set_title("Confusion Matrix")
    save(fig, "model_confusion_matrix.png")

    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    RocCurveDisplay.from_predictions(y_test, y_proba, ax=ax)
    ax.set_title("ROC Curve")
    save(fig, "model_roc_curve.png")

    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    PrecisionRecallDisplay.from_predictions(y_test, y_proba, ax=ax)
    ax.set_title("Precision-Recall Curve")
    save(fig, "model_precision_recall_curve.png")

    preprocess = pipeline.named_steps["preprocess"]
    model = pipeline.named_steps["model"]
    feature_names = preprocess.get_feature_names_out()
    importance = (
        pd.DataFrame({"feature": feature_names, "importance": model.feature_importances_})
        .sort_values("importance", ascending=False)
        .head(20)
    )
    fig = plt.figure(figsize=(10, 6))
    sns.barplot(data=importance, y="feature", x="importance")
    plt.title("Top feature importance")
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    save(fig, "model_feature_importance.png")


def generate_diagrams() -> None:
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.axis("off")
    boxes = {
        "orders": (0.42, 0.55),
        "customers": (0.08, 0.72),
        "order_items": (0.42, 0.30),
        "payments": (0.75, 0.72),
        "reviews": (0.75, 0.50),
        "products": (0.08, 0.30),
        "sellers": (0.75, 0.25),
        "translation": (0.08, 0.08),
        "geolocation": (0.42, 0.08),
    }
    labels = {
        "orders": "orders\norder_id, customer_id\nstatus, timestamps",
        "customers": "customers\ncustomer_id\ncity, state, zip",
        "order_items": "order_items\norder_id, product_id\nseller_id, price, freight",
        "payments": "order_payments\norder_id\npayment_type, value",
        "reviews": "order_reviews\norder_id\nreview_score",
        "products": "products\nproduct_id\ncategory, dimensions",
        "sellers": "sellers\nseller_id\ncity, state, zip",
        "translation": "category_translation\ncategory_name\ncategory_english",
        "geolocation": "geolocation\nzip_prefix\nlat, lng",
    }
    for key, (x, y) in boxes.items():
        ax.text(
            x,
            y,
            labels[key],
            ha="center",
            va="center",
            fontsize=10,
            bbox=dict(boxstyle="round,pad=0.45", facecolor="#eef3ff", edgecolor="#4b6cb7"),
        )

    def arrow(source: str, target: str) -> None:
        ax.annotate("", xy=boxes[target], xytext=boxes[source], arrowprops=dict(arrowstyle="->", color="#333", lw=1.4))

    for source, target in [
        ("customers", "orders"),
        ("orders", "order_items"),
        ("orders", "payments"),
        ("orders", "reviews"),
        ("products", "order_items"),
        ("sellers", "order_items"),
        ("translation", "products"),
        ("geolocation", "customers"),
        ("geolocation", "sellers"),
    ]:
        arrow(source, target)
    ax.set_title("ERD quan hệ giữa các bảng Olist", fontsize=15, fontweight="bold")
    save(fig, "erd_olist_relationships.png")

    fig, ax = plt.subplots(figsize=(12, 7))
    ax.axis("off")
    fact = (0.5, 0.5)
    ax.text(
        *fact,
        "fact_order_items\nprice, freight_value\nreview_score, delivery_days\ndelay_days, is_delayed, bad_review",
        ha="center",
        va="center",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.55", facecolor="#fff0d8", edgecolor="#cc7a00"),
    )
    dims = {
        "dim_date": (0.5, 0.85),
        "dim_customer": (0.15, 0.68),
        "dim_seller": (0.85, 0.68),
        "dim_product": (0.15, 0.32),
        "dim_payment": (0.85, 0.32),
        "dim_order_status": (0.5, 0.15),
    }
    for name, (x, y) in dims.items():
        ax.text(
            x,
            y,
            name,
            ha="center",
            va="center",
            fontsize=11,
            bbox=dict(boxstyle="round,pad=0.45", facecolor="#e8f8ef", edgecolor="#2e8b57"),
        )
        ax.annotate("", xy=fact, xytext=(x, y), arrowprops=dict(arrowstyle="->", lw=1.5, color="#333"))
    ax.set_title("Star Schema của Olist Data Warehouse", fontsize=15, fontweight="bold")
    save(fig, "dwh_star_schema.png")

    fig, ax = plt.subplots(figsize=(12, 4.5))
    ax.axis("off")
    stages = [
        ("CSV Dataset", "9 Olist CSV files"),
        ("ETL / Preprocessing", "pandas + feature engineering"),
        ("Data Warehouse", "PostgreSQL / SQL Server"),
        ("Analytics", "Iceberg Cube + ML model"),
        ("Application", "FastAPI + Streamlit"),
    ]
    xs = [0.08, 0.29, 0.50, 0.71, 0.92]
    for (title, subtitle), x in zip(stages, xs):
        ax.text(
            x,
            0.55,
            f"{title}\n{subtitle}",
            ha="center",
            va="center",
            fontsize=10,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#f3f6fa", edgecolor="#555"),
        )
    for x1, x2 in zip(xs[:-1], xs[1:]):
        ax.annotate("", xy=(x2 - 0.08, 0.55), xytext=(x1 + 0.08, 0.55), arrowprops=dict(arrowstyle="->", lw=1.8))
    ax.set_title("Kiến trúc tổng thể hệ thống Olist Analytics", fontsize=15, fontweight="bold")
    save(fig, "system_architecture.png")


def main() -> None:
    configure_fonts()
    tables = load_olist_tables()
    features = build_order_features(tables)
    model_dataset = build_model_dataset(features)
    cubes = compute_default_olist_cubes(features)

    generate_eda_images(features, tables)
    generate_cube_images(cubes)
    generate_model_images(model_dataset)
    generate_diagrams()


if __name__ == "__main__":
    main()
