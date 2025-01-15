# uv

## Yêu cầu

- [uv](https://github.com/astral-sh/uv)

## Thiết lập môi trường và dependencies

```sh
uv sync --no-dev
```

## Chạy chương trình

```sh
uv run check-phat-nguoi # (1)
```

1. Có thể thêm arg `--frozen` để không mutate lock file
