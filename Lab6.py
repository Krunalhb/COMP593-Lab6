import requests
import hashlib
import os
import sys

def main():
    # Determine the architecture of the current system (32-bit or 64-bit)
    arch = 'win32' if sys.maxsize <= 2**32 else 'win64'

    # Get the latest version of VLC
    latest_version = get_latest_version()

    # Construct the download URL for the appropriate installer
    url = f'http://download.videolan.org/pub/videolan/vlc/{latest_version}/{arch}/vlc-{latest_version}-{arch}.exe'

    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256(latest_version, arch)

    # Download (but don't save) the VLC installer from the VLC website
    installer_data = download_installer(url)

    # Verify the integrity of the downloaded VLC installer by comparing the expected and computed SHA-256 hash values
    if installer_ok(installer_data, expected_sha256):

        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)

        # Silently run the VLC installer
        run_installer(installer_path)

        # Delete the VLC installer from disk
  #      delete_installer(installer_path)

def get_latest_version():
    url = 'http://download.videolan.org/pub/videolan/vlc/'
    response = requests.get(url)
    versions = []
    for line in response.iter_lines():
        if 'href' in str(line):
            version = str(line).split('"')[1]
            if version.startswith('3.'):
                versions.append(version)
    latest_version = max(versions)
    return latest_version

def get_expected_sha256(version, arch):
    url = f'http://download.videolan.org/pub/videolan/vlc/{version}/{arch}/SHA256SUMS'
    response = requests.get(url)
    expected_sha256 = ''
    for line in response.iter_lines():
        if f'vlc-{version}-{arch}.exe' in str(line):
            expected_sha256 = str(line).split()[0]
    return expected_sha256

def download_installer(url):
    response = requests.get(url)
    installer_data = response.content
    return installer_data

def installer_ok(installer_data, expected_sha256):
    computed_sha256 = hashlib.sha256(installer_data).hexdigest()
    return computed_sha256 == expected_sha256

def save_installer(installer_data):
    installer_path = 'vlc_installer.exe'
    with open(installer_path, 'wb') as f:
        f.write(installer_data)
    return installer_path

def run_installer(installer_path):
    os.system(f'start /wait {installer_path} /S')

#def delete_installer(installer_path):
 #   os.remove(installer_path)

if __name__ == '__main__':
    main()
