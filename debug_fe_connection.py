from dashboard.utils import call_api
import json

def debug():
    print("--- ĐANG KIỂM TRA KẾT NỐI FE -> BE ---")
    # 1. Thử đăng nhập
    data, status = call_api('POST', '/login', data={'email': 'admin@shop.com', 'password': 'admin12345'})
    if status != 200:
        print(f"LỖI: Đăng nhập thất bại (Status {status}). Chi tiết: {data}")
        return
    
    token = data.get('access_token')
    print("-> Đăng nhập thành công.")

    # 2. Thử lấy danh mục
    cats, status_cat = call_api('GET', '/admin/categories', token=token)
    print(f"-> API Categories Status: {status_cat}")
    if isinstance(cats, list):
        print(f"-> Số lượng danh mục lấy được: {len(cats)}")
    else:
        print(f"-> LỖI: API không trả về danh sách. Kết quả: {cats}")

    # 3. Thử lấy sản phẩm
    prods, status_prod = call_api('GET', '/admin/products', token=token)
    print(f"-> API Products Status: {status_prod}")
    if isinstance(prods, list):
        print(f"-> Số lượng sản phẩm lấy được: {len(prods)}")
    else:
        print(f"-> LỖI: API không trả về danh sách. Kết quả: {prods}")

if __name__ == "__main__":
    debug()
