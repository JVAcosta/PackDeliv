# coding=utf-8
import enum
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy import ForeignKey, Date, Float, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker, relationship
from Rest_utils.entities_atributes_Names import *  #(dont work in RestApi.py -->fix it)

Base = declarative_base()

class Adress(Base):
    __tablename__= ADRESS

    id= Column(ADRESS_ID,Integer,primary_key=True)
    street = Column(ADRESS_STREET, String(255), nullable=False)
    number = Column(ADRESS_NUMBER,String(255), nullable=False)
    complement = Column(ADRESS_COMPLEMENT,String(255))
    district = Column(ADRESS_DISTRICT,String(255), nullable=False)
    postal_code= Column(ADRESS_POSTAL_CODE, String(255), nullable= False)
    city = Column(ADRESS_CITY, String(255), nullable=False)
    state = Column(ADRESS_STATE, String(255),nullable=False)
    country = Column(ADRESS_COUNTRY,String(255),nullable=False)
    lat=Column(LOCALIZATION_LAT,Float(), nullable=False)
    long=Column(LOCALIZATION_LONG,Float(), nullable=False)

    id_company=Column(COMPANY+'_'+COMPANY_ID,Integer, ForeignKey(COMPANY+'.'+COMPANY_ID))
    id_client=Column(CLIENT+'_'+CLIENT_ID,Integer, ForeignKey(CLIENT+'.'+CLIENT_ID))

    type=Column(ADRESS_TYPE, Enum('endereco_empresa_matriz','endereco_empresa','endereco_cliente'))

    def as_dict(self):
     return { ADRESS_ID: self.id,
              ADRESS_STREET: self.street,
              ADRESS_NUMBER: self.number,
              ADRESS_COMPLEMENT: self.complement,
              ADRESS_DISTRICT: self.district,
              ADRESS_CITY: self.city,
              ADRESS_STATE: self.state,
              ADRESS_COUNTRY: self.country,
              LOCALIZATION_LAT: self.lat,
              LOCALIZATION_LONG: self.long,
              COMPANY+'_'+COMPANY_ID: self.id_company,
              CLIENT+'_'+CLIENT_ID: self.id_client,
              ADRESS_TYPE: self.type

              }
    def __str__(self):
        dic = self.as_dict()
        string='{ '
        for i,j in dic.items():
            string+= str(i) + ' : ' + str(j) + ',\n'
        string=string[:len(string)-2]
        string+=' }'
        return string


class Client(Base):
    __tablename__=CLIENT

    id= Column(CLIENT_ID,Integer,primary_key=True)
    upi=Column(CLIENT_UPI,String(11),unique=True)#unique company identifier
    name=Column(CLIENT_NAME,String(255),nullable=False)
    adresses=relationship(Adress.__name__)

    def as_dict(self):
     return { CLIENT_ID: self.id,
              CLIENT_UPI: self.upi,
              CLIENT_NAME: self.name,
              ADRESSES: self.adresses,
              }

    def __str__(self):
        dic = self.as_dict()
        string='{ '
        for i,j in dic.items():
            string+= str(i) + ' : ' + str(j) + ',\n'
        string=string[:len(string)-2]
        string+=' }'
        return string

class Vehicle(Base):
    __tablename__= VEHICLE

    id= Column(VEHICLE_ID,Integer,primary_key=True)
    licence_plate = Column(VEHICLE_LICENSE_PLATE, String(255),unique=True, nullable=False)
    year=Column(VEHICLE_YEAR, Integer,nullable=False)
    model = Column(VEHICLE_MODEL,String(255),nullable=False)
    color =Column(VEHICLE_COLOR,String(255))
    ready=Column(VEHICLE_READY, Boolean, default=False)
    volume=Column(VEHICLE_VOLUME,Integer,nullable=False)


    def as_dict(self):
     return { VEHICLE_ID: self.id,
              VEHICLE_LICENSE_PLATE: self.licence_plate,
              VEHICLE_YEAR: self.year,
              VEHICLE_MODEL: self.model,
              VEHICLE_COLOR: self.color,
              VEHICLE_READY: self.ready,
              VEHICLE_VOLUME: self.volume}

    def __str__(self):
        dic = self.as_dict()
        string='{ '
        for i,j in dic.items():
            string+= str(i) + ' : ' + str(j) + ',\n'
        string=string[:len(string)-2]
        string+=' }'
        return string


    def as_dict(self):
     return { VEHICLE_ID: self.id,
              VEHICLE_LICENSE_PLATE: self.licence_plate,
              VEHICLE_YEAR: self.year,
              VEHICLE_MODEL: self.model,
              VEHICLE_COLOR: self.color,
              VEHICLE_READY: self.ready,
              VEHICLE_VOLUME: self.volume }

    def __str__(self):
        dic = self.as_dict()
        string='{ '
        for i,j in dic.items():
            string+= str(i) + ' : ' + str(j) + ',\n'
        string=string[:len(string)-2]
        string+=' }'
        return string


