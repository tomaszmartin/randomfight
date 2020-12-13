from app.tools import scraper


def test_how_batches_are_generated():
    dataset = [0, 1, 2, 3, 4]
    batches = [batch for batch in scraper.batch(dataset, 3)]
    assert batches[0] == ([0, 1, 2], 0)
    assert batches[1] == ([3, 4], 3)
    assert len(batches[0][0]) + len(batches[1][0]) == len(dataset)
