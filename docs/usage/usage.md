# Hướng dẫn sử dụng

## Cài đặt python

- <https://www.python.org/downloads/>

??? note

    Project được viết bằng python 3.13 nhưng có thể chạy với python 3.10 trở lên (không đảm bảo)

---

## Clone repo

```sh
git clone https://github.com/NTGNguyen/check-phat-nguoi.git
```

---

## Cài đặt dependencies

### Thiết lập môi trường ảo

#### Tạo môi trường ảo

```sh
python -m venv .venv
```

#### Kích hoạt môi trường ảo

=== "Windows"

    ```powershell
    .venv/Scripts/activate
    ```

=== "Linux / MacOS"

    ```sh
    source .venv/bin/active
    ```

#### Cài đặt dependencies

```sh
pip install -e -r requirements.txt
```

???+note

    Để tắt môi trường khi không sử dụng chạy `deactivate`

---

## Sử dụng chương trình

### Thiết lập file config

Thiết lập file `config.json` (1)
{ .annotate }

1.  Hoặc
    - `check-phat-nguoi.config.json` tại nơi đang đứng
    - `~/check-phat-nguoi.config.json`

??? example

    ```json title="config.json"
    {% include "../../config.sample.json" %}
    ```

### Chạy chương trình

???+ note

    Yêu cầu kích hoạt venv

=== "Trực tiếp"

    ```sh
    check-phat-nguoi
    ```

=== "Python module"

    ```sh
    python -m check-phat-nguoi
    ```
