import os
import json
import requests

username = os.getenv("PLAYER")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/90.0.4430.85 Safari/537.36"
}

# Fetch link to archives
def FetchArchives(username):
    url = f"https://api.chess.com/pub/player/{username}/games/archives"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data.get("archives", [])

# Fetch games from archive
def FetchGames(archive_url):
    response = requests.get(archive_url, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data.get("games", [])

# Filter out reviewed games
def FilterGames(games):
    urls = []
    for game in games:
        if game.get("accuracies"):
            continue

        if len(game.get("pgn", "")) > 850: # Length Check to get an estimated of atleast 5 moves per game
            urls.append(game.get("url", ""))
    return urls

# Convert game URL to review URL
def ReviewUrl(game_url):
    return game_url.replace("/game/", "/analysis/game/") + "?tab=review"

# Save URLs to file
def SaveUrls(urls, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        for url in urls:
            f.write(url + "\n")





# Main Code

# Get Archives and reverse the order (latest first)
Archives = FetchArchives(username)
Archives.reverse()

final_urls = []

# Go through archives in order until 10 unreviewed games have been found
for archive in Archives:
    games = FetchGames(archive)
    pre_urls = FilterGames(games)
    pre_urls.reverse() # Reverse the URLs to ensure latest are checked first

    for url in pre_urls:
        if len(final_urls) == 10:
            break
        final_urls.append(ReviewUrl(url))
        
    if len(final_urls) == 10:
        break
    
SaveUrls(final_urls, "urls.txt")
