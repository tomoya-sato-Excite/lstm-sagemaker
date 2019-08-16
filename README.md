# lstm-sageMaker
Amazon SageMakerで利用するためのベースコンテナリポジトリになります。
機械学習でよく使うmecabを含んだイメージとなります。


## コンテナイメージのビルド方法
### ローカル版
ローカルで確認を行いたい場合は下記のコマンドを実行してください。
 ```
$ cd lstm-sagemaker
$ ./build.sh {コンテナイメージ名}
```

### Amazon ECRにプッシュしたい場合
コンテナイメージをビルドしつつ、Amazon ECRにプッシュしたい場合は下記の手順で行なってください。  
ただし、awsコマンドとプッシュするリージョンへのログイン情報をあらかじめ設定しておく必要があります。
```
$ cd lstm-sagemaker
$ ./build_and_push.sh {コンテナイメージ名}
```

## ローカルで実行する方法
### 学習
ローカルで学習を実行する場合は下記の手順を実行 

```
$ cd lstm-sagemaker/local_test
$ ./train_local.sh {コンテナイメージ名}
```
学習は`lstm/train`で定義されます。

### 推論
ローカルで推論を行う場合は下記の手順でサーバーを実行後、`predict.sh`によって確認できます。
```
$ cd lstm-sagemaker/local_test
$ ./serve_local.sh {コンテナイメージ名}
$ ./predict.sh {seed title}
```
デフォルトでは、特定の文字列を送ることによって推論を行います。

推論は`lstm/predictor.py`で定義されます。

これらの詳しい実装方法などはAWSの以下の記事などを参考にしてください。
https://aws.amazon.com/jp/blogs/news/train-and-host-scikit-learn-models-in-amazon-sagemaker-by-building-a-scikit-docker-container/#building