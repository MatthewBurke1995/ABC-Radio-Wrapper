=====
Usage
=====

To use ABC Radio Wrapper in a project::

    import abc_radio_wrapper
    ABC = abc_radio_wrapper.ABCRadio()
    
    #search through latest 100 songs
    search_result = ABC.search(station="triplej", limit=100)

    for radio_play in search_result.radio_songs:
        print(radio_play.song.title)
        for artist in radio_play.song.artists:
            print(artist.name)

To iterate through all songs of a radio channel between two time periods::

    ABC = abc_radio_wrapper.ABCRadio()

    startDate: datetime = datetime.fromisoformat("2020-04-30T03:00:00+00:00")
    endDate: datetime = datetime.fromisoformat("2020-05-01T03:00:00+00:00")

    #search through 24hour period of triplej songs
    for search_result in ABC.continuous_search(from_=startDate, to=endDate, station="triplej"):
        for radio_play in search_result.radio_songs:
            print(radio_play.song.title)
            for artist in radio_play.song.artists:
                print(artist.name)



A blog post with similar usage can be found [here](https://matthewburke.xyz/ABC%20Radio/)
