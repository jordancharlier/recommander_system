from flask import Flask,render_template,jsonify,json,request,url_for,redirect
from fabric.api import *
from pyspark import *
from pyspark.sql import *
from pyspark.conf import *
from pyspark.sql.functions import *
from uszipcode import ZipcodeSearchEngine
import numpy as np
import json



application = Flask(__name__)





@application.route('/')
def showMachineList():
    return render_template('index.html',connected = False,generalData = False)

@application.route('/<name>')
def generalData(name):
    return render_template('index.html',connected = True,generalData = True)


@application.route('/getRecJSON/<id>',methods=['POST'])
def getRecJSON(id):
    print("aaaaaaaaaaaaaaaaaaaa")
    return createJsonMoviePreference(id)

@application.route('/getSexeJSON',methods=['POST'])
def getSexeJSON():
    return setSexeJson

@application.route('/getMostViewGenreJSON',methods=['POST'])
def getMostViewGenre():
    return setGenreMostViewJson

@application.route('/getMoviesPerGenreJSON',methods=['POST'])
def getMoviesPerGenre():
    return setNbMovieForGenresJson

@application.route('/getAgeJSON',methods=['POST'])
def getAgeJSON():
    try:
        liste = json.loads(setAgeJson)
    except TypeError:
        print("catching TypeError")
    res = []
    try:
        for data in liste:
            x = []
            x.append(data["Age"])
            x.append(data["nb"])
            res.append(x)
    except TypeError:
        print("catching TypeError")
    
    return json.dumps(res)

@application.route('/getOccupJSON',methods=['POST'])
def getOccupJSON():
    return setOccupJson

@application.route('/getZipJSON',methods=['POST'])
def getZipJSON():
    return setZipJson
    


@application.route('/login',methods = ['POST'])
def login():
    if request.method == 'POST':
        u = lenUsers()
        userID = int(request.form['inputSpace'])
        if userID <= u:
            return redirect(url_for('generalData',name = userID))
        else:
            return redirect(url_for('showMachineList'))
        



def lenUsers():
    return dfusers.count()

def weightsUser(id):

    listGenre = []
    dic = {'Action':0,'Adventure':0,'Animation':0,'Children\'s':0,'Comedy':0,'Crime':0,'Documentary':0,'Drama':0
          ,'Fantasy':0,'Film-Noir':0,'Horror':0,'Musical':0,'Mystery':0,'Romance':0,'Sci-Fi':0,'Thriller':0
           ,'War':0,'Western':0}
    
    dicRating = {'Action':0,'Adventure':0,'Animation':0,'Children\'s':0,'Comedy':0,'Crime':0,'Documentary':0,'Drama':0
          ,'Fantasy':0,'Film-Noir':0,'Horror':0,'Musical':0,'Mystery':0,'Romance':0,'Sci-Fi':0,'Thriller':0
           ,'War':0,'Western':0}

    count = 0
    utilisateur = dfJoin.where((dfJoin.UID == id))
    filmeRegarder = utilisateur.select(utilisateur.Genres,utilisateur.Rating).collect()
    for i in filmeRegarder:
        l=[i[0].split('|')]
        for genre in l:
            for g in genre:
                dic[g] += 1
                count += 1
                dicRating[g] += int(i[1])       
    for key in dicRating:
        if dic[key] != 0:
            dicRating[key] /= count
    #s = [(k, dic[k]) for k in sorted(dic, key=dic.get, reverse=True)]
    return dicRating   

def writeDataUserInCsvFile(data,id,HeadCsv):
    file = open("usersV2.csv","a") 
    if HeadCsv:
        file.write("id,genre,view\n")
    for genre in data:
        file.write(str(id)+","+genre+","+str(data[genre])+"\n")
    
    file.close()

def createCsvFileWithDataUsers():
    sizeOfUsers = dfusers.count()
    infoCsv = True
    for user in range(1,sizeOfUsers+1):
        s = weightsUser(id = user)
        if user == 2:
            infoCsv = False
        writeDataUserInCsvFile(data = s,id = user,HeadCsv = infoCsv)


