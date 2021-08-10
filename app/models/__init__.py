from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import DeclarativeMeta

db = SQLAlchemy()

def commit(data):
    if isinstance(data, list):
            db.session.add_all(data)
    else:
        db.session.add(data)
    
    db.session.commit()

def serialize(data, depth=1, avoid=['password', 'money']):
    depth -= 1
    
    encoded_data = {}
    for column in data.__table__.columns:
        if column.name not in avoid:
            encoded_data[column.name] = getattr(data, column.name)
    
    if depth:
        for attr, relation in data.__mapper__.relationships.items():
            if relation.key in avoid:
                continue
            
            value = getattr(data, attr)
            if value is None:
                encoded_data[relation.key] = None
            elif isinstance(value.__class__, DeclarativeMeta):
                encoded_data[relation.key] = serialize(value, depth, avoid)
            else:
                encoded_data[relation.key] = [serialize(i, depth, avoid) for i in value]
    
    return encoded_data