# Hướng dẫn sử dụng

## Yêu cầu

- [Python](https://www.python.org/downloads/)
- [Tesseact OCR CLI](https://tesseract-ocr.github.io/tessdoc/Installation.html) và [Tesseact data set](https://github.com/tesseract-ocr/tessdata) (Không bắt buộc)(1)
  { .annotate }

      1. Sử dụng để giải captcha đối với API csgt.vn

??? note

    Project được viết bằng python 3.13 nhưng có thể chạy với python 3.10 trở lên (không đảm bảo). Đối với discord notification yêu cầu phiên bản >= 3.13.

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
    .venv\Scripts\activate
    ```

=== "Unix / MacOS"

    ```sh
    source .venv/bin/activate
    ```

#### Cài đặt dependencies

```sh
pip install -r requirements/requirements.txt
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

???+ note

    Xem [`Config Schema`](https://ntgnguyen.github.io/check-phat-nguoi/schemas/config.html) để biết chi tiết config

???+ warning

    Hiện tại API từ csgt.vn không đảm bảo hoạt động.

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