def weightsMovie(movieId):
    movie = dfJoin.where(dfJoin.MID == movieId).select(dfJoin.UID).collect()
   # dfJoin.where(dfJoin.MID == movieId).show()
    #print(len(movie))
    dic = {'Action':0,'Adventure':0,'Animation':0,'Children\'s':0,'Comedy':0,'Crime':0,'Documentary':0,'Drama':0
           ,'Fantasy':0,'Film-Noir':0,'Horror':0,'Musical':0,'Mystery':0,'Romance':0,'Sci-Fi':0,'Thriller':0
           ,'War':0,'Western':0}
    if len(movie) > 0:
        for idUser in movie:
            userDataGenre = dfUsersData.where(dfUsersData.id == idUser[0]).collect()
            for userGenre in userDataGenre:
                dic[userGenre[1]] += float(userGenre[2])
        for key in dic:
            dic[key] /= len(movie)
    return dic


def writeMovieDataInCsvFile(data,id,HeadCsv):
    file = open("movieV2.csv","a") 
    if HeadCsv:
        file.write("id,genre,view\n")
    for genre in data:
        file.write(str(id)+","+genre+","+str(data[genre])+"\n")
    
    file.close()

def createCsvFileWithMovieData():
    sizeOfUsers =dfmovies.count()
    infoCsv = False
    for movie in range(1077,sizeOfUsers+1):
        s = weightsMovie(movieId = movie)
        if movie == 2:
            infoCsv = False
        writeMovieDataInCsvFile(data = s,id = movie,HeadCsv = infoCsv)




def distanceE(vec , vec2):
    return np.linalg.norm(np.array(vec)-np.array(vec2))
    
def createVectorOfWeightsData(data):
    lists = []
    for info in data:
        lists.append(info[2])
    return lists

def createListMovieView(listOfMoviesView):
    liste = []
    for idM in listOfMoviesView:
        liste.append(int(idM[0]))
    return liste
    
def algoRecommendation(idUsers):    
    dataDebug = dfUsersData.where(dfUsersData.id == idUsers).collect()
    listUserDefault = createVectorOfWeightsData(dataDebug)
    listDistance = {}
    listOfMoviesView = dfJoin.where(dfJoin.UID == idUsers).select(dfJoin.MID).collect()
    listOfMV = createListMovieView(listOfMoviesView = listOfMoviesView)
    for movieId in range(1,dfmovies.count()):
        print(movieId)
        if movieId not in listOfMV:
            movieWeights = dfMovieData.where(dfMovieData.id == movieId).collect()
            listMovieWeights = createVectorOfWeightsData(movieWeights)
            if len(listMovieWeights) == len(listUserDefault):
                listDistance[movieId] = distanceE(vec = listUserDefault , vec2 = listMovieWeights)        
    return listDistance



def createJsonMoviePreference(id):
    dicMovies = algoRecommendation(id)
    jsonM = []
    for ids in sorted(dicMovies, key=dicMovies.get, reverse=False):
        movies = dfmovies.where(dfmovies.MID == ids).collect()
        dic = {}
        print('r')
        for m in movies:
            dic ["Title"] = str(m[1])
            dic ["Genres"] = m[2]
            dic ["Year"] = m[3]
        dic["Compatibility"] = dicMovies[ids]
        jsonM.append(dic)
    return json.dumps(jsonM)


def getSexeUsersJson():
    countMen = dfusers.where(dfusers.Gender == "M").count()
    countWomen = dfusers.where(dfusers.Gender == "F").count()   
    data = {}
    data['F'] = countWomen
    data['M'] = countMen
    return json.dumps(data)

def getAgeUsersJson():
    data = {}
    JsonArray = []
    for a in range(1,100):
        age = dfusers.where(dfusers.Age == a).collect()
        if len(age) > 0:
            data[a] = len(age)

    for d in data:
        JsonObjet = {}
        JsonObjet['Age'] = d
        JsonObjet['nb'] = data[d]
        JsonArray.append(JsonObjet)
    return json.dumps(JsonArray)

def getOccupationUsersJson():
    dicO ={0:" not specified",1:"academic/educator",2:"artist",3:"clerical/admin",4:"college/grad student",5:"custom service",6:"doctor/health core",7:"executive/managerial",8:"farmer",9:"homemaker",10:"K-12 student",11:"lawyer",12:"programmer",13:"retired",14:" sales/marketing",15:"scientist",16:"self-employed",17:"technicien/engineer",18:"tradesman/craftman",19:"unemployed",20:"writer"}
    data = {}
    JsonArray = []
    for oc in range(0,20):
        ocu = dfusers.where(dfusers.Occupation == oc).collect()
        data[oc] = len(ocu)
    for d in data:
        JsonObjet = {}
        JsonObjet['name'] = dicO[d]
        JsonObjet['drilldown'] = dicO[d]
        JsonObjet['y'] = data[d]
        JsonArray.append(JsonObjet)
    return json.dumps(JsonArray)

