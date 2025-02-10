# ポケポケ「幻のいる島」環境における最適戦略は何だったか、解析してみた
## セットアップ
Python のパッケージマネージャとして uv を使用しています。
```
brew install uv
```
以下のコマンドにより仮想環境のセットアップが行えます。
```
uv sync
```
## 実行
record.json を配置した状態で、以下のコマンドにより解析コードを実行できます。
```
uv run find_equilibrium.py
```
結果は equilibrium.json に出力されます。