
import sqlite3 as sq

def main():

    return 0

class local_database_sqlite():
    def __init__(self, db_path):
        self.connection = sq.connect(db_path)
        self.cursor = self.connection.cursor() #NOT NULL PRIMARY KEY
    
    def create_tables(self):
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
                            Metadata1 VARCHAR(20), 
                            Metadata2 VARCHAR(20),
                            Metadata3 VARCHAR(20),
                            Metadata4 VARCHAR(20),
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


    def insert_dataset(self, primers_dict : dict, matrix_dict : dict, meta_dict : dict, metadata_headers : list):
        #samples_already_processed = []
        loci_already_processed = []

        added_sampleIDs = 0
        ignored_sampleIDs = 0
        
        added_sequences = 0
        ignored_sequences = 0

        try:
            for sampleID, data in matrix_dict.items():
                if (not(sampleID in meta_dict) and not(matrix_dict[sampleID]["Metadata"])):
                    continue

                list_metadata_values = []
                for i, header in enumerate(metadata_headers, 1):
                    list_metadata_values.append(meta_dict[sampleID][header])
                    if (i == 4):
                        break

                row_table_sample = (sampleID,) + tuple(list_metadata_values)
                query_table_sample = """INSERT OR IGNORE INTO table_sample
                            (SampleID, Metadata1, Metadata2, Metadata3, Metadata4) values(?, ?, ?, ?, ?);
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
            return (True, None, added_sequences)
        except Exception as e:
            print(f"An Error occurred when adding the dataset into the local database:\n{e}\n")
            return (False, e, added_sequences)
    

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

    def get_distinct(self, query):
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows


if __name__ == "__main__":
    main()