def getZipCodeUsersJson():
    data = []
    listZCode = []
    jsonArray = []
    zcode = dfusers.groupBy("Zip-code").count().collect()
    search = ZipcodeSearchEngine()
    for code in zcode:
        jsonObjet = {}
        jsonObjet['zip'] = code[0]
        zipcode = search.by_zipcode(code[0])
        listZCode.append(zipcode["City"])
        jsonObjet['country'] = zipcode["City"]
        jsonObjet['name'] = zipcode["State"]
        jsonObjet['z'] = code[1]
        jsonObjet['y'] = code[1]
        data.append(jsonObjet)
    jO = {}
    jO ['data'] = data
    jO['categoris'] = listZCode
    jsonArray.append(jO)
    return json.dumps(jsonArray)

def getGenreMostViewJson():
    data = {}
    listUsers = []
    jsonArray = []
    listMovie = []
    dic = {'Action':0,'Adventure':0,'Animation':0,'Children\'s':0,'Comedy':0,'Crime':0,'Documentary':0,'Drama':0
          ,'Fantasy':0,'Film-Noir':0,'Horror':0,'Musical':0,'Mystery':0,'Romance':0,'Sci-Fi':0,'Thriller':0
           ,'War':0,'Western':0}
    listdata = dfJoin.select(dfJoin.UID,dfJoin.Genres).collect()
    for ld in listdata:
        l = ld[1].split('|')
        if ld[0] not in listUsers:
            listMovie = []
            listUsers.append(ld[0])
            for genre in l:
                dic[genre] += 1
                listMovie.append(genre)
        else:
            for genre in l:
                if genre not in listMovie:
                    dic[genre] += 1
                    listMovie.append(genre)
    for d in dic:
        jsonObjet = {}
        jsonObjet['name'] = d
        jsonObjet['y'] = dic[d]
        jsonArray.append(jsonObjet)
    return json.dumps(jsonArray)
                    
def getNbMovieForGenresJson():
    data = {}
    jsonArray = []
    dic = {'Action':0,'Adventure':0,'Animation':0,'Children\'s':0,'Comedy':0,'Crime':0,'Documentary':0,'Drama':0
          ,'Fantasy':0,'Film-Noir':0,'Horror':0,'Musical':0,'Mystery':0,'Romance':0,'Sci-Fi':0,'Thriller':0
           ,'War':0,'Western':0}
    listMovie = dfmovies.select(dfmovies.Genres).collect()
    for movie in listMovie:
        l = movie[0].split('|')
        for genre in l:
            dic[genre] += 1
    for d in dic:
        jsonObjet = {}
        jsonObjet['name'] = d
        jsonObjet['y'] = dic[d]
        jsonArray.append(jsonObjet)
    return json.dumps(jsonArray)


if __name__ == "__main__":
    sc = SparkContext
    spark = SparkSession.builder.appName("SparkProjet").config("spark.some.config.option" , "some-value").getOrCreate()
    dfmovies = spark.read.format("csv").option("header","true").csv('/user/movies.csv')
    dfusers = spark.read.format("csv").option("header","true").csv('/user/users.csv')
    dfratings = spark.read.format("csv").option("header","true").csv('/user/ratings.csv')
    dfJoin = dfusers.alias('u').join(dfratings.alias('ra') , col('u.UID') == col('ra.UserID'))
    dfJoin = dfJoin.alias('jo').join(dfmovies.alias('m') , col('jo.MovieID') == col('m.MID'))
    dfUsersData = spark.read.format('csv').option("header","true").load('/user/usersV2.csv')
    dfMovieData = spark.read.format('csv').option("header","true").load('/user/movieV2.csv') 
    dfJoin = dfJoin.drop("UserID")
    dfJoin = dfJoin.drop("MovieID")
    dfUsersData = dfUsersData.withColumn("view", dfUsersData["view"].cast("double"))
    dfMovieData = dfMovieData.withColumn("view", dfMovieData["view"].cast("double"))
    setSexeJson = getSexeUsersJson()
    setAgeJson = getAgeUsersJson()
    setOccupJson = getOccupationUsersJson()
    setZipJson = getZipCodeUsersJson()
    setGenreMostViewJson = getGenreMostViewJson()
    setNbMovieForGenresJson = getNbMovieForGenresJson()
    application.run(host='ec2-52-19-132-242.eu-west-1.compute.amazonaws.com')

