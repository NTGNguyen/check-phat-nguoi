![pre-commit status](https://img.shields.io/github/actions/workflow/status/NTGNguyen/check-phat-nguoi/pre-commit.yml?style=for-the-badge&label=pre%20commit&branch=main&logo=precommit)
[![wakatime](https://wakatime.com/badge/github/NTGNguyen/check-phat-nguoi.svg?style=for-the-badge)](https://wakatime.com/badge/github/NTGNguyen/check-phat-nguoi)

> [!WARNING]
>
> Work in progress!

> [!NOTE]
>
> Project được viết bằng python 3.13 nhưng có thể chạy với python 3.10 trở lên (không đảm bảo)

---

### TABLE OF CONTENTS

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

  - [USE](#use)
    - [From source](#from-source)
  - [DEV](#dev)
  - [DISCLAIMER](#disclaimer)
  - [APIs](#apis)
  - [REFS](#refs)
- [STAR HISTORY](#star-history)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

---

### USE

#### From source

1. Cài đặt requirements

```sh
python -m venv .venv
.venv/Scripts/activate # or "source .venv/bin/active" on Linux
pip install -e -r requirements.txt
```

2. Tạo `config.json`

- Dựa trên [`config.sample.json`](./config.sample.json)

3. Chạy chương trình

```sh
check-phat-nguoi # or "python -m check_phat_nguoi"
```

---

### DEV

> [!IMPORTANT]
> Require https://github.com/astral-sh/uv

```sh
uv sync # no need uv venv

.venv/Scripts/activate # or "source .venv/bin/active" on Linux

# uv can detect env with "uv run", not need active venv
uv run pre-commit install

uv run check-phat-nguoi
uv run generate-schemas
uv run generate-config-schema
```

- Test on production with python 3.10

```
uv python install 3.10
uv venv .venv-3.10 -p 3.10
uv pip install -e . -r ./requirements.txt
uv run check-phat-nguoi
```

---

### DISCLAIMER

> [!IMPORTANT]
>
> Repo được phát hành với mục đích học tập và tham khảo. Tác giả không chịu trách nhiệm đối với bất kỳ hành vi sử dụng nào có thể gây ảnh hưởng tiêu cực đến cá nhân, tổ chức khác hoặc vi phạm pháp luật Việt Nam.

1. Không đảm bảo

- Mã nguồn và tài nguyên trong repo này được cung cấp mà không có bất kỳ đảm bảo nào, dù rõ ràng hay ngụ ý.
- Không có sự đảm bảo rằng mã nguồn sẽ hoạt động chính xác, đáng tin cậy, hoặc phù hợp với bất kỳ mục đích cụ thể nào. Người sử dụng tự chịu toàn bộ rủi ro khi sử dụng các tài nguyên này.

2. Không phải sản phẩm chính thức

- Repo này không đại diện cho bất kỳ sản phẩm, dịch vụ chính thức nào của tổ chức, công ty, hoặc cá nhân nào khác ngoài tác giả.

3. Quyền sở hữu trí tuệ

- Trừ khi được chỉ định khác, toàn bộ nội dung trong repo này được cấp phép theo các điều khoản trong tệp [`LICENSE`](./LICENSE). Khi sử dụng mã nguồn hoặc tài nguyên, người dùng cần tuân thủ đầy đủ các quy định của giấy phép này.

---

### APIs

> [!NOTE]
>
> Read [docs](/docs)

---

### REFS

- List bien so: https://voz.vn/t/trang-check-phat-nguoi-tu-phat-trien.1048134/
- https://github.com/thaoanhhaa1/phat-nguoi-bot

---

## STAR HISTORY

<a href="https://star-history.com/#NTGNguyen/check-phat-nguoi&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=NTGNguyen/check-phat-nguoi&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=NTGNguyen/check-phat-nguoi&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=NTGNguyen/check-phat-nguoi&type=Date" />
 </picture>
</a>
