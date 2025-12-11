import datetime
from datetime import date

# Global counters or dictionary to track species counts for IDs
species_counts = {}

def gen_birth_date(age_years, season_born):
    """
    Derives an animal's birthday from the data.
    Returns date in ISO 8601 format (YYYY-MM-DD).
    
    Assumptions for seasons (if not provided, defaults to Jan 1):
    - Spring: March 21
    - Summer: June 21
    - Fall: Sept 21
    - Winter: Dec 21
    """
    current_year = date.today().year
    birth_year = current_year - int(age_years)
    
    season_dates = {
        "spring": "-03-21",
        "summer": "-06-21",
        "fall": "-09-21",
        "winter": "-12-21"
    }
    
    # Default to Jan 1 if season is unknown or not provided
    date_suffix = season_dates.get(season_born.lower(), "-01-01")
    
    return f"{birth_year}{date_suffix}"

def gen_unique_id(species):
    """
    Formulates a unique identifier for each animal.
    Example: Hyena -> Hy01
    """
    # Normalize species name to handle case sensitivity
    species_key = species.lower()
    
    if species_key not in species_counts:
        species_counts[species_key] = 0
    
    species_counts[species_key] += 1
    
    # Take first 2 chars of species and append count (padded to 2 digits)
    prefix = species[:2].capitalize()
    count_str = str(species_counts[species_key]).zfill(2)
    
    return f"{prefix}{count_str}"

def load_names(file_path):
    """
    Reads animalNames.txt and returns a data structure of names.
    (Implementation depends on file format)
    """
    names_dict = {}
    current_species = ""
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.endswith("Names:"):
                    current_species = line.split()[0].lower()
                    names_dict[current_species] = []
                elif line and current_species:
                    names_list = [n.strip() for n in line.split(',')]
                    names_dict[current_species].extend(names_list)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
    return names_dict

def process_zoo_data(input_file, names_file, output_file):
    """
    Main logic to read inputs, process animals, and write the report.
    """
    # 1. Load Names
    species_names = load_names(names_file)
    
    # Dictionary to hold output lines per species
    habitats = {}
    
    # 2. Open Input File
    try:
        with open(input_file, 'r') as f_in:
            lines = f_in.readlines()
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Parse the line
                # Example: "4 year old female hyena, born in spring, tan color, 70 pounds, from Friguia Park, Tunisia"
                parts = [p.strip() for p in line.split(',')]
                
                # Segment 0: "4 year old female hyena"
                first_segment = parts[0].split()
                age = int(first_segment[0])
                sex = first_segment[3]
                species = first_segment[-1]
                
                # Segment 1: "born in spring"
                season = "unknown"
                if "born in" in parts[1]:
                    season = parts[1].replace("born in", "").strip()
                
                # Segment 2: "tan color"
                color = parts[2]
                
                # Segment 3: "70 pounds"
                weight = parts[3]
                
                # Segment 4+: Origin
                origin = ", ".join(parts[4:])

                # 3. Generate Data
                birth_date = gen_birth_date(age, season)
                unique_id = gen_unique_id(species)
                
                # Assign Name
                name = "Unnamed"
                species_key = species.lower()
                if species_key in species_names and species_names[species_key]:
                    name = species_names[species_key].pop(0)
                
                # Arrival Date
                arrival_date = date.today().isoformat()
                
                # Format Output Line
                output_line = f"{unique_id}; {name}; birth date: {birth_date}; {color}; {sex}; {weight}; {origin}; arrived {arrival_date}"
                
                if species_key not in habitats:
                    habitats[species_key] = []
                habitats[species_key].append(output_line)
        
        # 4. Write to Output (Organized by Habitat)
        with open(output_file, 'w') as f_out:
            # Standard order based on assignment usually: Hyena, Lion, Bear, Tiger
            habitat_order = ["hyena", "lion", "bear", "tiger"]
            
            for species in habitat_order:
                if species in habitats:
                    f_out.write(f"{species.capitalize()} Habitat:\n\n")
                    for animal in habitats[species]:
                        f_out.write(f"{animal}\n")
                    f_out.write("\n")
            
            # Write any remaining species not in the standard list
            for species in habitats:
                if species not in habitat_order:
                    f_out.write(f"{species.capitalize()} Habitat:\n\n")
                    for animal in habitats[species]:
                        f_out.write(f"{animal}\n")
                    f_out.write("\n")
                
    except FileNotFoundError:
        print("Error: Input file not found.")

if __name__ == "__main__":
    # Define file paths
    input_path = "arrivingAnimals.txt"
    names_path = "animalNames.txt"
    output_path = "zooPopulation.txt"
    
    print("Starting Zookeeper's Challenge...")
    process_zoo_data(input_path, names_path, output_path)
    print(f"Processing complete. Report generated at {output_path}")