# 画像から猫の種類を判別するAPIです
Intel Xeon E3-1231v3(Core i7-4770と同等性能)で、0.3秒で判別できます。<br>
モデルはオックスフォード大学が公開しているペットのデータセットを利用して訓練しました。<br>
https://www.robots.ox.ac.uk/~vgg/data/pets/<br>

必要なライブラリのインストールは下記コマンドでできます
```sh
make install
```

下記コマンドでimagesフォルダ内に配置した画像を仕分け（アノテーションを作成）して、学習を行います。<br>
```sh
make train
```
h5モデルが問題なく使用可能な状態になっていれば、下記コマンドでAPIの起動ができます。
```sh
make run
```

`test.py`でAPIの動作確認ができます。判別したい画像を`test_img`フォルダに配置して、引数にその画像の名前を指定して実行すれば結果が瞬時に帰ってきます。
テスト用の画像が1枚入っているので、下記コマンドで試してみてください。
```sh
python3 test.py 1.jpeg
```

参考記事
https://qiita.com/study_ryoma/items/a61ba10a3cd79acc5749