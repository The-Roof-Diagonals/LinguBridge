import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


HOST="aws.connect.psdb.cloud"
USERNAME="xh3l9a1q7xhnvs68gfa6"
PASSWORD="pscale_pw_hIQNkoSX1RMJmlLr6lrBLshNOiInHAhDkdA3zVBn6ny"
DATABASE="tumaitest"

engine = create_engine(f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}")

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.VARCHAR(255))
    address = sqlalchemy.Column(sqlalchemy.VARCHAR(255))
    date = sqlalchemy.Column(sqlalchemy.DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "date": self.date,
        }
    
class Task(Base):
    __tablename__ = 'tasks'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.VARCHAR(255))
    project_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    created = sqlalchemy.Column(sqlalchemy.DateTime, default=sqlalchemy.func.now())
    updated = sqlalchemy.Column(sqlalchemy.DateTime, default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now())
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'project_id': self.project_id,
            'active': self.active,
            'created': self.created.strftime("%Y-%m-%d %H:%M:%S"),
            'updated': self.updated.strftime("%Y-%m-%d %H:%M:%S"),
        }

class File(Base):
    __tablename__ = 'files'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.VARCHAR(255))
    task_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    created = sqlalchemy.Column(sqlalchemy.DateTime, default=sqlalchemy.func.now())
    updated = sqlalchemy.Column(sqlalchemy.DateTime, default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now())
    language= sqlalchemy.Column(sqlalchemy.VARCHAR(3))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'task_id': self.task_id,
            'created': self.created,
            'updated': self.updated,
            'language': self.language
        }


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()

def create_Project(name, address, date):
    session = Session()
    project = Project(name=name, address=address, date=date)
    session.add(project)
    session.commit()
    session.close()

def create_Task(name, project_id):
    session = Session()
    task = Task(name=name, project_id=project_id)
    session.add(task)
    session.commit()
    session.close()
    return task.id

def get_Tasks_for_Project(project_id):
    session = Session()
    res = session.query(Task).filter_by(project_id=project_id).all()
    session.close()
    return res

def create_File(name, task_id, language):
    session = Session()
    file = File(name=name, task_id=task_id, language=language)
    session.add(file)
    session.commit()
    session.close()

def get_Project(id):
    session = Session()
    res = session.query(Project).filter_by(id=id).first()
    session.close()
    return res

def get_all_Projects():
    session = Session()
    res = session.query(Project).all()
    session.close()
    return res

def get_Task(id):
    session = Session()
    res = session.query(Task).filter_by(id=id).first()
    session.close()
    return res

def get_all_Tasks(project_id):
    session = Session()
    res = session.query(Task).filter_by(project_id=project_id).all()
    session.close()
    return res

def get_File(id):
    session = Session()
    res = session.query(File).filter_by(id=id).first()
    session.close()
    return res

def get_all_Files(task_id):
    session = Session()
    res = session.query(File).filter_by(task_id=task_id).all()
    session.close()
    return res

def update_Task(id):
    session = Session()
    session.query(Task).filter_by(id=id).update({"active": False})
    session.commit()
    session.close()



