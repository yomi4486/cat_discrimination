画像から猫の種類を判別するAPIです
Intel Xeon E3-1231v3(Core i7-4770と同等性能)で、0.3秒で判別できます。
モデルはオックスフォード大学が公開しているペットのデータセットを利用して訓練しました。
https://www.robots.ox.ac.uk/~vgg/data/pets/

必要なライブラリのインストールは下記コマンドでできます
pip install -r requirements.txt

model.pyでimagesフォルダ内に配置した画像を仕分け（アノテーションを作成）して、学習を行います。

GitHubの制約上pushはしませんが、モデルの容量は120MB程度で軽量です。
h5モデルが問題なく使用可能な状態になっていれば、run.batでAPIの起動ができます。

test.pyでAPIの動作確認ができます。判別したい画像をtest_imgフォルダに配置して、引数にその画像の名前を入れて実行すれば結果が瞬時に帰ってきます。
テスト用の画像が1枚入っているので、下記コマンドで試してみてください。
python test.py 1.jpeg

参考記事
https://qiita.com/study_ryoma/items/a61ba10a3cd79acc5749