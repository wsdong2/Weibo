import sqlite3
import
import jieba.analyse

db = sqlite3.connect("weiBoData.db")
cour = db.cursor()
cour.execute("select * from DATA")
results = cour.fetchall()
jieba.analyse.set_stop_words("stopWords.txt")

peopleNum = 0
commentNum = 0
mCommentNum = 0
fCommentNum = 0
gender = [0, 0]
time = []
text = ""
commentInfo = {}

for i in range(0, 24):
    time.append(0)

for row in results:
    commentId = row[0]
    userId = row[1]
    userName = row[2]
    commentTime = row[3]
    userGender = row[4]
    commentText = row[5]

    commentNum += 1
    text += commentText
    if userId in commentInfo:
        commentInfo[userId][0] += 1
        commentInfo[userId][3] = commentInfo[userId][3] + "  " + commentText
    else:  # 没有就存入
        info = [1, userGender, userName, commentText]
        commentInfo.setdefault(userId, info)
        peopleNum += 1
        if userGender == "m":
            gender[0] += 1
        else:
            gender[1] += 1

    if userGender == "m":
        mCommentNum += 1
    else:
        fCommentNum += 1
    commentTime = int(commentTime.split(" ")[3].split(":")[0])
    time[commentTime] += 1

commentInfo = list(commentInfo.items())
commentInfo.sort(key=lambda info: int(info[1][0]), reverse=True)

words = jieba.lcut(text)
count = {}
for word in words:
    if len(word) == 1:
        continue
    else:
        count[word] = count.get(word, 0) + 1
stopeWords = []
with open('stopWords.txt', encoding="utf-8") as f:
    stopeWords = [word.strip() for word in f]
for word in stopeWords:
    if word in count:
        del (count[word])
counts = list(count.items())
counts.sort(key=lambda x: x[1], reverse=True)

print("------")
print("总评论人数有: " + peopleNum.__str__())
print("男性评论人数有：" + gender[0].__str__() + "    女性评论人数有：" + gender[1].__str__())
print("男性的评论有：" + mCommentNum.__str__() + "    女性的评论有：" + fCommentNum.__str__())
print("排名次数前二十的用户信息")
for i in range(0, 20):
    print("用户ID:" + commentInfo[i][0] + "  用户姓名：" + "%-20s" % commentInfo[i][1][2] + "用户性别：" + commentInfo[i][1][1]
          + "      评论次数：" + "%-3s" % commentInfo[i][1][0].__str__() + "   此用户评论内容的五个关键字：" + jieba.analyse.extract_tags(
        commentInfo[i][1][3], topK=5).__str__())
print("------")
print("总评论数有: " + commentNum.__str__(), "有效关键字共有:", len(counts))
print("评论的三十个关键字为：")
for i in range(30): 
    word, count = counts[i]
    print("{0:<3}:{1:>5}".format(word, count))