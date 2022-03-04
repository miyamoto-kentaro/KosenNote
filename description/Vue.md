# KosenNote : Vue のセットアップ

# Vue プロジェクトの作成

```bash
# ubuntuの更新
sudo apt update
sudo apt -y upgrade

# nodeコンテナをbuild
docker build -f frontend/Dockerfile.setup -t kosennote-frontend frontend/

# nodeコンテナをfrontにボリュームして起動
docker run -it -v $PWD/frontend/:/usr/src/app kosennote-frontend bash
```

コンテナの中で Vue を立ち上げる

```bash
# Vueのインストール
npm install -g @vue/cli
# カレントディレクトリに作成
vue create .
```

VueCli のマニュアルに従って、以下の項目を選択する

---

> - Use https://registry.npm.taobao.org for faster installation?
>   -> no
>
> - Please pick a preset:
>
>   - Default ([Vue 2] babel, eslint)
>   - Default (Vue 3) ([Vue 3] babel, eslint)
>   - Manually select features <- select
>
> - Please pick a preset: Manually select features.Check the features needed for your project:
>
>   - **Choose Vue version** <-
>   - **Babel** <-
>   - **TypeScript** <- 任意
>   - Progressive Web App (PWA) Support
>   - **Router** <-
>   - **Vuex** <-
>   - **CSS Pre-processors** <-
>   - Linter / Formatter
>   - Unit Testing
>   - E2E Testing
>
> - version:
>
>   - **3.x** <-
>   - 2.x
>
> - Use class-style component syntax?
>
>   - **No**
>
> - Use Babel alongside TypeScript (required for modern mode, auto-detected polyfills, transpiling JSX):
>
>   - **Yes**
>
> - history mode:
>
>   - **Yes**
>
> - Css preprocessor
>
>   - **Sass/SCSS (with dart-sass)** <-
>   - Sass/SCSS (with node-sass)
>   - Less
>   - Stylus
>
> - Where do you prefer placing config ...
>   - **In dedicated config files** <-
>   - In package.json
> - Save this as a preset for future projects?
>
>   - **No**
>
> - Pick the package manager to use when installing dependencies:
>   - Use Yarn
>   - **Use NPM** <-

---

よく使うライブラリーをインストールしておく

```
npm install axios
npm install bulma
npm install bulma-toast
```

frontend に権限を付与する
これをしないと、config を編集できない

```
sudo chown -R {username}:{username} frontend/
```

## docker-compose をつかって、Django のテスト

docker-compose.local.yml を起動して、コンテナが local で動くかをテストします。

```
docker-compose -f docker-compose.local.yml up -d --build
docker-compose -f docker-compose.local.yml down -v
```

Gitでファイルを持ってきてfrontend/node_modulesが存在しないときは

```
# nodeコンテナをbuild
docker build -f frontend/Dockerfile.setup -t kosennote-frontend frontend/

# nodeコンテナをfrontにボリュームして起動
docker run -it -v $PWD/frontend/:/usr/src/app kosennote-frontend bash
```

コンテナを立ち上げて

```
npm install
```

npmインストールをすると、エラーがなくなる。
