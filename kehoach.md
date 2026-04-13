### MVP (Hoàn thành trước 12.04.2026)

#### 1) Mục tiêu MVP
MVP tập trung vào các chức năng cốt lõi của một website bán hàng: khách hàng có thể xem sản phẩm và tạo đơn hàng; quản trị viên có thể quản lý dữ liệu nền (danh mục, sản phẩm, phương thức thanh toán) và theo dõi đơn hàng. MVP ưu tiên “chạy được end-to-end” và đảm bảo đúng luồng nghiệp vụ hơn là tối ưu giao diện hoặc bổ sung tính năng nâng cao.

#### 2) Các chức năng MVP sẽ thực hiện

**A. Chức năng phía khách hàng (Customer)**
- Đăng ký tài khoản, đăng nhập và nhận JWT token.
- Xem danh sách sản phẩm, xem chi tiết sản phẩm.
- Giỏ hàng phía client (frontend demo lưu LocalStorage): thêm/xóa/cập nhật số lượng.
- Checkout tạo đơn hàng:
  - Chọn phương thức thanh toán (đọc từ API).
  - Nhập địa chỉ giao hàng (shipping_address).
  - Gửi tạo đơn gồm nhiều sản phẩm (order items).
- Xem danh sách đơn hàng của chính mình và xem chi tiết đơn.
- Quản lý thông tin cá nhân (xem/cập nhật) theo đúng tài khoản đăng nhập.

**B. Chức năng phía quản trị (Admin)**
- Đăng nhập admin và nhận JWT token (bearer).
- Quản lý danh mục (CRUD): tạo/sửa/xóa; khách hàng chỉ được xem.
- Quản lý sản phẩm (CRUD): tạo/sửa/xóa; khách hàng chỉ được xem.
- Quản lý phương thức thanh toán (CRUD): để hỗ trợ checkout.
- Quản lý đơn hàng:
  - Xem danh sách đơn, xem chi tiết đơn.
  - Cập nhật trạng thái đơn hàng (ví dụ: Pending/Confirmed/Shipping/Completed/Canceled).

**C. Ràng buộc và quy tắc nghiệp vụ tối thiểu**
- Email khách hàng là duy nhất (không cho đăng ký trùng).
- Khách hàng chỉ được thao tác dữ liệu của chính mình (đúng `customer_id` theo token).
- Đơn hàng phải có ít nhất 1 item, số lượng mua > 0, sản phẩm và phương thức thanh toán phải tồn tại.

#### 3) Kế hoạch kiểm thử (cho MVP)

**3.1. Mục tiêu kiểm thử**
- Xác nhận API hoạt động đúng chức năng và đúng phân quyền.
- Xác nhận luồng nghiệp vụ chính chạy end-to-end: đăng ký → đăng nhập → xem sản phẩm → checkout → xem đơn.
- Phát hiện lỗi validate dữ liệu, lỗi xử lý nghiệp vụ và lỗi kết nối frontend-backend.

**3.2. Phạm vi kiểm thử**
- Backend API (FastAPI): routers + service + database transaction.
- Auth/Authorization: JWT cho customer và admin.
- Frontend demo: kiểm tra gọi API, xử lý token, giỏ hàng và checkout.

**3.3. Hình thức kiểm thử**
- **Kiểm thử API (tự động):** dùng `pytest` + `fastapi.testclient` cho các endpoint quan trọng.
- **Kiểm thử tích hợp (bán tự động):** chạy backend và thao tác trên frontend demo theo checklist (Happy path).
- **Kiểm thử thủ công (manual):** kiểm tra giao diện, thông báo lỗi, các trường hợp nhập sai dữ liệu.

**3.4. Danh sách test case gợi ý**
1) **Customer – Register/Login**
   - Đăng ký thành công.
   - Đăng ký trùng email → báo lỗi.
   - Đăng nhập đúng mật khẩu → trả token.
   - Đăng nhập sai mật khẩu → báo lỗi.
2) **Authorization**
   - Không có token gọi endpoint protected → 401.
   - Customer gọi API của customer khác (`/customers/{id}`) → 403.
   - Customer gọi API admin-only (POST/PUT/DELETE products, categories, payment-methods) → 401/403.
3) **Products/Categories/Payment methods**
   - GET list và GET detail trả dữ liệu đúng.
   - Admin CRUD thành công; kiểm tra dữ liệu thay đổi sau CRUD.
