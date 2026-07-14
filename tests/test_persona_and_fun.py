from app.community.handlers.fun import joke, predict


def test_predict_and_joke_keep_distinct_names():
    assert predict.__name__ == "predict"
    assert joke.__name__ == "joke"
    assert predict.__name__ != joke.__name__
