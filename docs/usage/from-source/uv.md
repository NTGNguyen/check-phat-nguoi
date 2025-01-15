# uv

## Yêu cầu

- [uv](https://github.com/astral-sh/uv)

---

## Thiết lập môi trường và dependencies

```sh
uv sync --no-dev
```

??? info

    uv sẽ tự động cài đặt phiên bản python phù hợp và cài đặt dependencies vào môi trường ảo

---

## Chạy chương trình

=== "uv run"

    ```sh
    uv run check-phat-nguoi # (1)
    ```

    1. Có thể thêm arg `--frozen` để không mutate lock file

=== "actived venv"

    Kích hoạt môi trường ảo

    === "Windows"

        ```powershell
        .venv\Scripts\activate
        ```

    === "Unix / MacOS"

        ```sh
        source .venv/bin/activate
        ```

    Chạy chương trình

    ```sh
    check-phat-nguoi
    ```
