from sqlalchemy import Table, MetaData,Column, String,Integer,Sequence,Text,DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
Base = declarative_base()
DB_CON_STR = 'mysql://root:123456Aa@localhost:3306/SpAppDb?charset=utf8'
engine = create_engine(DB_CON_STR, echo=False)

class searchrecoder(Base):
   
    """ 定义了三个字段， 数据库表名为model名小写
    """
    __tablename__ = 'searchrecoder'
    reqid = Column(Integer, primary_key=True, autoincrement=True)
    reqloc =  Column(String(250))
    reqkeywds = Column(String(250))
    remark =  Column(Text)
    recommendsite = Column(String(250))
    addTime=Column(String(250))

class dbcall:
      reqloc =''
      reqkeywds = ''
      remark = ''  
      recommendsite=''
      
      def __init__(self, reqloc, reqkeywds, remark, recommendsite):
            self.remark=remark
            self.reqkeywds=reqkeywds
            self.recommendsite=recommendsite
            self.reqloc=reqloc

      def save(self):
            Session = sessionmaker(bind=engine)
            session = Session()
        
            obj = searchrecoder(reqid=0, reqloc=self.reqloc,reqkeywds=self.reqkeywds,recommendsite=self.recommendsite,remark=self.remark,addTime=datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S'))
            session.add(obj)
            session.commit()


