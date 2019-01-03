# LandScape
Bare Metal as Code. No relation to Terraform.

# Usage
1. Install dependencies (pip3 install -r requirements.txt)
2. Populate file with desired configuration (LandScape uses main.ls by default)
    - Multiple hosts can be created
3. Run python3 landscape.py create (-f FILE)
4. Run python3 landscape.py delete (-f FILE) to delete configuration
