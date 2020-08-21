# Here's how SQLAlchemy works

# Import your model -> Article, and special Session class
from models import Article, Session

# Create an Article

a = Article()
a.title = "my article"

# Save it
a.save()

# Query for it
session = Session()
session.query(Article).all()
articles = session.query(Article).filter(Article.title == "my article").all()

# Print em out
for art in articles:
    print("Article (id=", art.id, "title=", art.title)
