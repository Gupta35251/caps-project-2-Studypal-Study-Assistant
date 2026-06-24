from youtubesearchpython import VideosSearch

def get_yt_search(query):
    search = VideosSearch(query,limit = 3)
    result = search.result()

    # print(result)

    title = [video['title'] for video in result['result']]
    link = [video['link'] for video in result['result']]
    # print("\n\n\n\n")
    return title,link

# get_yt_search("Python programming")