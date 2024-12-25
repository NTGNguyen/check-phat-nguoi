![pre-commit status](https://img.shields.io/github/actions/workflow/status/NTGNguyen/check-phat-nguoi/pre-commit.yml?style=for-the-badge&label=pre%20commit&branch=main&logo=precommit)
[![wakatime](https://wakatime.com/badge/github/NTGNguyen/check-phat-nguoi.svg?style=for-the-badge)](https://wakatime.com/badge/github/NTGNguyen/check-phat-nguoi)

---

### DEV

```sh
python -m venv .venv
.\.venv\Scripts\activate # For windows
pip install --editable .[dev]
pre-commit install

check-phat-nguoi # or "python -m check_phat_nguoi"

generate-config-schema # or "python -m generate_config_schema"
```

> [!NOTE]
>
> - \_\_main\_\_.py is for running as module (python -m)

### API

<details>
  <summary>
    Example
  </summary>

1. Example 1

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

2. Example 2

```sh
curl --data '{"bienso": "98A56604"}' -X POST -H "Content-Type: application/json" https://api.checkphatnguoi.vn/phatnguoi | jq .
```

```json
{
  "status": 1,
  "msg": "",
  "data": [
    {
      "Biển kiểm soát": "98A-566.04",
      "Màu biển": "Nền mầu trắng, chữ và số màu đen",
      "Loại phương tiện": "Ô tô",
      "Thời gian vi phạm": "11:09, 09/07/2023",
      "Địa điểm vi phạm": "Ngã 4 Xương Giang - Vương Văn Trà - Quang Trung, Phường Trần Phú, Thành phố Bắc Giang, Tỉnh Bắc Giang",
      "Hành vi vi phạm": "12321.5.5.a.01.Không chấp hành hiệu lệnh của đèn tín hiệu giao thông",
      "Trạng thái": "Chưa xử phạt",
      "Đơn vị phát hiện vi phạm": "Đội Cảnh sát giao thông, Trật tự - Công an thành phố Bắc Giang - Tỉnh Bắc Giang",
      "Nơi giải quyết vụ việc": [
        "1. Đội Cảnh sát giao thông, Trật tự - Công an thành phố Bắc Giang - Tỉnh Bắc Giang",
        "Địa chỉ: số 384 đường Xương Giang, phường Ngô Quyền",
        "Số điện thoại liên hệ: 0911595121"
      ]
    }
  ],
  "data_info": {
    "total": 1,
    "chuaxuphat": 1,
    "daxuphat": 0,
    "latest": "17:54 19/10/2024"
  }
}
```

3. Example 3

```sh
curl --data '{"bienso": "30F88251"}' -X POST -H "Content-Type: application/json" https://api.checkphatnguoi.vn/phatnguoi | jq .
```

```json
{
  "status": 1,
  "msg": "",
  "data": [
    {
      "Biển kiểm soát": "30F-882.51",
      "Màu biển": "Nền mầu trắng, chữ và số màu đen",
      "Loại phương tiện": "Ô tô",
      "Thời gian vi phạm": "10:21, 09/07/2023",
      "Địa điểm vi phạm": "Km 82+400, QL37, Xã Việt Tiến, Thị xã Việt Yên, Tỉnh Bắc Giang",
      "Hành vi vi phạm": "12321.5.6.a.01.Điều khiển xe chạy quá tốc độ quy định trên 20 km/h đến 35 km/h",
      "Trạng thái": "Chưa xử phạt",
      "Đơn vị phát hiện vi phạm": "Đội Cảnh sát giao thông, Trật tự - Công an thị xã Việt Yên - Tỉnh Bắc Giang",
      "Nơi giải quyết vụ việc": [
        "1. Đội Cảnh sát giao thông, Trật tự - Công an thị xã Việt Yên - Tỉnh Bắc Giang",
        "Địa chỉ: Thị xã Việt Yên",
        "2. Đội Cảnh sát giao thông, Trật tự - Công an quận Hai Bà Trưng - Thành phố Hà Nội"
      ]
    },
    {
      "Biển kiểm soát": "30F-882.51",
      "Màu biển": "Nền mầu trắng, chữ và số màu đen",
      "Loại phương tiện": "Ô tô",
      "Thời gian vi phạm": "11:32, 09/07/2023",
      "Địa điểm vi phạm": "Ngã 4 Xương Giang - Vương Văn Trà - Quang Trung, phường Trần Phú, thành phố Bắc Giang",
      "Hành vi vi phạm": "Điều khiển xe rẽ trái tại nơi có biển báo hiệu có nội dung cấm rẽ trái đối với loại phương tiện đang điều khiển",
      "Trạng thái": "Chưa xử phạt",
      "Đơn vị phát hiện vi phạm": "CA Thành phố Bắc Giang, Bắc Giang",
      "Nơi giải quyết vụ việc": [
        "1. CA Thành phố Bắc Giang, Bắc Giang",
        "Địa chỉ: Số 384 đường Xương Giang, phường Ngô Quyền, TP. Bắc Giang",
        "Số điện thoại liên hệ: 0911595121"
      ]
    },
    {
      "Biển kiểm soát": "30F-882.51",
      "Màu biển": "Nền mầu trắng, chữ và số màu đen",
      "Loại phương tiện": "Ô tô",
      "Thời gian vi phạm": "08:44, 21/12/2021",
      "Địa điểm vi phạm": "Km208+920",
      "Hành vi vi phạm": "Điều khiển xe chạy quá tốc độ quy định từ 10km/h đến 20 km/h",
      "Trạng thái": "Đã xử phạt",
      "Đơn vị phát hiện vi phạm": "Đội TTKSGTĐB số 1, Phòng 8 - Cục Cảnh sát giao thông",
      "Nơi giải quyết vụ việc": [
        "1. Đội TTKSGTĐB số 1, Phòng 8 - Cục Cảnh sát giao thông",
        "Địa chỉ: Đội TTKSGTĐB cao tốc số 1",
        "Số điện thoại liên hệ: 02435816399"
      ]
    },
    {
      "Biển kiểm soát": "30F-882.51",
      "Màu biển": "Nền mầu trắng, chữ và số màu đen",
      "Loại phương tiện": "Ô tô",
      "Thời gian vi phạm": "15:58, 23/04/2021",
      "Địa điểm vi phạm": "Nội Bài - Lào Cai",
      "Hành vi vi phạm": "Điều khiển xe chạy quá tốc độ quy định từ 10km/h đến 20 km/h",
      "Trạng thái": "Đã xử phạt",
      "Đơn vị phát hiện vi phạm": "Đội TTKSGTĐB số 1, Phòng 8 - Cục Cảnh sát giao thông",
      "Nơi giải quyết vụ việc": [
        "1. Đội TTKSGTĐB số 1, Phòng 8 - Cục Cảnh sát giao thông",
        "Địa chỉ: Đội TTKSGTĐB cao tốc số 1",
        "Số điện thoại liên hệ: 02435816399"
      ]
    }
  ],
  "data_info": {
    "total": 4,
    "chuaxuphat": 2,
    "daxuphat": 2,
    "latest": "19:53 01/06/2024"
  }
}
```

4. Example 4

```sh
curl --data '{"bienso": "59XB00000"}' -X POST -H "Content-Type: application/json" https://api.checkphatnguoi.vn/phatnguoi | jq .
```

```json
{
  "status": 2,
  "data": null
}
```

</details>

### REFS

- List bien so: https://voz.vn/t/trang-check-phat-nguoi-tu-phat-trien.1048134/
- https://github.com/thaoanhhaa1/phat-nguoi-bot
