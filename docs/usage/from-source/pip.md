# Pip

## Yêu cầu

- [Python](https://www.python.org/downloads/) (>=3.13)

---

## Thiết lập môi trường ảo

### Tạo môi trường ảo

```sh
python -m venv .venv
```

### Kích hoạt môi trường ảo

=== "Windows"

    ```powershell
    .venv\Scripts\activate
    ```

=== "Unix / MacOS"

    ```sh
    source .venv/bin/activate
    ```

---

## Cài đặt dependencies

```sh
pip install -r requirements/requirements.txt
```

???- info "Tắt môi trường ảo"

    Để tắt môi trường khi không sử dụng chạy `deactivate`

---

## Chạy chương trình

!!! important ""

    Yêu cầu kích hoạt venv

=== "Trực tiếp"

    ```sh
    check-phat-nguoi
    ```

=== "Python module"

    ```sh
    python -m check-phat-nguoi
    ```
