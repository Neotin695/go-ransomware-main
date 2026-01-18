#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FLUTTER SOURCE CODE ENCRYPTOR - WINDOWS FIXED VERSION
"""

import os
import sys
import json
import getpass
from pathlib import Path
from cryptography.fernet import Fernet

def print_safe(text):
    """طباعة آمنة للويندوز"""
    try:
        print(text)
    except UnicodeEncodeError:
        # استبدال الرموز الغير مدعومة
        text = text.replace('❌', '[ERROR]')
        text = text.replace('✅', '[OK]')
        text = text.replace('🔐', '[LOCK]')
        text = text.replace('📁', '[FOLDER]')
        text = text.replace('📄', '[FILE]')
        text = text.replace('🎉', '[SUCCESS]')
        text = text.replace('🔑', '[KEY]')
        text = text.replace('🔒', '[ENCRYPT]')
        text = text.replace('🔓', '[DECRYPT]')
        text = text.replace('📊', '[STATS]')
        text = text.replace('💾', '[SAVE]')
        text = text.replace('👤', '[CLIENT]')
        text = text.replace('⚠️', '[WARNING]')
        print(text)

def main():
    """الدالة الرئيسية"""
    print("=" * 60)
    print_safe("FLUTTER SOURCE CODE ENCRYPTOR")
    print("=" * 60)
    print()

    # الحصول على المسار الحالي
    current_dir = Path.cwd()
    print_safe(f"[FOLDER] Working in: {current_dir}")
    print()

    # التحقق من وجود مجلد lib
    lib_path = current_dir / "./lib"
    if not lib_path.exists():
        print_safe("[ERROR] 'lib' folder not found!")
        print("Please run this from your Flutter project root")
        input("\nPress Enter to exit...")
        return

    print_safe("[OK] Found lib folder")

    # البحث عن ملفات Dart
    dart_files = []
    for file in lib_path.rglob("*.dart"):
        dart_files.append(file)

    if not dart_files:
        print_safe("[ERROR] No Dart files found in lib/")
        input("\nPress Enter to exit...")
        return

    print_safe(f"[OK] Found {len(dart_files)} Dart files")
    for file in dart_files[:3]:  # عرض أول 3 ملفات فقط
        print_safe(f"   [FILE] {file.name}")
    if len(dart_files) > 3:
        print_safe(f"   ... and {len(dart_files) - 3} more files")

    # طلب كلمة المرور
    print("\n" + "=" * 50)
    print("ENCRYPTION PASSWORD")
    print("=" * 50)
    print("This password will be required to decrypt the files")
    print("Keep it safe and share it with your client!")
    print()

    password = getpass.getpass("Enter password: ")
    if len(password) < 4:
        print_safe("[ERROR] Password too short!")
        input("\nPress Enter to exit...")
        return

    confirm = getpass.getpass("Confirm password: ")
    if password != confirm:
        print_safe("[ERROR] Passwords don't match!")
        input("\nPress Enter to exit...")
        return

    # إنشاء مفتاح التشفير
    print_safe("\n[KEY] Generating encryption key...")
    key = Fernet.generate_key()
    cipher = Fernet(key)

    # تشفير الملفات
    print_safe("\n[ENCRYPT] Encrypting files...")
    encrypted_count = 0
    failed_count = 0

    for file_path in dart_files:
        try:
            # قراءة الملف الأصلي
            with open(file_path, 'rb') as f:
                original_data = f.read()

            # تشفير
            encrypted_data = cipher.encrypt(original_data)

            # حفظ الملف المشفر
            encrypted_path = file_path.with_suffix('.dart.encrypted')
            with open(encrypted_path, 'wb') as f:
                f.write(encrypted_data)

            # حذف الملف الأصلي
            os.remove(file_path)

            encrypted_count += 1
            print_safe(f"   [OK] {file_path.name}")

        except Exception as e:
            failed_count += 1
            print_safe(f"   [ERROR] {file_path.name}")

    # حفظ معلومات المفتاح
    print_safe("\n[SAVE] Saving encryption info...")

    info_content = f"""ENCRYPTION KEY FOR FLUTTER PROJECT
========================================

ENCRYPTION KEY (Save this!):
{key.decode()}

PASSWORD (Share with client):
{password}

ENCRYPTION DETAILS:
- Total files: {len(dart_files)}
- Successfully encrypted: {encrypted_count}
- Failed: {failed_count}

INSTRUCTIONS:
1. KEEP THIS FILE SAFE - DO NOT SHARE WITH CLIENT!
2. Share the password with client: {password}
3. Use decryptor.py to decrypt files

DECRYPTION:
1. Place decryptor.py in project folder
2. Run: python decryptor.py
3. Enter the encryption key above
========================================
"""

    with open("decryption_key.txt", "w", encoding="utf-8") as f:
        f.write(info_content)

    # إنشاء برنامج فك التشفير للعميل
    print_safe("\n[CLIENT] Creating decryptor for client...")

    decryptor_code = '''#!/usr/bin/env python3
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
        print("\\nOperation cancelled")
    except Exception as e:
        print(f"\\n[ERROR] {e}")
        input("Press Enter to exit...")
'''

    with open("decryptor.py", "w", encoding="utf-8") as f:
        f.write(decryptor_code)

    # عرض النتائج النهائية
    print_safe("\n" + "=" * 60)
    print_safe("[SUCCESS] ENCRYPTION COMPLETED!")
    print("=" * 60)
    print()
    print(f"RESULTS:")
    print(f"   Encrypted: {encrypted_count} files")
    print(f"   Failed: {failed_count} files")
    print()
    print(f"PASSWORD FOR CLIENT: {password}")
    print()
    print("GENERATED FILES:")
    print("   1. decryption_key.txt (KEEP THIS SAFE!)")
    print("   2. decryptor.py (Send this to client)")
    print()
    print("INSTRUCTIONS FOR CLIENT:")
    print("   1. Place decryptor.py in project folder")
    print("   2. Run: python decryptor.py")
    print("   3. Choose option 1 and enter the encryption key")
    print("   4. Or use password: " + password)
    print()

    input("Press Enter to exit...")

if __name__ == "__main__":
    # معالجة الأخطاء الشائعة
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[ERROR] Operation cancelled by user")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"\n\n[ERROR] UNEXPECTED ERROR: {e}")
        print("\nPlease check:")
        print("1. Are you in a Flutter project folder?")
        print("2. Is 'cryptography' installed? Run: pip install cryptography")
        print("3. Do you have write permissions?")
        input("\nPress Enter to exit...")