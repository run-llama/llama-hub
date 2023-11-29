"""Genome reader."""

from typing import List
from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class GenomeAnnotationReader(BaseReader):
    """Genome Reader.

    Read read genome annotation from NCBI.

    """

    def load_data(self, species, email, rettype="gb", retmode="text") -> List[Document]:
        """Load genebank genome annotation NCBI's nuccore database.

        Args:
            email [str]: "your_email@example.com"
            species_query [str]: "Homo sapien"
        """
        from Bio import Entrez

        Entrez.email = email

        try:
            # Search for the species
            handle = Entrez.esearch(db="nuccore", term=f"{species} [Organism]")
            record = Entrez.read(handle)
            handle.close()

            if len(record["IdList"]) == 0:
                print(f"No records found for species: {species}")
                return []

            # Fetch the genome annotation record
            genome_id = record["IdList"]

            annotations = []

            for id in genome_id:
                handle = Entrez.efetch(
                    db="nuccore", id=id, rettype=rettype, retmode=retmode
                )
                annotation_text = handle.read()
                handle.close()
                annotations.append(Document(text=annotation_text))

            return annotations

        except Exception as e:
            print(f"An error occurred: {e}")
            return []


if __name__ == "__main__":
    reader = GenomeAnnotationReader()
    print(reader.load_data())
