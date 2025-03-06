from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# Link các hướng dẫn
ACTIONS_DATA = {
    "tải phần mềm": {
        "name": "<b>Phần mềm Quản Lý Hụi</b> của em chạy trên nền tảng web nên Anh/Chị không cần tải về để sử dụng. Để truy cập vào phần mềm Quản Lý Hụi, Anh/Chị hãy làm theo các bước sau:",
        "details": "<b>Bước 1:</b> Anh/Chị hãy mở trình duyệt web (Cốc Cốc, Chrome, Edge,...). <br><br>" +
                   "<b>Bước 2:</b> Truy cập vào địa chỉ <b>'phanmemhui.com'</b>.<br><br>" +
                   "<b>Bước 3:</b> Tiếp đến, Anh/Chị hãy bấm vào nút 'MỞ PHẦN MỀM QUẢN LÝ HỤI' màu xanh lá.",
        "link": ""
    },
    "sử dụng phần mềm": {
        "name": "sử dụng phần mềm",
        "details": "Chào Anh/Chị, em có đăng rất nhều video hướng dẫn sử dụng <b>Phần mềm Quản Lý Hụi</b> bên kênh Youtube. Anh/Chị hãy truy câp vào kênh Youtube bên dưới để xem các video hướng dẫn sử dụng phần mềm nhé",
        "link": "https://www.youtube.com/@congtyphanmemtotnhat8496/shorts"
    },
    "hốt hụi": {
        "name": "hốt hụi",
        "details": "<b>Bước 1:</b> Anh/Chị hãy chọn vào mục <b>QUẢN LÝ HỤI</b>.<br><br>"
                   "<b>Bước 2:</b> Chọn <b>dây hụi cần hốt</b>. <br><br>"
                   "<b>Bước 3:</b> Bấm vào nút <b>HỐT HỤI</b>. <br><br>"
                   "<b>Bước 4:</b> Anh/Chị hãy chọn <b>Người hốt</b>. Sau đó <b>Ghi tiền thăm</b>. Chọn ngày hốt rồi bấm <b>OK</b><br>"
                   "(chỗ ngày hốt có thể lùi ngày nếu cho hốt lại các kỳ cũ) <br><br>"
                   "<b>Bước 5:</b> Sau khi đã điền đầy đủ thông tin, Anh/Chị hãy bấm <b>XÁC NHẬN HỐT HỤI</b>. Phần mềm sẽ tính số tiền hụi viên cần đóng, Anh/Chị hãy chờ vài giây cho phần mềm xử lý xong nhé. <br><br>"
                   "<b>Bước 6:</b> Bấm <b>In toa hốt</b> để gửi phiếu giao hụi. Sau đó hãy bấm vào nút  <img src='img/1358023.png' width='16px'>  ở bên trái màng hình để chia sẽ phiếu cho khách. <br>"
                   "(Anh/Chị có thể chọn chia sẽ qua Zalo hoặc Messager cho khách hàng)<br><br>"
                   "<b>Bước 7:</b> Vuốt màng hình từ trái qua phải để quay về.",
        "link": "https://www.youtube.com/watch?v=Yn8LgiFjy3g"
    },
    "đóng hụi": {
        "name": "đóng hụi",
        "details": "<b>Bước 1:</b> Bấm vào mục <b>Hụi cần đóng trong ngày </b> <br><br>"
                   "<b>Bước 2:</b> Chọn <b>Xem dữ liệu</b>. Phần mềm sẽ tải các dữ liệu hụi viên cần đóng, Anh/Chị hãy chờ vài giây cho phần mềm xử lý xong nhé. <br><br>"
                   "<b>Bước 3:</b> Bấm vào nút <b>IN PHIẾU</b> để xem phiếu đóng hụi. <br><br>"
                   "<b>Bước 4:</b> Bấm vào nút <b>XÁC NHẬN VÀ IN PHIẾU</b>, phần mềm sẽ hiển thị phiếu đóng hụi tạm tính. Sau đó hãy bấm vào nút  <img src='img/1358023.png' width='16px'>  ở bên trái màng hình để chia sẽ phiếu cho khách. <br>"
                   "(Anh/Chị có thể chọn chia sẽ qua Zalo hoặc Messager cho khách hàng)<br><br>"
                   "<b>Bước 5:</b> Vuốt màng hình từ trái qua phải để quay về. <br>"
                   "(Hụi viên đã đóng hụi sẽ được <b>Gạch</b> và ghi <b>Đã đóng hụi</b>)",
        "link": "https://www.youtube.com/watch?v=SSxNbCxp1EY"
    },
    "tất toán hụi chết": {
        "name": "tất toán hụi chết",
        "details": "<b>Bước 1:</b> Chọn vào mục <b>Chức năng</b>.<br><br>"
                   "<b>Bước 2:</b> Chọn <b>Tất toán hụi chết</b>.<br><br>"
                   "<b>Bước 3:</b> Chọn <b>Hụi viên cần tất toán</b>. Sau đó chọn <b>Dây hụi cần tất toán</b><br><br>"
                   "<b>Bước 4:</b> Bấm <b>XÁC NHẬN ĐÓNG HỤI</b>.<br><br>"
                   "<b>Bước 5:</b> Thông báo tất toán thành công sẽ hiện lên, bấm vào nút <b>OK</b> để kết thúc quá trình tất toán.",
        "link": "https://www.youtube.com/shorts/jJf87pcf23c"
    },
    "in tất cả bill đóng trong ngày": {
        "name": "in tất cả bill đóng trong ngày",
        "details": "<b>Bước 1:</b> Chọn vào <b>HỤI CẦN ĐÓNG</b>.<br><br>"
                   "<b>Bước 2:</b> Bấm nút <b>IN TẤT CẢ</b> màu xanh dương. Phần mềm sẽ hiện thị tất cả các bill trong ngày, phần mềm sẽ vài giây để xử lý, <b>Anh/Chị hãy chờ đến khi thanh màu xanh lá phía dưới biến mất hãy thao tác tiếp nhé</b>.<br><br>"
                   "<b>Bước 3:</b> Bấm vào nút <b>Chia sẽ ZALO</b> để chia sẽ bill đóng.<br>"
                   "(Anh/Chị có thể chọn chia sẽ qua Zalo hoặc Messager cho khách hàng)",
        "link": "https://www.youtube.com/shorts/nw7WNiRD_RI"
    },
    "xóa hốt hụi": {
        "name": "xóa hốt hụi",
        "details": "<b>Bước 1:</b> Anh/Chị hãy chọn vào mục <b>Quản lý hụi</b>.<br><br>"
                   "<b>Bước 2:</b> Chọn vào <b>HÔT HỤI THEO NGÀY</b>.<br><br>"
                   "<b>Bước 3:</b> Bấm vào <b>người hốt cần xóa</b>."
                   "<b>Bước 4:</b> Bấm vào nút <b>XÓA DỮ LIỆU</b>.<br><br>"
                   "<b>Bước 5:</b> Bấm <b>OK</b> để xác nhận xóa, sau đó bấm <b>OK, xóa đóng hụi</b>.",
        "link": "https://www.youtube.com/shorts/nxlwQEc61YU"
    },
    "gom hụi viên bị trùng": {
        "name": "gom hụi viên bị trùng",
        "details": "<b>Bước 1:</b> Chọn vào <b>THÔNG TIN HỤI VIÊN</b>.<br><br>"
                   "<b>Bước 2:</b> Tìm tên hụi viện bị trùng. <br><br>"
                   "<b>Bước 3:</b> Chọn hụi viên cần gom.<br><br>"
                   "<b>Bước 4:</b> Bấm vào nút <b>CHUYỂN THÔNG TIN</b>.<br><br>"
                   "<b>Bước 5:</b> Chọn hụi viên muốn gom thành, Sau đó bấm nút <b>LƯU</b>.<br><br>"
                   "<b>Bước 6:</b> Bấm <b>OK</b> để xác nhận gom, thông báo gom thành công sẽ hiện lên, bấm <b>OK</b>.<br><br>"
                   "<b>Bước 7:</b> Bấm <b>XÓA</b> để loại bỏ hụi viên bị trùng. Sau đó bấm <b>OK</b> để xác nhận xóa hụi viên bị trùng.",
        "link": "https://www.youtube.com/shorts/9VFWoRkcFXI"
    },
    "thêm số phần hụi trong dây hụi": {
        "name": "thêm số phần hụi trong dây hụi",
        "details": "<b>Bước 1:</b> Anh/Chị hãy chọn vào mục <b>QUẢN LÝ HỤI</b>.<br><br>"
                   "<b>Bước 2:</b> Chọn vào <b>Dây hụi cần thay đổi.<br><br></b>"
                   "<b>Bước 3:</b> Chỉnh <b>Số phần (kỳ hốt)</b> lại theo nhu cầu của Anh/Chị. Sau đó bấm vào <b>Dấu + màu xanh lá</b>.<br><br>"
                   "<b>Bước 4:</b> kéo lên, sau đó nhập tên hụi viên mới vào <b>Phần trống vào được thêm vào</b>.<br><br>"
                   "<b>Bước 5:</b> Bấm <b>LƯU THÔNG TIN</b> để hoàn tất.",
        "link": "https://www.youtube.com/shorts/Yuup3Vt0YWU"
    },
    "giảm số phần hụi trong dây hụi": {
        "name": "giảm số phần hụi trong dây hụi",
        "details": "<b>Bước 1:</b> Anh/Chị hãy chọn vào mục <b>QUẢN LÝ HỤI</b>.<br><br>"
                   "<b>Bước 2:</b> Chọn vào <b>Dây hụi cần thay đổi</b>.<br><br>"
                   "<b>Bước 3:</b> kéo lên, bấm vào nút  <img src='img/3515498.png' width='16px'>  bên cạnh tên hội viên cần giảm.<br><br>"
                   "<b>Bước 4:</b> Chỉnh <b>Số phần (kỳ hốt)</b> lại theo nhu cầu của Anh/Chị.<br><br>"
                   "<b>Bước 5:</b> Bấm <b>LƯU THÔNG TIN</b> để hoàn tất.",
        "link": "https://www.youtube.com/shorts/Yuup3Vt0YWU"
    },
    "thay đổi hụi viên trong dây hụi": {
        "name": "thay đổi hụi viên trong dây hụi",
        "details": "<b>Bước 1:</b> Anh/Chị hãy chọn vào mục <b>QUẢN LÝ HỤI</b>.<br><br>"
                   "<b>Bước 2:</b> Chọn vào <b>Dây hụi cần thay đổi</b>.<br><br>"
                   "<b>Bước 3:</b> kéo lên, sau đó bấm vào <b>THAY ĐỔI THÔNG TIN HỤI VIÊN</b>.<br><br>"
                   "<b>Bước 4:</b> Chọn vào tên hụi viên cần thay đổi rồi sửa.<br><br>"
                   "<b>Bước 5:</b> Bấm <b>LƯU THÔNG TIN</b> để hoàn tất.",
        "link": "https://www.youtube.com/shorts/Yuup3Vt0YWU"
    },
    "hốt hụi nhiều người cùng kỳ": {
        "name": "hốt hụi nhiều người cùng kỳ",
        "details": "<b>Bước 1:</b> Anh/Chị hãy chọn vào mục <b>QUẢN LÝ HỤI</b>.<br><br>"
                   "<b>Bước 2:</b> Chọn vào <b>Dây hụi cần thay đổi</b>.<br><br>"
                   "<b>Bước 3:</b> Chọn <b>HỐT HỤI</b>.<br><br>"
                   "<b>Bước 4:</b> kiểm tra lại kỳ hụi muốn thêm người hốt.<br>"
                   "(Nếu kỳ hụi đã có người hốt thì sẽ có cảnh báo xuất hiện, bấm <b>OK</b> để tiếp tục)<br><br>"
                   "<b>Bước 5:</b> Chọn <b>Hụi viên sẽ hốt</b>.<br>"
                   "(Nếu kỳ hụi đã có người hốt thì sẽ có cảnh báo xuất hiện, bấm <b>OK</b> để tiếp tục)<br><br>"
                   "<b>Bước 6:</b> Nhập tiền thăm và bấm <b>XÁC NHẬN HỐT HỤI</b>.<br>"
                   "(Sau đó Anh/Chị có thể bấm vào <b>IN TOA HỐT</b> để chia sẽ phiếu hốt. Bấm vào nút  <img src='img/1358023.png' width='16px'>  ở bên trái màng hình để chia sẽ qua Zalo)",
        "link": "https://www.youtube.com/shorts/MNswWfmdWHQ"
    },
    "xóa tất toán hụi chết": {
        "name": "xóa tất toán hụi chết",
        "details": "<b>Bước 1:</b> Anh/Chị hãy chọn vào mục <b>QUẢN LÝ HỤI</b>.<br><br>"
                   "<b>Bước 2:</b> Chọn vào <b>Đóng hụi theo ngày</b>.<br><br>"
                   "<b>Bước 3:</b> Nếu đã tất toán nhiều ngày trước thì bấm vào lịch chọn ngày tất toán. Tìm dòng <b>Tất toán cần xóa</b>.<br><br>"
                   "<b>Bước 4:</b> Bấm vào dòng <b>Tất toán cần xóa</b>.<br><br>"
                   "<b>Bước 5:</b> Bấm <b>XÓA TẤT CẢ ĐÓNG HỤI</b>, sau đó bấm <b>OK</b> để xác nhận xóa.<br><br>",
        "link": "https://www.youtube.com/shorts/8GfCuW9uKZg"
    },
    "tất toán hụi sống": {
        "name": "tất toán hụi sống",
        "details": "<b>Bước 1:</b> Chọn vào mục <b>Chức năng</b>.<br><br>"
                   "<b>Bước 2:</b> Chọn <b>Tất toán hụi sống</b>.<br><br>"
                   "<b>Bước 3:</b> Chọn hụi viên, sau đó chọn dây hụi.<br><br>"
                   "<b>Bước 4:</b> Nhấn vào dây hụi cần tất toán.<br><br>"
                   "<b>Bước 5:</b> Bấm <b>XEM TRƯỚC TẤT TOÁN</b> (nút màu vàng).<br>"
                   "(Bấm vào nút  <img src='img/1358023.png' width='16px'>  ở bên trái màng hình để chia sẽ phiếu cho khách, Anh/Chị có thể chọn chia sẽ qua Zalo hoặc Messager cho khách hàng)",
        "link": "https://www.youtube.com/shorts/7TJFDykejAU"
    },
    "tạo dây hụi góp": {
        "name": "tạo dây hụi góp",
        "details": "<b>Bước 1:</b> Anh/Chị hãy chọn vào mục <b>QUẢN LÝ HỤI</b>.<br><br>"
                   "<b>Bước 2:</b> Bấm vào <b>Dấu + màu vàng</b> để thêm dây hụi mới.<br><br>"
                   "<b>Bước 3:</b> Điền đầy đủ thông tin dây hụi: Mã số, số tiền dây hụi, số tiền đầu thảo, số phần (kỳ hốt),... Sau đó chọn vào ô <b>Hụi góp</b> và nhập <b>Số lần góp</b><br>"
                   "(Lưu ý, Anh/Chị phải đặt mục <b>Khui hụi/lần</b> từ 2 ngày trở lên)<br>"
                   "<list>"
                   "<li>Phần mềm sẽ tính <b>tiền đóng chết</b> dựa vào <b>Tiền dây hụi</b> và <b>Số lân góp</b>.</li>"
                   "<li><b>Tiền đóng sống</b> sẽ được tính dựa trên <b>Thăm kêu</b>.</li>"
                   "<li>Nếu cho góp chân sống thì chọn vào ô <b>Hụi góp chân sống</b><br>.</li>"
                   "</list>"
                   "<b>Bước 4:</b> Nhập tên hui viên và điền vao số chân, sau đó bấm nút <b>Thêm</b> để thêm hụi viên.<br><br>"
                   "<b>Bước 5:</b> Bấm nút <b>LƯU THÔNG TIN</b>, sau đó bấm <b>OK</b> để hoàn thành việc tạo dây hụi góp.",
        "link": "https://www.youtube.com/shorts/rSyTlHMM_OA"
    },
    "mở dây hụi mãn trở lại đang hoạt động": {
        "name": "mở dây hụi mãn trở lại đang hoạt động",
        "details": "<b>Bước 1:</b> Anh/Chị hãy chọn vào mục <b>QUẢN LÝ HỤI</b>.<br><br>"
                   "<b>Bước 2:</b> Chọn vào chỗ <b>Đang hoạt động</b> sau đó chọn <b>Mãn</b>, rồi bấm nút <b>Tìm kiếm</b>.<br><br>"
                   "<b>Bước 3:</b>Hệ thống sẽ hiện th các dây hụi đang bị mãn, hãy bấm vào dây hụi Anh/Chị muốn mở hoạt động lại.<br><br>"
                   "<b>Bước 4:</b> Ở chỗ <b>Tình trạng dây hụi</b> hãy chọn <b>Đang hoạt động</b>, sau đó bấm <b>OK</b>.<br><br>"
                   "<b>Bước 5:</b> Kéo xuống và bấm nút <b>LƯU THÔNG TIN</b>.",
        "link": "https://www.youtube.com/shorts/HG76fJ1DmQI"
    },
    "mãn dây hụi": {
        "name": "mãn dây hụi",
        "details": "<b>Bước 1:</b> Anh/Chị hãy chọn vào mục <b>QUẢN LÝ HỤI</b>.<br><br>"
                   "<b>Bước 3:</b>Bấm vào dây hụi Anh/Chị muốn mãn.<br><br>"
                   "<b>Bước 4:</b> Ở chỗ <b>Tình trạng dây hụi</b> hãy chọn <b>Mãn</b>, sau đó bấm <b>OK</b>.<br><br>"
                   "<b>Bước 5:</b> Kéo xuống và bấm nút <b>LƯU THÔNG TIN</b>.<br>"
                   "Dây hụi bị mãn sẽ không được hiển thị, trừ các dây hụi đang hoạt động.",
        "link": "https://www.youtube.com/shorts/SF5m5mQxp1w"
    },
    "đóng lại hụi cũ để tính cân bằng hụi chính xác": {
        "name": "đóng lại hụi cũ để tính cân bằng hụi chính xác",
        "link": "https://www.youtube.com/watch?v=SSxNbCxp1EY"
    },
    "xóa kỳ hốt": {
        "name": "xóa kỳ hốt",
        "details": "<b>Bước 1:</b> Anh/Chị hãy chọn vào mục <b>QUẢN LÝ HỤI</b>.<br><br>"
                   "<b>Bước 2:</b> Chọn dây hụi có <b>Hụi viên cần xóa kỳ hôt</b>.<br><br>"
                   "<b>Bước 3:</b> Bấm vào nút <b>XEM CHI TIẾT</b>.<br><br>"
                   "<b>Bước 4:</b> Chọn kỳ hốt có <b>Hụi viên cần xóa kỳ hốt</b>.<br><br>"
                   "<b>Bước 5:</b> Bấm vào <b>Hụi viên cần xóa kỳ hốt</b>, sau đó bấm vào nút <b>XÓA DỮ LIỆU</b>.",
        "link": "https://www.youtube.com/shorts/8i7RiyGiW8c"
    },
    "xóa kỳ đóng bị lỗi": {
        "name": "xóa kỳ đóng bị lỗi",
        "details": "<b>Bước 1:</b> Anh/Chị hãy chọn vào mục <b>QUẢN LÝ HỤI</b>.<br><br>"
                   "<b>Bước 2:</b> Chọn dây hụi có <b>Hụi viên cần xóa kỳ hôt</b>.<br><br>"
                   "<b>Bước 3:</b> Bấm vào nút <b>XEM CHI TIẾT</b>.<br><br>"
                   "<b>Bước 4:</b> Chọn kỳ hốt có <b>Hụi viên cần xóa kỳ hốt</b>.<br><br>"
                   "<b>Bước 5:</b> Bấm vào <b>Hụi viên cần xóa kỳ hốt</b>, sau đó bấm vào nút <b>XÓA DỮ LIỆU</b>.",
        "link": "https://www.youtube.com/shorts/8i7RiyGiW8c"
    },
    "xác nhận đóng tất cả hụi": {
        "name": "xác nhận đóng tất cả hụi",
        "details": "<b>Bước 1:</b> Bấm vào mục <b>Hụi cần đóng trong ngày </b> <br><br>"
                   "<b>Bước 2:</b> Chọn <b>Xem dữ liệu</b>. Phần mềm sẽ tải các dữ liệu hụi viên cần đóng, Anh/Chị hãy chờ vài giây cho phần mềm xử lý xong nhé. <br><br>"
                   "<b>Bước 3:</b> Bấm vào nút <b>IN PHIẾU</b> để xem phiếu đóng hụi. <br><br>"
                   "<b>Bước 4:</b> Bấm vào nút <b>XÁC NHẬN VÀ IN PHIẾU</b>, phần mềm sẽ hiển thị phiếu đóng hụi tạm tính. Sau đó hãy bấm vào nút  <img src='img/1358023.png' width='16px'>  ở bên trái màng hình để chia sẽ phiếu cho khách. <br>"
                   "(Anh/Chị có thể chọn chia sẽ qua Zalo hoặc Messager cho khách hàng)<br><br>"
                   "<b>Bước 5:</b> Vuốt màng hình từ trái qua phải để quay về. <br>"
                   "(Hụi viên đã đóng hụi sẽ được <b>Gạch</b> và ghi <b>Đã đóng hụi</b>)",
        "link": "https://www.youtube.com/watch?v=SSxNbCxp1EY"
    },
    "cân bằng âm dương": {
        "name": "cân bằng âm dương",
        "details": "<b>Bước 1:</b> Chọn vào mục <b>Chức năng</b>.<br><br>"
                   "<b>Bước 2:</b> Bấm <b>Cân bằng hụi</b>.<br><br>"
                   "<b>Bước 3:</b> Chọn hụi viên cần xem, sau đó bấm <b>OK</b>.<br><br>"
                   "<b>Bước 4:</b> Bấm <b>IN BẢNG CÂN BẰNG (CHI TIẾT)</b>.<br>"
                   "(Bấm vào nút  <img src='img/1358023.png' width='16px'>  ở bên trái màng hình để chia sẽ phiếu cho khách, Anh/Chị có thể chọn chia sẽ qua Zalo hoặc Messager cho khách hàng)",
        "link": "https://www.youtube.com/shorts/acgQvk26wQI"
    }
}

