from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)
BASE_API_URL = "http://mysql_apifahasa:8002"

TEMPLATE = '''
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <title>BÀI TẬP CUỐI KỲ CHUYÊN ĐỀ CƠ SỞ DỮ LIỆU</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />
  <style>
    body {
      background-color: #f5f5f5;
    }
    .header {
      background-color: #343a40;
      color: white;
      padding: 20px;
      text-align: center;
      font-weight: bold;
      font-size: 24px;
    }
    .sidebar {
      background: white;
      padding: 15px;
      margin-top: 10px;
      border-radius: 5px;
      box-shadow: 0 0 10px rgba(0,0,0,0.1);
      max-width: 300px;
    }
    .product-card img {
      object-fit: cover;
      height: 220px;
      width: 100%;
      border-radius: 5px 5px 0 0;
    }
    .price del,
    .price s {
    color: #999;
    font-size: 0.9rem;
    }
    .price {
      font-weight: bold;
      color: #d9534f;
      font-size: 1.1rem;
      margin: 5px 0;
    }
    .product-title {
        font-weight: 600;
        font-size: 1rem;
        line-height: 1.4em;               
        max-height: 2.8em;            
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
    }
    .banner {
      width: 100%;
      margin-top: 20px;
      border-radius: 10px;
    }
  </style>
</head>
<body>
  <div class="header">BÀI TẬP CUỐI KỲ CHUYÊN ĐỀ CƠ SỞ DỮ LIỆU</div>

  <div class="container mt-4">
    <img src="https://cdn1.fahasa.com/media/wysiwyg/Thang-03-2024/HSO_DoChoiT324_Slide_840x320.jpg" class="banner" alt="Banner" />
    <p class="mt-2 fw-semibold text-muted">Số lượng sản phẩm: {{ products|length }}</p>
  </div>

  <div class="container my-4">
    <div class="row">
      <div class="col-md-3 mb-4">
        <div class="sidebar">
          <h5>Bộ Lọc</h5>
          <form method="get" class="row g-3">
            <div class="mb-3">
              <label class="form-label fw-semibold">Lọc theo giá</label><br>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" name="price" value="0-150000" id="price1"
                {% if '0-150000' in price %} checked {% endif %}>
                <label class="form-check-label" for="price1">0đ - 150,000đ</label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" name="price" value="150000-300000" id="price2"
                {% if '150000-300000' in price %} checked {% endif %}>
                <label class="form-check-label" for="price2">150,000đ - 300,000đ</label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" name="price" value="300000-500000" id="price3"
                {% if '300000-500000' in price %} checked {% endif %}>
                <label class="form-check-label" for="price3">300,000đ - 500,000đ</label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" name="price" value="500000-700000" id="price4"
                {% if '500000-700000' in price %} checked {% endif %}>
                <label class="form-check-label" for="price4">500,000đ - 700,000đ</label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="checkbox" name="price" value="700000-999999999" id="price5"
                {% if '700000-999999999' in price %} checked {% endif %}>
                <label class="form-check-label" for="price5">700,000đ - Trở lên</label>
              </div>
            </div>

            <div class="mb-3">
              <label for="supplierInput" class="form-label fw-semibold">Nhà cung cấp</label>
              <input
                id="supplierInput"
                type="text"
                name="supplier"
                class="form-control"
                placeholder="Nhập tên nhà cung cấp"
                value="{{ supplier }}"
              />
            </div>

            <button type="submit" class="btn btn-primary w-100">Áp dụng lọc</button>
          </form>
        </div>
      </div>

      <div class="col-md-9">
        <form method="get" class="row g-2 align-items-center mb-3">
          <div class="col-9 col-sm-10">
            <input
              type="text"
              name="search"
              class="form-control"
              placeholder="Tìm kiếm sản phẩm..."
              value="{{ search }}"
            />
          </div>
          <div class="col-3 col-sm-2">
            <button type="submit" class="btn btn-primary w-100">Tìm kiếm</button>
          </div>
        </form>

        <div id="product-container" class="row row-cols-1 row-cols-md-4 g-4">
          {% if products %}
            {% for product in products %}
              <div class="col">
                <div class="card product-card h-100 shadow-sm">
                  <img src="{{ product['hinh'] }}" alt="{{ product['ten'] }}" />
                  <div class="card-body">
                    <h5 class="product-title">{{ product['ten'] }}</h5>
                    <p class="price">{{ "{:,.0f}".format(product['giaBan']) }} đ</p>
                    <p class="price"><s>{{ "{:,.0f}".format(product['giaGoc']) }} đ</s></p>
                    <p class="text-muted">{{ product['noiSX'] }}</p>
                  </div>
                </div>
              </div>
            {% endfor %}
          {% else %}
            <p class="text-center mt-4">Không có sản phẩm phù hợp.</p>
          {% endif %}
        </div>
      </div>
    </div>
  </div>
</body>
</html>
'''

@app.route('/')
def index():
    search = request.args.get('search', '')
    prices = request.args.getlist('price')  # list các khoảng giá checkbox tick
    supplier = request.args.get('supplier', '')

    if search:
        url = f"{BASE_API_URL}/dochoi/search?ten={search}"
    else:
        url = f"{BASE_API_URL}/dochoi"

    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        print("Lỗi gọi API:", e)
        data = []

    filtered = []
    for item in data:
        price_value = item.get('giaBan', 0)
        supplier_name = item.get('noiSX', '').lower()

        if supplier and supplier.lower() not in supplier_name:
            continue

        if prices:
            matched = False
            for p in prices:
                try:
                    pmin, pmax = map(int, p.split('-'))
                    if pmin <= price_value <= pmax:
                        matched = True
                        break
                except:
                    pass
            if not matched:
                continue

        filtered.append(item)

    return render_template_string(TEMPLATE, products=filtered, search=search, price=prices, supplier=supplier)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
