#!/usr/bin/env python3
import build_repo

if __name__ == "__main__":
    build_repo.generate_sileo_depictions()
    build_repo.generate_static_package_pages()
    build_repo.generate_packages_files()
    build_repo.generate_sitemap()
    build_repo.generate_sileo_featured()
    print("Depictions and Repo files updated successfully.")