# Hàm chung để cung cấp hướng dẫn và link video hướng dẫn


class ActionProvideGuide(Action):
    def name(self) -> Text:
        return "action_provide_guide"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        actions = tracker.get_slot("actions")

        if actions in ACTIONS_DATA:
            if actions == "tải phần mềm":
                # Hướng dẫn truy cập phần mềm
                message = f"{ACTIONS_DATA[actions]['name']} <br><hr> {ACTIONS_DATA[actions]['details']}"
                dispatcher.utter_message(text=message)
            elif actions == "sử dụng phần mềm":
                # Hướng dẫn sử dụng tổng quát
                video_link = ACTIONS_DATA[actions]["link"]
                message = f"{ACTIONS_DATA[actions]['details']} <br><br> <a href='{video_link}' target='_blank'>Kênh Youtube hướng dẫn</a>"
                dispatcher.utter_message(text=message)
            else:
                # Hướng dẫn chi tiết các chức năng khác
                video_link = ACTIONS_DATA[actions]["link"]
                message = (f"Để <b>{ACTIONS_DATA[actions]['name']}</b>, Anh/Chị hãy làm theo các bước hướng dẫn sau:<br><hr>"
                           f"{ACTIONS_DATA[actions]['details']}<br><hr>"
                           f"Hoặc Anh/Chị có thể xem video hướng dẫn sau để hiểu hơn <a href='{video_link}' target='_blank'>Xem Video</a>")
                dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(
                text="Xin lỗi, em chưa hiểu ý của Anh/Chị.")

        return []


class ActionAnswerDuration(Action):
    def name(self) -> Text:
        return "action_answer_duration"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = (f"Xin lỗi Anh/Chị, bên em không có gói gia hạn này.<br>"
                   f"Hiện tại bên em chỉ có các gói gia hạn:"
                   f"<list>"
                   f"<li>3 tháng</li>"
                   f"<li>1 năm</li>"
                   f"<li>Vĩnh viễn</li>"
                   f"</list><br>"
                   f"Nếu Anh/Chị có nhu cầu sử dụng tiếp thì Anh/Chị có thể lựa chọn các gói gia hạn trên.")
        dispatcher.utter_message(text=message)

        return []
