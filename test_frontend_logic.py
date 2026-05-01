import requests
import time

FE_URL = "http://127.0.0.1:8080"
ADMIN_EMAIL = "admin@shop.com"
ADMIN_PASS = "admin12345"

def test_frontend():
    print("--- BẮT ĐẦU KIỂM THỬ FRONTEND ---")
    session = requests.Session()

    # 1. Kiểm tra truy cập trang Dashboard khi chưa đăng nhập (Phải bị redirect)
    print("TC-03: Kiểm tra Protected Route...")
    resp = session.get(f"{FE_URL}/", allow_redirects=True)
    if "login" in resp.url:
        print(" -> Đạt: Đã redirect về trang login.")
    else:
        print(f" -> Thất bại: Không redirect. URL hiện tại: {resp.url}")

    # 2. Đăng nhập
    print("TC-01: Kiểm tra Đăng nhập...")
    # Lấy CSRF token nếu cần (Django mặc định yêu cầu)
    session.get(f"{FE_URL}/login/")
    csrf_token = session.cookies.get('csrftoken')
    
    login_data = {
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASS,
        "csrfmiddlewaretoken": csrf_token
    }
    resp = session.post(f"{FE_URL}/login/", data=login_data, headers={"Referer": f"{FE_URL}/login/"})
    
    if resp.status_code == 200 and "Tổng quan" in resp.text:
        print(" -> Đạt: Đăng nhập thành công và vào được Dashboard.")
    else:
        print(f" -> Thất bại: Đăng nhập không thành công. Code: {resp.status_code}")

    # 3. Kiểm tra trang Danh mục
    print("TC-05: Kiểm tra hiển thị Danh mục...")
    resp = session.get(f"{FE_URL}/categories/")
    if "Áo Thun" in resp.text and "Sơ Mi" in resp.text:
        print(" -> Đạt: Danh sách danh mục hiển thị đúng dữ liệu từ API.")
    else:
        print(" -> Thất bại: Không tìm thấy dữ liệu danh mục.")

    # 4. Kiểm tra trang Sản phẩm
    print("TC-09: Kiểm tra hiển thị Sản phẩm...")
    resp = session.get(f"{FE_URL}/products/")
    if "Áo Thun Oversize Streetwear" in resp.text:
        print(" -> Đạt: Danh sách sản phẩm hiển thị đúng.")
    else:
        print(" -> Thất bại: Không tìm thấy dữ liệu sản phẩm.")

    # 5. Kiểm tra Đăng xuất
    print("TC-04: Kiểm tra Đăng xuất...")
    session.get(f"{FE_URL}/logout/")
    resp = session.get(f"{FE_URL}/", allow_redirects=False)
    if resp.status_code == 302:
        print(" -> Đạt: Đã đăng xuất và bảo vệ trang chủ.")
    else:
        print(" -> Thất bại: Vẫn có thể truy cập sau khi đăng xuất.")

    print("--- KIỂM THỬ FRONTEND HOÀN TẤT ---")

if __name__ == "__main__":
    # Đợi server khởi động
    time.sleep(3)
    try:
        test_frontend()
    except Exception as e:
        print(f"Lỗi khi chạy test: {e}")
