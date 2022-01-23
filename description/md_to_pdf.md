# KosenNote : markdown-pdf の導入

# node の導入

```bash
# nodejs, npm をインストール
sudo apt install -y nodejs npm

# n package をインストール
sudo npm install n -g

# node をインストール
sudo n stable

# 後処理
sudo apt purge -y nodejs npm
```

# [markdown-pdf](https://github.com/alanshaw/markdown-pdf) の導入

```bash
# -g オプションを付けて markdown-pdf をインストール
npm install -g markdown-pdf --ignore-scripts

# バージョンの確認
markdown-pdf --version
```

# 実行
```bash
markdown-pdf -o md_to_pdf.pdf md_to_pdf.md
```
