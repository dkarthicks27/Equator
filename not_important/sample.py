import numpy as np
import scipy
from scipy.sparse import vstack
import pickle
from sklearn.model_selection import train_test_split
from glob import glob
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer


def sample():
    text = [
        "Cricket is a bat-and-ball game played between two teams of eleven players on a field at the centre of which is a 20-metre (22-yard) pitch with a wicket at each end, each comprising two bails balanced on three stumps.",
        "The batting side scores runs by striking the ball bowled at the wicket with the bat, while the bowling and fielding side tries to prevent this and dismiss each player (so they are out). ",
        "it makes us really comfortable to play in the evening just to relax",
        "Tourism is the act of going for joy and roaming particularly in an unknown destination.",
        " However, tourism is not just confined to humans traveling to new locations, but the travel industry is one of the significant wellsprings of a national financial system.",
        "It has now developed into a major industry. "]
    # Here we have 6 doc's first 3 are about cricket and last 3 are about tourism
    # so accordingly we have labelled it
    label = [1, 1, 1, 2, 2, 2]
    # print(len(text))
    tfidf = TfidfVectorizer(stop_words="english", ngram_range=(2, 4))
    output = tfidf.fit_transform(text)
    # print(output)
    naiveBayes = MultinomialNB()
    naiveBayes.fit(output, label)
    test = ["cricket is my favourite sport",
            "The travel Industry makes employment increment and contributes towards enhancing the economy"]
    query = tfidf.transform(test)
    # let us predict the results
    print(naiveBayes.predict(query))


def otherLanguage():
    text = ["国际人权服务社祝您工作顺利！在即将到来的这一年和未来的岁月里，我们承诺，将继续竭尽全力，支持勇敢的人权捍卫者，他们每天都为建立更具包容性、公正、自由、可持续和尊重权利的社会而奋斗。"

            "我们很高兴推出2020年首期《人权季刊》，以帮助人权捍卫者和民间社会组织更好地了解联合国以及如何使用其人权机制并与之合作。我们希望您能像鼠家族一样聪慧和机敏，获得更多的信息保护人权！"

            "本刊编译英文版国际人权服务社《人权月刊》中与中国有关的内容，同时密切监测中国政府在联合国人权平台上的活动以及各国政府的反应，并向中国民间社会提示参与联合国人权机制的机会等。"]
    print(text[0])
    tfidf = TfidfVectorizer()
    output = tfidf.fit_transform(text)
    print(output)
    # it is printing the output in chinese


def nearDups():
    text = ["国际人权服务社祝您工作顺利！在即将到来的这一年和未来的岁月里，我们承诺，将继续竭尽全力，支持勇敢的人权捍卫者，他们每天都为建立更具包容性、公正、自由、可持续和尊重权利的社会而奋斗。"

            "我们很高兴推出2020年首期《人权季刊》，以帮助人权捍卫者和民间社会组织更好地了解联合国以及如何使用其人权机制并与之合作。我们希望您能像鼠家族一样聪慧和机敏，获得更多的信息保护人权！"

            "本刊编译英文版国际人权服务社《人权月刊》中与中国有关的内容，同时密切监测中国政府在联合国人权平台上的活动以及各国政府的反应，并向中国民间社会提示参与联合国人权机制的机会等。", "国际人权服务社祝您工作顺利！在即将到来的这一年和未来的岁月里，我们承诺，将继续竭尽全力，支持勇敢的人权捍卫者，他们每天都为建立更具包容性、公正、自由、可持续和尊重权利的社会而奋斗。"

            "我们很高兴推出2020年首期《人权季刊》，以帮助人权捍卫者和民间社会组织更好地了解联合国以及如何使用其人权机制并与之合作。我们希望您能像鼠家族一样聪慧和机敏，获得更多的信息保护人权！"

            "本刊编译英文版国际人权服务社《人权月刊》中与中国有关的内容，同时密切监测中国政府在联合国人权平台上的活动以及各国政府的反应，并向中国民间社会提示参与联合国人权机制的机会等。", "民间社会可以向条约机构提交自己的报告，就本国落实相关条约的情况提出他们的调查结论和看法。这样的报告有助于委员会成员对一国的人权状况获得更加全面的了解，因此至关重要。如果一个非政府组织没有时间或资源提交一份全面报告，应该考虑和其他国际组织合作，并考虑至少提交一份简要报告，强调指出有哪些关键议题委员会应该关注。非政府组织也可以推荐一些问题和建议，委员会在审议国家报告时可能会采用这些问题和建议。",
            "任何民间社会组织无论其地位都可以提供信息。来自国内非政府组织的报告在条约机构审查国家报告时具有特殊的价值，因为这些报告对当事国的人权状况提供了来源不同的信息。"]
    # here the first and the second string are the same out of the four string
    # so we can see that the result actually detects correctly the duplicate documents
    tfidf = TfidfVectorizer(ngram_range=(2, 4))
    output = tfidf.fit_transform(text)
    print(cosine_similarity(output))


nearDups()