class Company(Base):
    __tablename__=COMPANY

    id=Column(COMPANY_ID, Integer, primary_key=True)
    name_company=Column(COMPANY_NAME,String(255),nullable=False)
    password = Column(COMPANY_PASSWORD,String(255),nullable=False)
    login=Column(COMPANY_LOGIN,String(255),unique=True,nullable=False)
    email=Column(COMPANY_EMAIL,String(255),unique=True,nullable=False)
    uci=Column(COMPANY_UCI,String(14),unique=True)#unique company identifier
    type=Column(COMPANY_TYPE, String(255))
    adresses=relationship(Adress.__name__)
    __mapper_args__ = {
        'polymorphic_identity': COMPANY,
        'polymorphic_on':type
    }
    #o enum ja trata sem precisar utilizar uma especialização
    #adicionar o relacionamento com endereço de empresa
    #utilizar  Query-Enabled Properties para os dois endereços,
    #pois desse modo daria para manter os enums?
    #adicionar o relacionamento com endereço(esse é pra multiplos endereços de entrega)
    def as_dict(self):
     return { COMPANY_ID: self.id,
              COMPANY_NAME: self.name_company,
              COMPANY_EMAIL: self.email,
              COMPANY_UCI: self.uci,
              COMPANY_TYPE: self.type,
              ADRESSES: self.adresses}

    def __str__(self):
        dic = self.as_dict()
        string='{ '
        for i,j in dic.items():
            string+= str(i) + ' : ' + str(j) + ',\n'
        string=string[:len(string)-2]
        string+=' }'
        return string

class Deliveryman(Company):
    __tablename__=DELIVERYMAN
    id = Column(DELIVERYMAN_ID,Integer, ForeignKey(Company.id), primary_key=True)
    name_deliveryman=Column(DELIVERYMAN_NAME,String(255),nullable=False)
    dui=Column(DELIVERYMAN_DUI,String(255),unique=True,nullable=False)
    status=Column(DELIVERYMAN_STATUS,Boolean, default=False)
    ready=Column(DELIVERYMAN_READY,Boolean, default=False)
    lat=Column(LOCALIZATION_LAT,Float(), nullable=False)
    long=Column(LOCALIZATION_LONG,Float(), nullable=False)
    Id_veiculo=Column(DELIVERYMAN_ID_VEHICLE,Integer,ForeignKey(Vehicle.id))

    vehicle=relationship(Vehicle.__name__)
    __mapper_args__ = {
        'polymorphic_identity':DELIVERYMAN,
    }

    def as_dict(self):
     return { DELIVERYMAN_ID: self.id,
              DELIVERYMAN_NAME: self.name_deliveryman,
              DELIVERYMAN_DUI: self.email,
              DELIVERYMAN_STATUS: self.status,
              DELIVERYMAN_READY: self.ready,
              LOCALIZATION_LAT: self.lat,
              LOCALIZATION_LONG: self.long,
              VEHICLE: self.vehicle
              }

    def __str__(self):
        dic = self.as_dict()
        string='{ '
        for i,j in dic.items():
            string+= str(i) + ' : ' + str(j) + ',\n'
        string=string[:len(string)-2]
        string+=' }'
        return string


    #adicionar o relacionamento com entregas para que possa se realizar a lista de pacotes


