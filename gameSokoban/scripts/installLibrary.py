import importlib
import subprocess
import sys

def check_and_install_libs(required_libs):
    missing_libs = {}

    for lib, l in required_libs.items():
        try:
            importlib.import_module(lib)
            print(f"Đã có thư viện: {lib}")
        except ImportError:
            print(f"Thiếu thư viện: {lib}")
            missing_libs[lib] = l

    if missing_libs:
        print("\nMột số thư viện còn thiếu:")
        for lib, l in missing_libs.items():
            print(" -", lib)
        choice = input("\nBạn có muốn cài đặt tự động không? (y/n): ").strip().lower()

        while choice != "y" and choice != "n":
            print("Tôi không hiểu ý bạn!")
            choice = input("\nBạn có muốn cài đặt tự động không? (y/n): ").strip().lower()

        if choice == "y":
            for lib, l in missing_libs.items():
                print(f"Đang cài đặt {lib} ...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", l])
            print("\nHoàn tất cài đặt tất cả thư viện.")
            return True
        else:
            print("\nBạn đã chọn không cài đặt. Chương trình kêt thúc!")
            return False
    else:
        print("\nTất cả thư viện cần thiết đã có đầy đủ.")
        return True