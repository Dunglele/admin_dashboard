from django.shortcuts import render, redirect
from django.contrib import messages
from .utils import call_api

# --- Authentication ---
def login_view(request):
    if request.session.get('access_token'):
        return redirect('dashboard')
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        data, status_code = call_api("POST", "/login", data={"email": email, "password": password})
        if status_code == 200:
            request.session['access_token'] = data['access_token']
            request.session['admin_email'] = email
            request.session['admin_name'] = "Administrator"
            messages.success(request, "Đăng nhập thành công!")
            return redirect('dashboard')
        else:
            messages.error(request, data.get('detail', 'Đăng nhập thất bại'))
    return render(request, 'dashboard/login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')

# --- Main Dashboard ---
def dashboard_view(request):
    token = request.session.get('access_token')
    if not token: return redirect('login')
    
    prods, _ = call_api("GET", "/admin/products", token=token)
    cats, _ = call_api("GET", "/admin/categories", token=token)
    orders, _ = call_api("GET", "/admin/orders", token=token)
    users, _ = call_api("GET", "/admin/users", token=token)
    
    context = {
        'total_products': len(prods) if isinstance(prods, list) else 0,
        'total_categories': len(cats) if isinstance(cats, list) else 0,
        'total_orders': len(orders) if isinstance(orders, list) else 0,
        'total_users': len(users) if isinstance(users, list) else 0,
    }
    return render(request, 'dashboard/index.html', context)

# --- Category Management ---
def categories_view(request):
    token = request.session.get('access_token')
    if not token: return redirect('login')
    
    if request.method == "POST":
        action = request.POST.get('action')
        if action == "create":
            name = request.POST.get('name')
            image_url = request.POST.get('image_url')
            _, status_code = call_api("POST", "/admin/categories", token=token, data={"name": name, "image_url": image_url})
            if status_code == 200: messages.success(request, "Thêm danh mục thành công!")
            else: messages.error(request, "Lỗi khi thêm danh mục")
        
        elif action == "delete":
            cat_id = request.POST.get('id')
            _, status_code = call_api("DELETE", f"/admin/categories/{cat_id}", token=token)
            if status_code == 200: messages.success(request, "Xóa danh mục thành công!")
            else: messages.error(request, "Lỗi khi xóa danh mục")

    cats, status_code = call_api("GET", "/admin/categories", token=token)
    if status_code != 200:
        cats = []
        messages.error(request, "Không thể tải danh mục từ hệ thống.")
    return render(request, 'dashboard/categories.html', {'categories': cats})

# --- Product Management ---
def products_view(request):
    token = request.session.get('access_token')
    if not token: return redirect('login')
    
    if request.method == "POST":
        action = request.POST.get('action')
        if action == "create":
            data = {
                "name": request.POST.get('name'),
                "description": request.POST.get('description'),
                "price": float(request.POST.get('price')),
                "stock": int(request.POST.get('stock')),
                "image_url": request.POST.get('image_url'),
                "size": request.POST.get('size'),
                "color": request.POST.get('color'),
                "category_id": int(request.POST.get('category_id')),
            }
            _, status_code = call_api("POST", "/admin/products", token=token, data=data)
            if status_code == 200: messages.success(request, "Thêm sản phẩm thành công!")
            else: messages.error(request, "Lỗi khi thêm sản phẩm")
            
        elif action == "delete":
            prod_id = request.POST.get('id')
            _, status_code = call_api("DELETE", f"/admin/products/{prod_id}", token=token)
            if status_code == 200: messages.success(request, "Xóa sản phẩm thành công!")
            else: messages.error(request, "Lỗi khi xóa sản phẩm")

    prods, _ = call_api("GET", "/admin/products", token=token)
    cats, _ = call_api("GET", "/admin/categories", token=token)
    return render(request, 'dashboard/products.html', {'products': prods, 'categories': cats})

# --- Order Management ---
def orders_view(request):
    token = request.session.get('access_token')
    if not token: return redirect('login')
    
    if request.method == "POST":
        order_id = request.POST.get('id')
        new_status = request.POST.get('status')
        _, status_code = call_api("PATCH", f"/admin/orders/{order_id}/status", token=token, data={"status": new_status})
        if status_code == 200: messages.success(request, "Cập nhật trạng thái đơn hàng thành công!")
    
    orders, _ = call_api("GET", "/admin/orders", token=token)
    return render(request, 'dashboard/orders.html', {'orders': orders})

# --- User Management ---
def users_view(request):
    token = request.session.get('access_token')
    if not token: return redirect('login')
    
    users, _ = call_api("GET", "/admin/users", token=token)
    return render(request, 'dashboard/users.html', {'users': users})
