import pandas as pd
import os
from dotenv import load_dotenv
from config.Neo4j import Neo4J

load_dotenv()
import logging
logger = logging.getLogger(__name__)

logging.basicConfig(filename="app.log",level=logging.INFO,format='[%(filename)s:%(lineno)s - %(funcName)20s() ] %(asctime)s - %(levelname)s - %(message)s'
                    ,datefmt='%Y-%m-%d %H:%M:%S')

BASE_DIR = os.getenv('BASE_DIR')
class neo4j_writer:
    def __init__(self,connection):
        self.connection = connection

    def write_persons(self,tx):
        person_file_dir=os.getenv("PERSON_DIR")
        pd_persons=pd.read_csv(person_file_dir)
        persons_dql = pd.DataFrame(columns=pd_persons.columns)
        for _,person in  pd_persons.iterrows():
            try:
                query = "CREATE (n:Student {Id:$id,Name: $name, Age: $age, Major: $major})"
                tx.run(query, name=person["Name"], age=person["Age"], id=person["Student_Id"], major=person["Major"])
            except Exception as e:
                print(e)
                logger.error(f"{e} ,{person}")
                failed_row = pd.DataFrame([person])
                persons_dql = pd.concat([persons_dql, failed_row], ignore_index=True)

        if not persons_dql.empty:
            persons_dql.to_csv(f"{BASE_DIR}dql/persons_dql.csv",mode='a',index=False,header=not os.path.exists(f"{BASE_DIR}dql/persons_dql.csv"))

    def write_courses(self,tx):
        course_file_dir=os.getenv("COURSE_DIR")
        pd_courses=pd.read_csv(course_file_dir)
        courses_dql = pd.DataFrame(columns=pd_courses.columns)
        for _,course in pd_courses.iterrows():
            try:
                query = "CREATE (n:Course {Id:$id,Name: $name, Tutor: $tutor})"
                tx.run(query, id=course["Course_Id"], name=course["Course_Name"], tutor=course["Course_Tutor"])

            except Exception as e:
                print(e)
                logger.error(f"{e} ,{course}")
                failed_row = pd.DataFrame([course])
                courses_dql = pd.concat([courses_dql, failed_row], ignore_index=True)

        if not courses_dql.empty:
            courses_dql.to_csv(f"{BASE_DIR}/courses_dql.csv",mode='a',index=False,header=not os.path.exists(f"{BASE_DIR}dql/courses_dql.csv"))

    def write_country(self, tx):
        country_file_dir = os.getenv("COUNTRY_DIR")
        pd_country = pd.read_csv(country_file_dir)
        country_dql = pd.DataFrame(columns=pd_country.columns)
        for _, country in pd_country.iterrows():
            try:
                query = "CREATE (n:Country {Name:$name,Code: $code})"
                tx.run(query, code=country["Country_Code"], name=country["Country_Name"])
            except Exception as e:
                print(e)
                logger.error(f"{e} ,{country}")
                failed_row = pd.DataFrame([country])
                country_dql = pd.concat([country_dql, failed_row], ignore_index=True)

        if not country_dql.empty:
            country_dql.to_csv(f"{BASE_DIR}dql/country_dql.csv", mode='a', index=False, header=not os.path.exists(f"{BASE_DIR}dql/country_dql.csv"))


    def assign_friends_relation_ship(self,tx):
        friends_file_dir=os.getenv("FRIENDS_DIR")
        pd_friends=pd.read_csv(friends_file_dir)
        friends_dql = pd.DataFrame(columns=pd_friends.columns)
        for _,friend in pd_friends.iterrows():
            try:
                query = ("MATCH (StudentA: Student {Id:$studentA}), (StudentB: Student {Id:$studentB}) MERGE (StudentA)-[:FRIENDS_WITH]->(StudentB) MERGE (StudentB)-[:FRIENDS_WITH]->(StudentA)")
                tx.run(query, studentA=friend["StudentA"], studentB=friend["StudentB"])
            except Exception as e:
                print(e)
                logger.error(f"{e} ,{friend}")
                failed_row = pd.DataFrame([friend])
                friends_dql = pd.concat([friends_dql, failed_row], ignore_index=True)
        if not friends_dql.empty:
            friends_dql.to_csv(f"{BASE_DIR}dql/friends_dql.csv", mode='a', index=False, header=not os.path.exists(f"{BASE_DIR}dql/friends_dql.csv"))

    def assign_country_of_origin_relationship(self,tx):
        country_of_orign_relationship_file_dir=os.getenv("COUNTRY_OF_ORIGN_DIR")
        pd_country=pd.read_csv(country_of_orign_relationship_file_dir)
        country_of_orign_relationship_dql = pd.DataFrame(columns=pd_country.columns)
        for _,country in pd_country.iterrows():
            try:
                query= ("MATCH (stud: Student {Id:$student_id}), (coun: Country {Code:$country_code})  MERGE (stud)-[:IS_FROM]->(coun)")
                tx.run(query, student_id=country["Student_Id"], country_code=country["Country"])
            except Exception as e:
                print(e)
                logger.error(f"{e} ,{country}")
                failed_row = pd.DataFrame([country])
                country_of_orign_relationship_dql = pd.concat([country_of_orign_relationship_dql, failed_row], ignore_index=True)
        if not country_of_orign_relationship_dql.empty:
            country_of_orign_relationship_dql.to_csv(f"{BASE_DIR}dql/country_of_orign_relationship_dql.csv", mode='a', index=False,
                                                     header=not os.path.exists(f"{BASE_DIR}dql/country_of_orign_relationship_dql.csv"))


    def assign_enrolled_in_relationship(self,tx):
        enrolled_in_relationship_file_dir=os.getenv("ENROLLED_IN_DIR")
        pd_enrolled=pd.read_csv(enrolled_in_relationship_file_dir)
        enrolled_in_relationship_dql = pd.DataFrame(columns=pd_enrolled.columns)
        for _,enrolled in pd_enrolled.iterrows():
            try:
                query= ("MATCH (stud: Student {Id:$Student_id}),(cours: Course {Id:$Course_Id}) MERGE (stud)-[:ENROLLED_IN]->(cours)")
                tx.run(query, Course_Id=enrolled["Course_Id"], Student_id=enrolled["Student_Id"])
            except Exception as e:
                print(e)
                logger.error(f"{e} ,{enrolled}")
                failed_row = pd.DataFrame([enrolled])
                enrolled_in_relationship_dql = pd.concat([enrolled_in_relationship_dql, failed_row], ignore_index=True)
        if not enrolled_in_relationship_dql.empty:
            enrolled_in_relationship_dql.to_csv(f"{BASE_DIR}dql/enrolled_in_relationship_dql.csv", mode='a', index=False,
                                                     header=not os.path.exists(f"{BASE_DIR}dql/enrolled_in_relationship_dql.csv"))





    def perform_write_actions(self):
        with self.connection.session() as session:
            self.write_persons(session)
            self.write_courses(session)
            self.write_country(session)
            self.assign_friends_relation_ship(session)
            self.assign_country_of_origin_relationship(session)
            self.assign_enrolled_in_relationship(session)


if __name__ == '__main__':
    neo4j= Neo4J()
    neo4j_writer=neo4j_writer(neo4j.getConnection())
    neo4j_writer.perform_write_actions()





