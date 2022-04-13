# KosenNote : Django のセットアップ

# Django プロジェクトの作成

```bash
# ubuntuの更新
sudo apt update
sudo apt -y upgrade

# pythonのversion確認と最新のpythonをインストール
python3 -V

# pythonコンテナをbuild
docker build -f backend/Dockerfile.setup -t kosennote-backend backend/

# pythonコンテナをbackendにボリュームして起動
docker run -it -v $PWD/backend/:/usr/src/app kosennote-backend bash
```

コンテナの中で Django を立ち上げる

```bash
# djangoのインストール
pip install django

# Djangoプロジェクトの作成
django-admin startproject config .

# アプリを作成
python manage.py startapp {appname}


# コンテナから退出
exit
```

backend に権限を付与する
これをしないと、config を編集できない

```
sudo chown -R {username}:{username} backend/
```

## docker-compose をつかって、Django のテスト

docker-compose.local.yml を起動して、コンテナが local で動くかをテストします。

```
docker-compose -f docker-compose.local.yml up -d --build
docker-compose -f docker-compose.local.yml down -v
```
