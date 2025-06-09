import os
import sys

def merge_cs_files(root_dir, output_path):
    """
    root_dir altındaki tüm `.cs` dosyalarını bulur (ancak hiçbir zaman ‘Packages’ klasörüne girmez)
    ve içeriklerini tek bir dosyada (output_path) birleştirir.
    """
    # Eğer zaten var olan bir merged dosya varsa, üzerine yazmak için önce sil
    if os.path.isfile(output_path):
        try:
            os.remove(output_path)
        except Exception as e:
            print(f"Çıkış dosyası silinirken hata oluştu: {e}")
            return

    # os.walk yaparken 'Packages' adlı klasöre asla inmemek için dirnames listesini filtreliyoruz.
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # dirnames içinde 'Packages' varsa çıkaralım; böylece o klasör ve içi adım dahi alınmaz.
        dirnames[:] = [d for d in dirnames if d.lower() != 'packages']

        for filename in filenames:
            if filename.lower().endswith('.cs'):
                cs_path = os.path.join(dirpath, filename)
                try:
                    with open(cs_path, 'r', encoding='utf-8') as cs_file:
                        content = cs_file.read()
                    # Çıktı dosyasına ekle
                    with open(output_path, 'a', encoding='utf-8') as merged_file:
                        merged_file.write(f"// ==== BEGIN FILE: {os.path.relpath(cs_path, root_dir)} ====\n")
                        merged_file.write(content)
                        merged_file.write(f"\n// ==== END FILE: {os.path.relpath(cs_path, root_dir)} ====\n\n")
                    print(f"Merged: {cs_path}")
                except Exception as e:
                    print(f"Error reading {cs_path}: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <Scripts_klasoru_yolu>")
        sys.exit(1)

    root_directory = sys.argv[1]
    if not os.path.isdir(root_directory):
        print(f"Error: {root_directory} geçerli bir klasör değil.")
        sys.exit(1)

    # Script'in (main.py) bulunduğu dizini alıyoruz
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Çıktı olarak oluşturulacak dosya:
    output_file = os.path.join(script_dir, "merged_cs_scripts.txt")

    merge_cs_files(root_directory, output_file)
    print(f"\nTüm geçerli .cs dosyaları birleştirildi ve aşağıdaki dosyaya yazıldı:\n{output_file}")
