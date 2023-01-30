import psycopg2 as pc2

class DB():
    def __init__(self, dbname):
        self.db = pc2.connect(
                                host='localhost',
                                dbname = dbname,
                                user='sineu',
                                password='dmscks1!',
                                port=5432
                                )
        print("\n=== NOTE : DB is now CONNECTED ===\n")
        # self.cursor = self.db.cursor()

    def execute(self, query):
        self.db.cursor().execute(query)


    def insert_info(self, movie_id, title, title_eng, director, year, rating):
        query = f'''
                INSERT INTO Movies (Movie_id, Title, Title_eng, Director, Year, Rating)
                    VALUES ({movie_id}, $$'{title}'$$, $$'{title_eng}'$$, $$'{director}'$$, '{year}', {rating});
    
                ''' 
        self.execute(query)
    
    def insert_review(self, movie_id, rating, content):
        
        query = f'''
                    INSERT INTO Reviews (Movie_id, Rating, Content)
                        VALUES ({movie_id}, {rating}, $$'{content}'$$);
                '''
        self.execute(query)

    def commit(self):
        self.db.commit()

    def execute_only_once(self):
        query = f'''
                DROP TABLE IF EXISTS Reviews;
                DROP TABLE IF EXISTS Movies;

                CREATE TABLE IF NOT EXISTS Movies (
                        Movie_id SERIAL primary key,
                        Title VARCHAR(100) not null,
                        Title_eng VARCHAR(100),
                        Director VARCHAR(30) not null,
                        Year VARCHAR(4) not null,
                        Rating float,
                        UNIQUE (Title, Director, Year)
                );
                CREATE TABLE IF NOT EXISTS Reviews (
                        Movie_id int REFERENCES Movies(Movie_id),
                        Content VARCHAR(1000),
                        Rating int
                        
                );
                '''
        self.execute(query)
        self.commit()
            
    


    


