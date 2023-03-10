from config import config
import psycopg2 as pc2


class DB():
    def __init__(self):
        self.conn = None
        try:
            params = config()
            self.conn = pc2.connect(**params)
            self.cur = self.conn.cursor()

            self.cur.execute('SELECT version()')
            db_version = self.cur.fetchone()
            print(f"PostgreSQL Database version : {db_version}")
        except (Exception, pc2.DatabaseError) as error:
            print(error)

    def execute(self, query):

        self.cur.execute(query)
    
    def insert_info(self, movie_id, title, title_eng, director, year, rating, explanation):
        query = f'''
                INSERT INTO Movies (movie_id, Title, Title_eng, Director, Year, Rating, content)
                    VALUES ({movie_id}, $$'{title}'$$, $$'{title_eng}'$$, $$'{director}'$$, '{year}', {rating}, $$'{explanation}'$$);
    
                ''' 
        self.execute(query)
    
    def insert_review(self, movie_id, rating, content):
        
        query = f'''
                    INSERT INTO Reviews (Movie_id, Rating, Content)
                        VALUES ({movie_id}, {rating}, $$'{content}'$$);
                '''
        self.execute(query)

    def commit(self):
        self.conn.commit()


    #왜 fetchone은 내부함수로 돌리면 안되고 꼭 db.cur.fetchone()으로만 가능할까?
    def fetchone(self):
        return self.cur.fetchone()
    
    def fetchmany(self, count):
        return self.cur.fetchmany(count)

    def fetchall(self):
        return self.cur.fetchall()

    def execute_only_once(self):
        query = f'''
                DROP TABLE IF EXISTS Reviews;
                DROP TABLE IF EXISTS Movies;

                CREATE TABLE IF NOT EXISTS movies (
                    movie_id SERIAL primary key, 
                    title varchar(100) not null, 
                    title_eng varchar(100), 
                    director varchar(30) not null, 
                    content text,
                    year varchar(4) not null, 
                    Rating float, 
                    published boolean, 
                    UNIQUE (title, director, year)
                    );
                CREATE TABLE IF NOT EXISTS Reviews (
                        Movie_id int REFERENCES Movies(Movie_id),
                        Content VARCHAR(1000),
                        Rating int
                        
                );
                '''
        self.execute(query)
        self.commit()

