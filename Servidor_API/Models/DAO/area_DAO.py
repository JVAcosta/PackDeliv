from Models.DB.DB_helper import getSession, Area, Package
from Models.DAO.DAO_utils import printError,checkType, changeEditedAttr

class AreaDao():
    def __init__(self):
        pass

    def save(self, area):
        session = getSession()
        checkType('Area', area)
        id_list = [package.id for package in area.packages]
        setattr(area, 'packages', [])
        session.add(area)
        session.commit()
        session.refresh(area)
        id_area = area.id
        session.close()
        session = getSession()
        packages = session.query(Package).filter(Package.id.in_( id_list)).all()
        for package in packages :
            package.id_area = id_area
        session.add_all(packages)
        session.commit()
        session.close()

        return area.id

    def update(self,editedArea):
        session = getSession()
        response = None
        try:
            checkType('Area',editedArea)
            area=session.query(Area).filter(Area.id == editedArea.id).first()
            if area != None:
                area=changeEditedAttr(area,editedArea)
                session.add(area)
                session.commit()
                session.close()
                response = True
            else:
                response = False

        except:
            printError()
            response = False

        return response

    def delete(self,id):
        session = getSession()
        try:
            deleted_rows = session.query(Area).filter(Area.id == id).delete()
            session.commit()
            session.close()
            return deleted_rows == 1
        except:
            printError()
            return False

    def select(self,id=None):
        session = getSession()
        try:
            if id == None:
                response=session.query(Area).all()
                response=[area for area in response]
            else:
                response=session.query(Area).filter(Area.id == id).all()
                response=response[0]
            return response
        except:
            printError()
            return None
