# ML.SageMaker
Amazon SageMakerで利用するためのベースコンテナリポジトリになります。
機械学習でよく使うmecabを含んだイメージとなります。


## コンテナイメージのビルド方法
### ローカル版
ローカルで確認を行いたい場合は下記のコマンドを実行してください。
 ```
$ cd ML.SageMaker
$ ./build.sh {コンテナイメージ名}
```

### Amazon ECRにプッシュしたい場合
コンテナイメージをビルドしつつ、Amazon ECRにプッシュしたい場合は下記の手順で行なってください。  
ただし、awsコマンドとプッシュするリージョンへのログイン情報をあらかじめ設定しておく必要があります。
```
$ cd ML.SageMaker
$ ./build_and_push.sh {コンテナイメージ名}
```

## ローカルで実行する方法
### 学習
ローカルで学習を実行する場合は下記の手順を実行 

```
$ cd ML.SageMaker/local_test
$ ./train_local.sh {コンテナイメージ名}
```
学習は`decision_trees/train`で定義されます。

### 推論
ローカルで推論を行う場合は下記の手順でサーバーを実行後、`predict.sh`によって確認できます。
```
$ cd ML.SageMaker/local_test
$ ./serve_local.sh {コンテナイメージ名}
$ ./predict.sh payload_test.csv
```
デフォルトでは、特定のcsvを含んだリクエストを送ることによって推論を行います。

また、mecabによる確認を行う場合は、サーバーを起動した状態で下記で確認することができます。
```
curl -H 'Content-Type:application/json' -v http://localhost:8080/invocations -d '{"text":"【E・レシピ】料理のプロが作る簡単レシピ"}'
```

推論は`decision_trees/predictor.py`で定義されます。

これらの詳しい実装方法などはAWSの以下の記事などを参考にしてください。
https://aws.amazon.com/jp/blogs/news/train-and-host-scikit-learn-models-in-amazon-sagemaker-by-building-a-scikit-docker-container/#building