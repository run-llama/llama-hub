from Bio import Entrez

def fetch_genome_annotation(species_query, rettype='gb', retmode='text'):
    # Provide your email address to NCBI
    Entrez.email = "your_email@example.com"

    # Search for the species
    handle = Entrez.esearch(db="genome", term=species_query)
    record = Entrez.read(handle)
    handle.close()

    if len(record["IdList"]) == 0:
        print(f"No records found for species: {species_query}")
        return None

    # Fetch the genome annotation record
    genome_id = record["IdList"][0]
    handle = Entrez.efetch(db="genome", id=genome_id, rettype=rettype, retmode=retmode)
    annotation_text = handle.read()
    handle.close()

    return annotation_text

# Example usage
species_query = "Escherichia coli"
annotation_text = fetch_genome_annotation(species_query)

if annotation_text:
    print(annotation_text)
