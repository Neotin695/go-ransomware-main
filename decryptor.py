#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FLUTTER SOURCE CODE DECRYPTOR
"""

import os
import sys
from cryptography.fernet import Fernet

def main():
    print("=" * 60)
    print("FLUTTER DECRYPTOR")
    print("=" * 60)
    print()
    print("This will decrypt your Flutter project files")
    print()

    # خيار 1: استخدام المفتاح مباشرة
    print("Option 1: Use encryption key")
    print("Option 2: Use password (if provided by developer)")
    print()

    choice = input("Choose option (1 or 2): ").strip()

    if choice == "1":
        # استخدام المفتاح
        key_input = input("Enter encryption key: ").strip()
        try:
            cipher = Fernet(key_input.encode())
        except:
            print("[ERROR] Invalid key!")
            input("Press Enter to exit...")
            return

    elif choice == "2":
        # استخدام الباسورد (مثال مبسط)
        password = input("Enter password from developer: ").strip()
        # في الواقع، تحتاج لتحويل الباسورد لمفتاح
        # لكن هذا مثال مبسط
        print("[INFO] Password mode requires the original encryption script")
        print("Please ask developer for the encryption key")
        input("Press Enter to exit...")
        return
    else:
        print("[ERROR] Invalid choice!")
        input("Press Enter to exit...")
        return

    # البحث عن الملفات المشفرة وفك تشفيرها
    print()
    print("[DECRYPT] Searching for encrypted files...")

    decrypted_count = 0
    error_count = 0

    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith('.encrypted'):
                file_path = os.path.join(root, file)

                try:
                    with open(file_path, 'rb') as f:
                        encrypted_data = f.read()

                    # فك التشفير
                    decrypted_data = cipher.decrypt(encrypted_data)

                    # استعادة الاسم الأصلي
                    original_name = file_path.replace('.encrypted', '')
                    with open(original_name, 'wb') as f:
                        f.write(decrypted_data)

                    # حذف الملف المشفر
                    os.remove(file_path)

                    print(f"   [OK] {file}")
                    decrypted_count += 1

                except Exception as e:
                    print(f"   [ERROR] {file}")
                    error_count += 1

    # عرض النتائج
    print()
    print("=" * 60)
    print("DECRYPTION RESULTS")
    print("=" * 60)
    print(f"Successfully decrypted: {decrypted_count} files")
    print(f"Errors: {error_count} files")

    if decrypted_count > 0:
        print()
        print("[SUCCESS] Project decrypted successfully!")
        print("You can now run: flutter clean && flutter run")
    else:
        print()
        print("[ERROR] No files were decrypted!")
        print("Possible reasons:")
        print("1. Wrong encryption key")
        print("2. No encrypted files found")
        print("3. Files already decrypted")

    print()
    input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        input("Press Enter to exit...")
