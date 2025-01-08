# Hướng dẫn sử dụng

## Cài đặt python

- <https://www.python.org/downloads/>

<!-- prettier-ignore-start -->
???+note
    Project được viết bằng python 3.13 nhưng có thể chạy với python 3.10 trở lên (không đảm bảo)
<!-- prettier-ignore-end -->

---

## Clone repo

```sh
git clone https://github.com/NTGNguyen/check-phat-nguoi.git
```

---

## Cài đặt dependencies

### Thiết lập môi trường ảo

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

<!-- prettier-ignore-start -->
???+note
    Tắt môi trường ảo chạy `deactivate`
<!-- prettier-ignore-end -->

---

## Sử dụng chương trình

### Thiết lập file config

<!-- prettier-ignore-start -->

???+important annotate
    Thiết lập file `config.json` (1)

1.  Hoặc `check-phat-nguoi.config.json` tại nơi đang đứng (1)
    { .annotate }

    1.  Hoặc tại `~/check-phat-nguoi.config.json`

<!-- prettier-ignore-end -->

```json
{% include "../config.sample.json" %}
```

### Chạy chương trình

```sh
check-phat-nguoi # (1)
```

<!-- prettier-ignore-start -->

1.   Hoặc python -m check-phat-nguoi

<!-- prettier-ignore-end -->
