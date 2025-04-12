# MapGenerator
CHaserの対戦マップを自動で生成する機能の開発

## 使用技術
python 3.12.2  
poetry 2.1.1  

# 開発方法
一番最初に以下のコマンドを実行する.  
```bash
poetry install
```

コードを書いた場合, fmtとlintを適宜実行する.  
実行のためにMakefileが用意されている.  
実行例:  
```bash
make fmt
make lint

# fmtとlintの両方を実行する
make check
```

## 実行方法
各プログラムのドキュメントに記載しています.  
[RandomMapGenerator](docs/RandomMapGenerator.md)
