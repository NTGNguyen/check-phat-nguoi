# Cài đặt python

- https://www.python.org/downloads/

> [!NOTE]
>
> Project được viết bằng python 3.13 nhưng có thể chạy với python 3.10 trở lên (không đảm bảo)

---

# Clone repo

```sh
git clone https://github.com/NTGNguyen/check-phat-nguoi.git
```

---

# Cài đặt dependencies

## Thiết lập môi trường ảo

1. Tạo môi trường ảo

```sh
python -m venv .venv
```

2. Kích hoạt môi trường ảo

```sh
# Windows
.venv/Scripts/activate

# Linux
source .venv/bin/active
```

3. Cài đặt dependencies

```sh
pip install -e -r requirements.txt
```

> [!NOTE]
>
> Tắt môi trường ảo chạy `deactivate`

---

# Sử dụng chương trình

## Thiết lập file config

> [!IMPORTANT]
>
> Thiết lập file `config.json` hoặc `check-phat-nguoi.config.json` tại nơi đang đứng hoặc tại `~/check-phat-nguoi.config.json`

```json
{% include "../config.sample.json" %}
```

## Chạy trương chình

```sh
check-phat-nguoi

# Hoặc
python -m check_phat_nguoi
```
