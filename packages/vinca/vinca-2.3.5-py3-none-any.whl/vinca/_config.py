# Configuration for VINCA

# location of the database file
collection_path = '~/cards.db'

# cards with hidden_tags can only be accessed using `vinca -a ...`
# the option flag -a stands for "all cards"
hidden_tags = ['private',]

# integrate vinca with dolthub for easy database backup across multiple devices
# if these are set to None we will use the "collection_path" variable instead
dolt_repo_url = None
dolt_repo_dir = None
