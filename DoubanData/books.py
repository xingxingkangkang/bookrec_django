class Book(object):
    def __init__(self, detail):
        fields = detail.split(",")
        self.name = fields[0]
        self.author = fields[1]
        self.img = fields[2]
        self.price = fields[3]
        self.publish_time = fields[4]
        self.score = fields[5]
        self.judge = fields[6]
        self.rec_most = fields[7]
        self.rec_more = fields[8]
        self.rec_normal = fields[9]
        self.rec_bad = fields[10]
        self.rec_worst = fields[11]
        self.readed = fields[12]
        self.reading = fields[13]
        self.readup = fields[14]
        self.mess = fields[15]
        self.tag = fields[16]

    def to_sql(self):
        return "INSERT INTO book VALUES (null,'" + self.name + "','" + self.author +\
               "','" + self.img + "'," + self.price + ",'" + self.publish_time + \
               "'," + self.score + "," + self.judge + "," + self.rec_most + \
               "," + self.rec_more + "," + self.rec_normal + "," + self.rec_bad + \
               "," + self.rec_worst + "," + self.readed + "," + self.reading + \
               "," + self.readup + ",'" + self.mess + "','" + self.tag + "');"