class Package(Base):
    __tablename__=PACKAGE
    id=Column(PACKAGE_ID, Integer, primary_key=True)
    width=Column(PACKAGE_WIDTH,Integer,nullable=False)
    height=Column(PACKAGE_HEIGHT,Integer,nullable=False)
    length=Column(PACKAGE_LENGTH,Integer,nullable=False)
    weight=Column(PACKAGE_WEIGHT,Integer,nullable=False)
    shiped=Column(PACKAGE_SHIPPED,Boolean, default=False)
    received=Column(PACKAGE_RECEIVED,Boolean, default=False)
    volume=Column(PACKAGE_VOLUME,Integer,nullable=False)
    static_location=Column(PACKAGE_CURRENT_STATIC_LOCATION,String(255))
    status=Column(PACKAGE_STATUS, Enum('em fila para coleta','em fila para entrega','em analise','entregue','em coleta','em entrega'))
    id_adress_start=Column(PACKAGE_ID_ADRESS_START,Integer)#adress company id
    id_adress_destiny=Column(PACKAGE_ID_ADRESS_DESTINY,Integer)#adress client id


    #adresses=relationship(Adress.__name__)
    #deliveries=relationship(Delivery.__name__, back_populates="package")
    #adress posuira dois endereços a diferença estará no tipo, tentar especificar como o
    #join do relacionamento irá funcionar para que ele mantenha as duas keys estrangeiras
    #tentar manter o __name__ em Delivery no outro relacionamento, caso não consiga
    # por o nome direto

    def as_dict(self):
     return { PACKAGE_ID: self.id,
              PACKAGE_WIDTH: self.width,
              PACKAGE_HEIGHT: self.height,
              PACKAGE_LENGTH: self.length,
              PACKAGE_WEIGHT: self.weight,
              PACKAGE_SHIPPED: self.shiped,
              PACKAGE_RECEIVED: self.received,
              PACKAGE_VOLUME: self.volume,
              PACKAGE_ID_ADRESS_START: self.id_adress_start,
              PACKAGE_ID_ADRESS_DESTINY: self.id_adress_destiny
              }

    def __str__(self):
        dic = self.as_dict()
        string='{ '
        for i,j in dic.items():
            string+= str(i) + ' : ' + str(j) + ',\n'
        string=string[:len(string)-2]
        string+=' }'
        return string

class Delivery(Base):
    __tablename__=DELIVERY

    id=Column(DELIVERY_ID, Integer, primary_key=True)
    code=Column(DELIVERY_IDENTIFIER_CODE, String(255))
    shipping_date=Column(DELIVERY_SHIPPING_DATE,DateTime, default=datetime.datetime.utcnow)
    finalization_date=Column(DELIVERY_FINALIZATION_DATE,DateTime, default=False)
    id_service_order=Column(DELIVERY_ID_SERVICE_ORDER,ForeignKey(SERVICE_ORDER+'.'+SERVICE_ORDER_ID))
    id_package=Column(DELIVERY_ID_PACKAGE,Integer,ForeignKey(PACKAGE+'.'+PACKAGE_ID))
    status=Column(DELIVERY_STATUS, Enum('entregador designado para a coleta','entregador a caminho para coleta',
    'saiu para entrega','a caminho da casa do cliente','entrega finalizada','coleta finalizada'))
    type=Column(DELIVERY_TYPE, Enum('entrega','coleta'))
    package=relationship(Package.__name__)

    def as_dict(self):
     return { DELIVERY_ID: self.id,
              DELIVERY_IDENTIFIER_CODE: self.code,
              DELIVERY_SHIPPING_DATE: self.shipping_date,
              DELIVERY_FINALIZATION_DATE: self.length,
              DELIVERY_ID_SERVICE_ORDER: self.weight,
              DELIVERY_STATUS: self.status,
              DELIVERY_TYPE: self.type,
              PACKAGE: self.package
              }

    def __str__(self):
        dic = self.as_dict()
        string='{ '
        for i,j in dic.items():
            string+= str(i) + ' : ' + str(j) + ',\n'
        string=string[:len(string)-2]
        string+=' }'
        return string

class Service_order(Base):
    __tablename__=SERVICE_ORDER

    id=Column(SERVICE_ORDER_ID, Integer, primary_key=True)
    code=Column(SERVICE_ORDER_IDENTIFIER_CODE,String(255),unique=True,nullable=False)
    shipping_date=Column(SERVICE_ORDER_SHIPPING_DATE,DateTime, default=datetime.datetime.utcnow)
    finalization_date=Column(SERVICE_ORDER_FINALIZATION_DATE,DateTime, default=False)
    status = Column(SERVICE_ORDER_STATUS, Enum('em analise','confirmado','finalizado'))
    deliveries=relationship(Delivery.__name__)
    #adionar o relacionamento com ordem de serviço e pacote
    def as_dict(self):
     return { SERVICE_ORDER_ID: self.id,
              SERVICE_ORDER_IDENTIFIER_CODE: self.code,
              SERVICE_ORDER_SHIPPING_DATE: self.shipping_date,
              SERVICE_ORDER_FINALIZATION_DATE: self.finalization_date,
              DELIVERIES: self.deliveries
              }

    def __str__(self):
        dic = self.as_dict()
        string='{ '
        for i,j in dic.items():
            string+= str(i) + ' : ' + str(j) + ',\n'
        string=string[:len(string)-2]
        string+=' }'
        return string


def getEngine():

    user ="root"
    password=""
    adress="localhost"
    database_name="packDeliv"
    engine = create_engine('mysql+pymysql://%s:%s@%s/%s'%(user, password, adress, database_name), echo=True)


    return engine

def INIT_API():
    engine = getEngine()
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)

def getSession():
    engine = getEngine()
    Session=sessionmaker(bind=engine)
    return Session()
