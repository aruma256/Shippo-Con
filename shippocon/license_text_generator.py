import base64

B64_LICENSE_TEXT = r"""
PLACEHOLDER
"""


def get_license_text() -> str:
    if B64_LICENSE_TEXT.strip() == "PLACEHOLDER":
        return "".join(f"サンプルライセンステキスト{i}\n" for i in range(100))
    return base64.b64decode(B64_LICENSE_TEXT.encode()).decode("utf-8")
