### DEV

```sh
python -m venv .venv
pip install -r requirements.txt
```

### API

```sh
curl --data '{"bienso": "60A64685"}' -X POST -H "Content-Type: application/json" https://api.checkphatnguoi.vn/phatnguoi | jq .
```

```json
{
  "status": 1,
  "msg": "",
  "data": [
    {
      "Biển kiểm soát": "60A64685",
      "Màu biển": "Nền mầu trắng, chữ và số màu đen",
      "Loại phương tiện": "Ô tô",
      "Thời gian vi phạm": "13:57, 07/10/2023",
      "Địa điểm vi phạm": "Km1716+005, Quốc lộ 1A - Bình Thuận",
      "Hành vi vi phạm": "12321.5.3.a.01.Điều khiển xe chạy quá tốc độ quy định từ 05 km/h đến dưới 10 km/h",
      "Trạng thái": "Chưa xử phạt",
      "Đơn vị phát hiện vi phạm": "ĐỘI TT, ĐTGQTNGT VÀ XLVP - PHÒNG CSGT BÌNH THUẬN",
      "Nơi giải quyết vụ việc": [
        "1. ĐỘI TT, ĐTGQTNGT VÀ XLVP - PHÒNG CSGT BÌNH THUẬN",
        "Địa chỉ: 115 Tôn Đức Thắng, TP. Phan Thiết",
        "Số điện thoại liên hệ: 0693.428184",
        "2. Đội Cảnh sát giao thông, Trật tự - Công an huyện Trảng Bom - Tỉnh Đồng Nai",
        "Địa chỉ: Huyện Trảng Bom"
      ]
    }
  ],
  "data_info": {
    "total": 1,
    "chuaxuphat": 1,
    "daxuphat": 0,
    "latest": "12:41 22/12/2024"
  }
}
```
