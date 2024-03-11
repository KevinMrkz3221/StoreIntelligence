from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session, sessionmaker

from src.logger import Logger


### Aqui van los parametros para la conexion con la base de datos
DB_NAME = 'amazonProducts.db'
ENGINE  = create_engine(f'sqlite:///{DB_NAME}', echo=True)


### Se esta configurando el handler de la base de datos
Base = declarative_base()
Session = sessionmaker(bind=ENGINE)
session = Session()

### Objeto logger
## Es el encargado de guardar los log dentro del proceso
## La variable se llama en distintos puntos del proceso para guardar las acciones de interes
logger = Logger('amazon.log')
