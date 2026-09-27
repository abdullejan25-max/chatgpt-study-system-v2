# Dependency License Audit

审计日期：2026-09-27
范围：当前 `pyproject.toml`、`uv.lock`、本机已安装发行物元数据，以及依赖项目/发行页面。本文记录工程审计结果，不替代法律意见。

## 项目许可证

本项目源码使用 Apache License 2.0。项目根目录 `LICENSE` 包含 Apache Software Foundation 发布的完整英文正文；`pyproject.toml` 声明 SPDX 标识 `Apache-2.0` 并将 `LICENSE` 列为发行包许可文件。这一声明仅适用于本项目自有作品，不会修改任何第三方依赖的许可条件。

构建后端最低版本要求为 Hatchling 1.27，以支持 PEP 639 的 SPDX `license` 与 `license-files` 元数据。

## 直接 Python 依赖

`pyproject.toml` 的默认依赖为 `mcp>=1,<2` 和 `pypdf>=6.18,<7`。当前 `uv.lock` 锁定为 MCP 1.30.0（MIT）与 pypdf 6.19.0（BSD-3-Clause）。MCP SDK 的锁定依赖闭包也包含 BSD-3-Clause、MIT、MIT-0、MPL-2.0、Apache-2.0、Apache-2.0 OR BSD-3-Clause 及 PSF 系许可证；本次检查没有在默认 Python 运行依赖中发现强 copyleft 依赖。

Windows / Python 3.12 的 31 个默认第三方运行包按发行元数据分组如下：

| 许可证 | 锁定包 |
| --- | --- |
| MIT | `annotated-types`, `anyio`, `attrs`, `h11`, `httpx-sse`, `jsonschema`, `jsonschema-specifications`, `mcp`, `pydantic`, `pydantic-core`, `pydantic-settings`, `PyJWT`, `referencing`, `rpds-py`, `typing-inspection` |
| BSD-3-Clause | `click`, `httpcore`, `httpx`, `idna`, `pycparser`, `pypdf`, `python-dotenv`, `sse-starlette`, `starlette`, `uvicorn` |
| 其他 | `certifi`（MPL-2.0）、`cffi`（MIT-0）、`cryptography`（Apache-2.0 OR BSD-3-Clause）、`python-multipart`（Apache-2.0）、`pywin32`（PSF）、`typing-extensions`（PSF-2.0） |

Windows 下的测试 extra 锁定 `pytest`、`iniconfig`、`packaging`、`pluggy`、`pygments` 与 `colorama`；它们的许可证元数据分别为 MIT、Apache-2.0 OR BSD-2-Clause、BSD-2-Clause，及 colorama 的 BSD classifier。构建后端最低版本为 `hatchling>=1.27,<2`，不属于运行依赖且当前未锁入 `uv.lock`；它支持 PEP 639 license metadata，正式构建时应留存解析版本与发行物 notices。

## 可选第三方组件

| 组件 | 仓库中的位置 | 审计结论与发布条件 |
| --- | --- | --- |
| PyMuPDF | `pdf-ocr` optional extra; PDF render/OCR path imports it lazily | Lockfile pins 1.28.2 only through the `pdf-ocr` extra. Default installation excludes it. Users explicitly selecting the extra receive PyMuPDF under its own GNU AGPL v3 or Artifex commercial licensing; the project Apache-2.0 license does not relicense PyMuPDF. |
| Tesseract | 外部本机软件；不在 Python 依赖或 `uv.lock` 中。本机未检测到可用安装 | 上游引擎采用 Apache-2.0；OCR 还依赖单独安装的语言数据。当前不随项目捆绑。若未来一起分发引擎或语言数据，需分别审计 notices 与数据许可。 |
| QMD | 用户独立安装的 Node.js CLI；不在 `pyproject.toml` / `uv.lock` 中 | 本机使用 `@tobilu/qmd` 2.8.3，包声明 MIT。当前项目不捆绑它。QMD 的 npm 运行依赖和平台二进制没有纳入本次 Python 依赖清单；若未来捆绑，应另做完整 npm 闭包审计。 |

## 发布 gate

- **已完成：**项目 LICENSE 正文、SPDX 元数据与发行包许可文件声明一致为 Apache-2.0。
- **已完成：**PyMuPDF 保持为非默认 `pdf-ocr` extra；独立 clean environment 的默认安装与 `dev` extra 均未安装该 distribution。`pdf-ocr` dry-run 仅计划增加 PyMuPDF 1.28.2。
- **已完成：**wheel 和 sdist 均成功构建；两种发行物都包含 Apache-2.0 SPDX metadata 与 LICENSE，PyMuPDF 依赖仅带 `extra == 'pdf-ocr'` marker。
- **用户使用条件：**如主动安装 `pdf-ocr`，需单独遵守 PyMuPDF 的授权条款；这不改变本项目的 Apache-2.0 声明。
- **后续维护：**为构建后端及发行时额外解析的构建依赖留存版本与许可信息。
- **外部边界：**Tesseract 与 QMD 是用户本机安装的外部工具，项目不自动安装或捆绑。

## 来源

- [Apache License 2.0 official text](https://www.apache.org/licenses/LICENSE-2.0.txt)
- [Python Packaging User Guide: license expression and PEP 639](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
- [PyMuPDF 1.28.2 on PyPI](https://pypi.org/project/PyMuPDF/1.28.2/) 与 [PyMuPDF installation / licensing docs](https://pymupdf.readthedocs.io/en/latest/installation.html)
- [MCP Python SDK license](https://github.com/modelcontextprotocol/python-sdk/blob/v1.x/LICENSE) 与 [MCP 1.30.0 PyPI metadata](https://pypi.org/pypi/mcp/1.30.0/json)
- [pypdf 6.19.0 PyPI metadata](https://pypi.org/pypi/pypdf/6.19.0/json) 与 [pypdf license](https://github.com/py-pdf/pypdf/blob/main/LICENSE)
- [QMD 2.8.3 package metadata](https://github.com/tobi/qmd/blob/main/package.json) 与 [QMD license](https://github.com/tobi/qmd/blob/main/LICENSE)
- [Tesseract license](https://github.com/tesseract-ocr/tesseract/blob/main/LICENSE) 与 [Tesseract installation guidance](https://github.com/tesseract-ocr/tessdoc/blob/main/Installation.md)
- [GNU license compatibility list](https://www.gnu.org/licenses/license-list.html.en)