4) **Orders**
   - Tạo order với danh sách items hợp lệ → 201.
   - Tạo order với items rỗng → báo lỗi.
   - Tạo order với quantity <= 0 → báo lỗi.
   - Tạo order với product_id không tồn tại → báo lỗi.
   - Customer xem danh sách đơn của mình → đúng dữ liệu.
   - Customer truy cập order của người khác → 403.
5) **Frontend demo (End-to-end)**
   - Từ `index/products` → `product-detail` → add cart → `checkout` → tạo order thành công.
   - Sau khi tạo order, kiểm tra `orders` hiển thị trong lịch sử.

**3.5. Dữ liệu & môi trường kiểm thử**
- Database PostgreSQL (theo `.env`), chạy migration bằng Alembic trước khi test thủ công.
- Tạo sẵn tối thiểu:
  - 1 Category
  - 3–5 Products
  - 1 Payment method (ví dụ: COD)

**3.6. Tiêu chí hoàn thành MVP (Definition of Done)**
- Tất cả luồng nghiệp vụ chính chạy được end-to-end trên máy cục bộ.
- Các lỗi nghiêm trọng (crash, sai phân quyền, tạo order sai) được xử lý.
- Swagger hiển thị đầy đủ endpoint; API trả về mã lỗi hợp lý.
- Có checklist kiểm thử và kết quả test ghi nhận (đạt/không đạt) cho các test case quan trọng.

#### 4) Chức năng dự trù cho phase kế tiếp (sau MVP)
- Trừ tồn kho khi tạo đơn + kiểm tra số lượng tồn.
- Chuẩn hóa trạng thái đơn hàng (rule chuyển trạng thái) và bổ sung lịch sử thay đổi trạng thái.
- Tăng cường quản trị:
  - Lưu admin trong CSDL, hỗ trợ nhiều admin và phân quyền theo role.
  - Trang quản trị riêng (UI) thay vì chỉ thao tác trên Swagger.
- Tìm kiếm/lọc sản phẩm nâng cao (theo giá, theo danh mục, theo keyword).
- Khuyến mãi/mã giảm giá và tính tổng tiền chuẩn hóa (subtotal, shipping, discount, total).
- Bảo mật nâng cao: đổi mật khẩu, quên mật khẩu, xác thực email (mức demo).
- Báo cáo thống kê cơ bản: doanh thu theo ngày/tháng, top sản phẩm.

---

### Beta Version (Chậm nhất 10.05.2026)

#### 1) Mục tiêu Beta
Beta hướng đến việc ổn định hệ thống, hoàn thiện tài liệu báo cáo và bổ sung một số tính năng nâng cao theo mức độ ưu tiên. Ngoài việc “chạy được”, Beta cần thể hiện sự kiểm soát chất lượng thông qua kết quả kiểm thử và tổng hợp lỗi.

#### 2) Kết quả kiểm thử (cách trình bày đề xuất)
Trong giai đoạn Beta, em sẽ tổng hợp kết quả kiểm thử theo dạng bảng, ví dụ:
- Danh sách test case (ID, mô tả, dữ liệu test, kết quả mong đợi).
- Kết quả thực tế (Pass/Fail) và ghi chú (nếu Fail thì kèm nguyên nhân/ảnh chụp/trace).
- Thống kê lỗi:
  - Số lỗi theo mức độ (Critical/Major/Minor)
  - Tỉ lệ đã fix, lỗi còn tồn
  - Ghi nhận regression test sau khi sửa

Ngoài ra, ưu tiên có ít nhất:
- 01 lần chạy kiểm thử end-to-end đầy đủ (happy path).
- 01 lần kiểm thử phân quyền (customer vs admin) và các trường hợp nhập sai dữ liệu.

#### 3) Viết báo cáo (nội dung chính)
Báo cáo Beta nên gồm các phần:
1) Giới thiệu đề tài, mục tiêu, phạm vi.
2) Phân tích yêu cầu (actors, FR/NFR, quy tắc nghiệp vụ).
3) Thiết kế hệ thống:
   - Kiến trúc tổng thể
   - Thiết kế CSDL (ERD, bảng, quan hệ)
   - Thiết kế API và phân quyền
4) Triển khai:
   - Công nghệ sử dụng
   - Cấu trúc project (router/service/model/schema)
   - Mô tả các module chính
5) Kiểm thử:
   - Kế hoạch kiểm thử
   - Kết quả kiểm thử (bảng + nhận xét)
6) Kết luận và hướng phát triển.

#### 4) Thời hạn hoàn thành dự kiến
- Hoàn thành MVP: **12.04.2026**
- Hoàn thành Beta Version (báo cáo + kết quả kiểm thử + cải tiến): **chậm nhất 10.05.2026**

