#You need easy_install or pip install SqlAlchemy
#For MSSQL Server you need pyODBC for SqlAlchemy

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


#Your current Wordpress database
engineSource = create_engine("mssql://user:pw@localhost\INSTANCE/database")
#Ghost's database
engineDesination = create_engine('mysql://user:pw@localhost/database')

meta = MetaData()
postsDest = Table('posts', meta, autoload=True, autoload_with=engineDesination)
postsSource = Table('wp_posts', meta, autoload=True, autoload_with=engineSource)
conn = engineDesination.connect()
Session = sessionmaker(bind=engineSource)
session = Session()
#There is a filter to migrate just published posts. If you want to carry your draft posts too, you need to code a little because statuses are not the same!!
#All posts created by Ghost user who's id is 1
for row in session.query(postsSource).filter_by(post_status='publish').all():     
     ins = postsDest.insert().values(uuid=row.guid, title=row.post_title, slug=row.post_name, markdown=row.post_content, html=row.post_content,  featured=0, page=0, status='published', language='en_US',  author_id=1, created_at=row.post_date, created_by=1, updated_at=row.post_date, updated_by=1, published_at=row.post_date, published_by=1)
     conn.execute(ins)




