import MeCab

# 品詞のインデクス
INDEX_CATEGORY = 0


'''
MeCabで分かち書きするクラスの定義
辞書は"mecab-ipadic-neologd"を使用
'''
class Tokenizer:
    def __init__(self, dictionary="mecabrc"):
        self.dictionary = dictionary
        self.tagger = MeCab.Tagger(self.dictionary)

    def extract_words(self, text):
        if not text or type(text) is not str:
            return None

        words = []
        # 文字列がGCされるのを防ぐ
        self.tagger.parse('')
        node = self.tagger.parseToNode(text)
        while node:
            feature = node.feature.split(',')
            # "，"で文字列の分割を行い, ターゲットになる品詞と比較を行う.
            if feature[INDEX_CATEGORY] == '名詞':
                words.append(node.surface)
            node = node.next

        return words


if __name__ == '__main__':
    test_text = '煮るのは5分！大根おでんに味を染み込ませる3つのコツ【野菜のきほん #3】 - 【E・レシピ】料理のプロが作る簡単レシピ[2/4ページ] 7月29日'
    tokenize_word = Tokenizer()
    print(tokenize_word.extract_words(test_text))
