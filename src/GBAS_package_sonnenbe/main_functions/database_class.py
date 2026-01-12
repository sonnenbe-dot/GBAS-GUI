
import sqlite3 as sq

def main():

    return 0

class local_database_sqlite():
    def __init__(self, db_path):
        self.connection = sq.connect(db_path)
        self.cursor = self.connection.cursor() #NOT NULL PRIMARY KEY
    
    def create_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS table_project(
                            projectname VARCHAR(20) NOT NULL,
                            ploidy VARCHAR(20) NOT NULL,
                            CONSTRAINT PK_table_poject PRIMARY KEY(projectname)
                    );""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS table_loci(
                            Locusname VARCHAR(20) NOT NULL,
                            Forwardsequence VARCHAR(200) NOT NULL,
                            Lengthforwardsequence INT NOT NULL,
                            Reversesequence VARCHAR(200) NOT NULL,
                            Lengthreversesequence INT NOT NULL,
                            CONSTRAINT PK_table_loci PRIMARY KEY(Locusname)
                    );""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS table_sample(
                            SampleID VARCHAR(20) NOT NULL,
                            projectname VARCHAR(20) NOT NULL, 
                            Metadata2 VARCHAR(20),
                            Metadata3 VARCHAR(20),
                            Metadata4 VARCHAR(20),
                            CONSTRAINT FK_table_project_table_sample FOREIGN KEY(projectname) REFERENCES table_project,
                            CONSTRAINT PK_table_sample PRIMARY KEY(SampleID)

                    );""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS table_allele(
                            Alleleindex VARCHAR(20) NOT NULL,
                            Locusname VARCHAR(20) NOT NULL,
                            Sequencelength INT NOT NULL,
                            Sequenceread VARCHAR[MAX] NOT NULL,
                            CONSTRAINT FK_table_loci_table_allele FOREIGN KEY(Locusname) REFERENCES table_loci,
                            CONSTRAINT PK_table_allele PRIMARY KEY(Alleleindex, Locusname)
                    );""")
                    ##CONSTRAINT unique_sequence UNIQUE (Sequenceread)    
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS beziehung_loci_sample(
                            Locusname VARCHAR(20),
                            SampleID VARCHAR(20),
                            CONSTRAINT FK_beziehung_loci_sample_table_loci FOREIGN KEY(Locusname) REFERENCES table_loci,
                            CONSTRAINT FK_beziehung_loci_sample_table_sample FOREIGN KEY(SampleID) REFERENCES table_sample,
                            CONSTRAINT PK_table_allele PRIMARY KEY(Locusname, SampleID)        
                    );""")


        self.cursor.execute("""CREATE TABLE IF NOT EXISTS beziehung_allele_sample(
                            Alleleindex VARCHAR(20),
                            Locusname VARCHAR(20),
                            SampleID VARCHAR(20),
                            CONSTRAINT FK_beziehung_allele_sample_table_allele FOREIGN KEY(Alleleindex, Locusname) REFERENCES table_allele,
                            CONSTRAINT FK_beziehung_allele_sample_table_sample FOREIGN KEY(SampleID) REFERENCES table_sample,
                            CONSTRAINT PK_beziehung_allele_sample PRIMARY KEY(Alleleindex, Locusname, SampleID)         
                    );""")




        self.connection.commit()

    def closing(self):
        print("Closing the database.")
        self.connection.close()


    def insert_dataset(self, primers_dict : dict, matrix_dict : dict, meta_dict : dict, metadata_headers : list, ploidy : str):
        #samples_already_processed = []
        loci_already_processed = []

        added_sampleIDs = 0
        ignored_sampleIDs = 0
        
        added_sequences = 0
        ignored_sequences = 0

        additional_info = ""

        try:
            if (not(ploidy == "diploid" or ploidy == "haploid")):
                print("\nNeither diploid nor haploid!\n")
                additional_info += "Neither diploid nor haploid!"
                return (False, None, added_sequences, additional_info)

            for sampleID, data in matrix_dict.items():
                if (not(sampleID in meta_dict) and not(matrix_dict[sampleID]["Metadata"])):
                    continue

                list_metadata_values = []
                for i, header in enumerate(metadata_headers, 1):
                    if (header in meta_dict[sampleID]):
                        list_metadata_values.append(meta_dict[sampleID][header])
                    else:
                        list_metadata_values.append("None")
                    if (i == 4):
                        break
                

                row_table_project = (list_metadata_values[0], ploidy)
                query_table_project = """INSERT OR IGNORE INTO table_project
                            (projectname, ploidy) values(?, ?);
                """
                self.cursor.execute(query_table_project, row_table_project)

                # print("HHHEEERE")
                # print(list_metadata_values)
                
                if (len(list_metadata_values) < 4):
                    while (len(list_metadata_values) < 4):
                        list_metadata_values.append("None")

                # print("HHHEEERE")
                # print(list_metadata_values)

                row_table_sample = (sampleID,) + tuple(list_metadata_values)
                query_table_sample = """INSERT OR IGNORE INTO table_sample
                            (SampleID, projectname, Metadata2, Metadata3, Metadata4) values(?, ?, ?, ?, ?);
                """
                self.cursor.execute(query_table_sample, row_table_sample)
                if self.cursor.rowcount > 0:
                    added_sampleIDs += 1
                else:
                    ignored_sampleIDs += 1


                for locus, alleles in data["Loci"].items():
                    # if (not(alleles["Alleles"])):
                    #     continue

                    row_table_beziehung_loci_sample = (locus, sampleID)
                    query_table_beziehung_loci_sample = """INSERT OR IGNORE INTO beziehung_loci_sample
                               (Locusname, SampleID) values(?, ?);
                    """
                    self.cursor.execute(query_table_beziehung_loci_sample, row_table_beziehung_loci_sample)


                    if (locus not in loci_already_processed):
                        forseq = ""
                        reverseseq = ""
                        forseq_length = 0
                        reverseseq_length = 0
                        if (locus in primers_dict["primers"]):
                            forseq = primers_dict["primers"][locus][0]
                            forseq_length = len(forseq)
                            reverseseq = primers_dict["primers"][locus][1]
                            reverseseq_length = len(reverseseq)
                        
                        row_table_loci = (locus, forseq, forseq_length, reverseseq, reverseseq_length)
                        query_table_loci = """INSERT OR IGNORE INTO table_loci
                                   (Locusname, Forwardsequence, Lengthforwardsequence, Reversesequence, Lengthreversesequence) values(?, ?, ?, ?, ?);
                        """
                        self.cursor.execute(query_table_loci, row_table_loci)
                        loci_already_processed.append(locus)
                    

                    query_beziehung_allele_sample = """INSERT OR IGNORE INTO beziehung_allele_sample
                               (Alleleindex, Locusname, SampleID) values(?, ?, ?);
                    """
        
                    query_table_allele = """INSERT OR IGNORE INTO table_allele
                               (Alleleindex, Locusname, Sequencelength, Sequenceread) values(?, ?, ?, ?);
                    """
                    
                    
                    for alleleseq, rest in alleles["Alleles"].items():
                        #print(rest)
                        alleleid = rest["ID"]
                        row_beziehung_allele_sample = (str(alleleid), locus, sampleID)
                        self.cursor.execute(query_beziehung_allele_sample, row_beziehung_allele_sample)
                        
                        length = rest["Length"]
                        read = rest["Read"]
                        row_table_allele = (alleleid, locus, length, read)
                        self.cursor.execute(query_table_allele, row_table_allele)
                        
                        if self.cursor.rowcount > 0:
                            added_sequences += 1
                        else:
                            ignored_sequences += 1

            self.connection.commit()
            return (True, None, added_sequences, additional_info)
        except Exception as e:
            print(f"An Error occurred when adding the dataset into the local database:\n{e}\n")
            return (False, e, added_sequences, additional_info)
    

    def get_view_for_extracting(self):
        self.cursor.execute("DROP VIEW IF EXISTS view_extraction")
        create_view_query_samples = """
            CREATE VIEW IF NOT EXISTS view_extraction AS
            SELECT 
                s.SampleID,
                s.projectname,
                s.Metadata2,
                s.Metadata3,
                s.Metadata4,
                p.ploidy,
                ls.Locusname,
                l.Forwardsequence,
                l.Lengthforwardsequence,
                l.Reversesequence,
                l.Lengthreversesequence,
                a.Alleleindex,
                a.Sequencelength,
                a.Sequenceread
            FROM 
                table_sample s

            INNER JOIN table_project p
                ON s.projectname = p.projectname

            INNER JOIN beziehung_loci_sample ls
                ON s.SampleID = ls.SampleID

            INNER JOIN table_loci l
                ON ls.Locusname = l.Locusname

            LEFT JOIN beziehung_allele_sample bas
                ON bas.SampleID = s.SampleID
                AND bas.Locusname = ls.Locusname

            LEFT JOIN table_allele a
                ON a.Alleleindex = bas.Alleleindex
                AND a.Locusname = bas.Locusname;
        """
        # create_view_query_samples = """
        #     CREATE VIEW IF NOT EXISTS view_extraction AS
        #     SELECT 
        #         s.SampleID,
        #         s.projectname,
        #         s.Metadata2,
        #         s.Metadata3,
        #         s.Metadata4,
        #         p.ploidy,
        #         ls.Locusname,
        #         l.Forwardsequence,
        #         l.Lengthforwardsequence,
        #         l.Reversesequence,
        #         l.Lengthreversesequence,
        #         a.Alleleindex,
        #         a.Sequencelength,
        #         a.Sequenceread
        #     FROM 
        #         table_sample s
        #     INNER JOIN 
        #         table_project p
        #         ON s.projectname = p.projectname
        #     INNER JOIN 
        #         beziehung_loci_sample ls
        #         ON s.SampleID = ls.SampleID
        #     INNER JOIN 
        #         table_loci l
        #         ON ls.Locusname = l.Locusname
        #     LEFT JOIN
        #         table_allele a
        #         ON ls.Locusname = a.Locusname
        #     INNER JOIN
        #         beziehung_allele_sample as
        #         ON s.SampleID = as.SampleID
        #         ON ls.Locusname
        # """
        try:
            self.cursor.execute(create_view_query_samples)
            self.connection.commit()
            print("VIEW 'view_allele_sample' created successfully.")
        except sq.Error as e:
            print(f"An error occurred while creating the VIEW: {e}")

    def get_selected_projects(self, project_include):
        if not project_include:
            print("Error: 'project_include' list is empty.")
            return []
        query = """
            SELECT 
                projectname,
                ploidy
            FROM 
                table_project
            WHERE 
                projectname IN ({include_placeholders_project}) 
        """

        include_placeholders_project = ','.join(['?'] * len(project_include))
        query = query.format(include_placeholders_project=include_placeholders_project)

        # Combine all parameters into a single tuple in the order of placeholders
        parameters = tuple(project_include)

        try:
            self.cursor.execute(query, parameters)
            rows = self.cursor.fetchall()
            print(f"Number of rows fetched: {len(rows)}")
            return rows
        except sq.Error as e:
            print(f"An error occurred while executing the query: {e}")
            return []

    def get_selected_loci_project_metadata(self, project_include, metadata_include, loci_include):
        """
        Retrieves rows from the view_extraction VIEW where:
        - Locusname is in loci_include
        - Project is in project_include
        - metadata is in metadata_include

        Parameters:
            loci_include (list of str): List of Locusname values to include.
            project_include (list of str): List of Project values to include.
            organism_include (list of str): List of Organism values to include.

        Returns:
            list of tuples: Retrieved rows matching the criteria.
        """
        
        # Validate that all input lists are non-empty
        if not loci_include:
            print("Error: 'loci_include' list is empty.")
            return []
        if not project_include:
            print("Error: 'project_include' list is empty.")
            return []
        if not metadata_include:
            print("Error: 'metadata_include' list is empty.")
            return []

        # Prepare the SQL query with placeholders
        query = """
            SELECT 
                SampleID,
                projectname,
                Metadata2,
                Metadata3,
                Metadata4,
                ploidy,
                Locusname,
                Forwardsequence,
                Lengthforwardsequence,
                Reversesequence,
                Lengthreversesequence,
                Alleleindex,
                Sequencelength,
                Sequenceread
            FROM 
                view_extraction
            WHERE 
                Locusname IN ({include_placeholders_loci}) 
                AND projectname IN ({include_placeholders_project}) 
                AND Metadata2 IN ({include_placeholders_metadata})
        """

        # Generate placeholders for each IN clause based on list lengths
        include_placeholders_loci = ','.join(['?'] * len(loci_include))
        include_placeholders_project = ','.join(['?'] * len(project_include))
        include_placeholders_metadata = ','.join(['?'] * len(metadata_include))

        # Format the query with the correct number of placeholders
        query = query.format(
            include_placeholders_loci=include_placeholders_loci,
            include_placeholders_project=include_placeholders_project,
            include_placeholders_metadata=include_placeholders_metadata
        )

        # Combine all parameters into a single tuple in the order of placeholders
        parameters = tuple(loci_include) + tuple(project_include) + tuple(metadata_include)

        # Debug: Print the final query and parameters
        # print("Executing SQL Query:")
        # print(query)
        # print("With Parameters:")
        # print(parameters)

        try:
            # Execute the query with the combined parameters
            self.cursor.execute(query, parameters)
            rows = self.cursor.fetchall()

            # Debug: Print the number of rows fetched
            print(f"Number of rows fetched: {len(rows)}")
            return rows
        except sq.Error as e:
            print(f"An error occurred while executing the query: {e}")
            return []



    def get_view_for_extracting2(self):
        create_view_query = """
            CREATE VIEW IF NOT EXISTS view_allele_sample2 AS
            SELECT 
                t.Locusname,
                t.Alleleindex,
                t.Sequencelength,
                t.Sequenceread,
                b.SampleID,
                s.projectname,
                s.Organism,
                s.Locality,
                s.Country
            FROM 
                table_allele t
            INNER JOIN 
                beziehung_allele_sample b 
                ON t.Locusname = b.Locusname 
                AND t.Alleleindex = b.Alleleindex
            INNER JOIN 
                table_sample s 
                ON s.SampleID = b.SampleID;
        """
        try:
            self.cursor.execute(create_view_query)
            self.connection.commit()
            print("VIEW 'view_allele_sample' created successfully.")
        except sq.Error as e:
            print(f"An error occurred while creating the VIEW: {e}")

    def get_number_nonempty_sequences(self):
        query = """SELECT COUNT(*) 
                   FROM table_allele
                   WHERE Sequenceread != ''
        """
        self.cursor.execute(query)  # Executing the query
        number = self.cursor.fetchone()  # Fetching the result
        return number[0]  # Returning the count

    def get_number_distinct_loci_with_alleles(self):
        query = """SELECT COUNT(DISTINCT Locusname) 
                   FROM table_allele;
        """
        self.cursor.execute(query)
        number = self.cursor.fetchone()
        return number[0]
    
    def get_number_distinct_loci_without_alleles(self):
        query = """SELECT l.Locusname
                   FROM table_loci AS l
                   LEFT JOIN table_allele AS a
                        ON a.Locusname = l.Locusname
                    WHERE a.Locusname IS NULL;
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows
    
    def get_number_distinct_lengths(self):
        query = """SELECT COUNT(DISTINCT Sequencelength) 
                   FROM table_allele;
        """
        self.cursor.execute(query)
        number = self.cursor.fetchone()
        return number[0]

    def get_rows(self, query):
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows


if __name__ == "__main__":
    main()