def test_rating_average():
    ratings = [5, 3, 4]
    avg = sum(ratings) / len(ratings)
    assert avg == 4