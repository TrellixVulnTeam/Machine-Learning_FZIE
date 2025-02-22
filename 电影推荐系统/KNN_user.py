# 针对用户相似度的推荐算法
# 这里我将一个用户对于全部流派的评分作为该用户的特征向量，使用KNN算法，对于输入的用户ID
# 首先选出10个与当前用户最相似的10个用户
# 之后选出这10个最相似用户看过的且当前用户没有看过的电影
# 最后在这些电影中选择出 平均评分最高的十部，推荐给用户

from featureAnalysis import *
import numpy as np
import matplotlib.pyplot as plt

def distance(user1,user2):
    # input: rating list
    return np.sqrt(sum(pow(user1[i]-user2[i],2)  for i in range(len(user1))))


# 用户之间的距离矩阵
def dis_matrix(user_gen):
    # input {userID:[3,4,2,0,3,...]}
    res=[]
    for id1 in user_gen:
        temp=[]
        for id2 in user_gen:
            if id1==id2:
                temp.append(float('inf'))
            else:
                temp.append(distance(user_gen[id1],user_gen[id2]))
        res.append(temp)
    return res


# 找到输入用户最接近的K位用户
def closeUser(user_id,dis_mat,K):
    row=int(user_id)-1
    dis=dis_mat[row]
    res=[]
    for i in range(K):
        min_idx=dis.index(min(dis))
        res.append(str(min_idx+1))
        dis[min_idx]=float('inf')
    return res

# 找到类似客户看过该用户未看过的电影列表
# 找到所有可能推荐的电影列表，包含该用户已经评分的，用于测评
def closeMovie(user_id,close_user,user):
    # input [id1,id2,....]
    # input {用户id:[[电影id],[评分]]}
    rate_table={}
    for id in close_user:
        for i in range(len(user[id][1])):
            score=user[id][1][i]
            movie=user[id][0][i]
            if not score in rate_table:
                rate_table[score]=[movie]
            else:
                rate_table[score].append(movie)
    rate_list=sorted(rate_table)
    # 排除用户已经看过的电影的所有电影ID list
    res,all_rec=[],[]
    while rate_list:
        rate=rate_list.pop()
        for mov_id in rate_table[rate]:
            all_rec.append(mov_id)
            if not mov_id in user[user_id][0]:
                res.append(mov_id)
    return res,all_rec

# 用户侧写
def userProfile(user_gen,user_id,gen_mov):
    # input {userID:[3,4,2,0,3,...]}
    # 流派名称list
    gen=[i for i in gen_mov]
    rate=user_gen[user_id]
    # 各流派平均得分条形图
    params = {'figure.figsize': '25, 4'}
    plt.rcParams.update(params)
    plt.bar(range(len(rate)), rate,tick_label=gen,width=0.5)
    plt.xlabel('Genre')
    plt.ylabel('Rating')
    plt.show()

# 打印推荐电影及其流派和预测评分
def printMovie(movie_name,mov_gen,rates):
    for i in range(len(movie_name)):
        print('{}{:.2f}   {}{}{}'.format('predict rate:', rates[i],movie_name[i],':',mov_gen[movie_name[i]]))




def allRecoMovies(user_id):
    name, mov_gen, gen_mov = loadGenre('movies.csv')
    rating, user = loadRating('ratings.csv', name)
    gen_rating = rateGenre(gen_mov, rating)
    user_gen = user_genre(user, mov_gen, gen_mov, name)
    # 该用户侧写
    userProfile(user_gen,user_id,gen_mov)
    dis_mat=dis_matrix(user_gen)
    close_user=closeUser(user_id,dis_mat,10)
    #  得到推荐电影
    res,all_rec=closeMovie(user_id,close_user,user)
    return res,all_rec

