# Here's how SQLAlchemy works

# Import your model -> Article, and special Session class
from db import Article, Session

# Create an Article

a = Article()
a.title = "my article"
session = Session()
session.add(a)

# Save it
session.commit()

# Query for it
session.query(Article).all()
articles = session.query(Article).filter(Article.title == "my article").all()

# Print em out
for art in articles:
    print("Article (id=", art.id, "title=", art.title)
